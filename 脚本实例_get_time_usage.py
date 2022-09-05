import argparse
import functools
import xlwt
from typing import Dict, Optional, Union, List

import requests
from loguru import logger

SERVER = "http://taxsupport.yunzhangfang.com"
HEADERS = {

    # cookie 隔段时间会失效，手动拷过来替换一下就行
    "Cookie": "_ga=GA1.2.1691642416.1649320534; Hm_lvt_5b07def52c26a375c2ec8059668f1c81=1658914443,1659441616; dd_refresh_token=6b1852d5094c4fa49b4b621766ec7cee; userInfo={%22userId%22:668%2C%22username%22:%22%E8%B5%B5%E5%BE%B7%E6%88%90%22}; dd_access_token=eyJhbGciOiJIUzI1NiJ9.eyJzZXQiOiIiLCJwaG9uZSI6IjE4ODk1MzE3NjIyIiwiZ3NJZCI6ImRlZmF1bHQiLCJpc3MiOiJhdXRoMCIsInVzZXJOYW1lIjoiMDBpU1Ztc1NINEkwbkd3UGM0Y2NuOHdpRWlFIiwiZXhwIjoxNjYyMDA1NjYyLCJ1c2VySWQiOiItMjAyMTMxOTkyOCJ9.bPGU1ilR2VZuC1to29pQjqjgdrriUymzYB5X0uPG5cA",
}

Nums = Union[float, int]


class Handler:

    def __init__(self, area_code):
        self.area_code = area_code
        self.session = requests.session()
        self.session.headers = HEADERS

    def _get_time_usage(
            self,
            start_date: str,
            end_date: str,
            task_type: Optional[str] = None,
            task_status: Optional[str] = None
    ) -> Dict[str, Union[str, int]]:

        url = SERVER + "/tax/dash/timeArea"

        params = {
            "beginDate": start_date,
            "endDate": end_date,
            "areaCode": self.area_code,
            "timeType": 3,
        }

        if task_type is not None:
            params["taskType"] = task_type

        if task_status is not None:
            params["taskStatus"] = task_status

        response = self.session.get(url, params=params)
        return response.json()["data"][0]

    def get_time_usage(self, start_date: str, end_date: str) -> List[List[Nums]]:
        get_time_usage = functools.partial(self._get_time_usage, start_date=start_date, end_date=end_date)

        result = []

        data_dict_1 = get_time_usage(task_type="5", task_status="1")  # 申报-成功
        data_list_1 = self.extract_data_list_from_data_dict(data_dict_1)
        result.append(data_list_1)

        data_dict_2 = get_time_usage(task_type="5")  # 申报-all
        data_list_2 = self.extract_data_list_from_data_dict(data_dict_2)
        result.append(data_list_2)

        data_dict_3 = get_time_usage(task_status="1")  # 申报-all
        data_list_3 = self.extract_data_list_from_data_dict(data_dict_3)
        result.append(data_list_3)

        data_dict_4 = get_time_usage()  # all-all
        data_list_4 = self.extract_data_list_from_data_dict(data_dict_4)
        result.append(data_list_4)

        return result

    @staticmethod
    def extract_data_list_from_data_dict(data_dict: Dict) -> List[Nums]:
        return [
            data_dict["loginOnRuntime"],  # 登录
            data_dict["executeWaitRuntime"],  # 等待执行
            data_dict["executeTaskRuntime"],  # 任务执行
            data_dict["returnWaitRuntime"],  # 等待返回
            data_dict["taskReturnRuntime"],  # 任务返回
            data_dict["ready2RetryRuntime"],  # 准备重试
            data_dict["taskReceiptRuntime"],  # 任务回执
            data_dict["interceptProcessRuntime"],  # 拦截处理

            data_dict["loginOnRuntime_num"],  # 登录
            data_dict["executeWaitRuntime_num"],  # 等待执行
            data_dict["executeTaskRuntime_num"],  # 任务执行
            data_dict["returnWaitRuntime_num"],  # 等待返回
            data_dict["taskReturnRuntime_num"],  # 任务返回
            data_dict["ready2RetryRuntime_num"],  # 准备重试
            data_dict["taskReceiptRuntime_num"],  # 任务回执
            data_dict["interceptProcessRuntime_num"],  # 拦截处理
        ]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--area", type=str, help="地区编码", required=True)
    args = parser.parse_args()

    month_mapping = {
        "六月": {"start_date": "2022-06-01", "end_date": "2022-06-30"},
        "七月": {"start_date": "2022-07-01", "end_date": "2022-07-31"},
        "八月": {"start_date": "2022-08-01", "end_date": "2022-08-31"},
    }

    h = Handler(area_code=args.area)

    work_book = xlwt.Workbook(encoding="utf-8")

    for month, date_dict in month_mapping.items():
        logger.info(f"开始抓取【{month}】份数据")
        sheet = work_book.add_sheet(month)
        data_list = h.get_time_usage(date_dict["start_date"], date_dict["end_date"])
        for row_index, row in enumerate(data_list):
            for col_index, data in enumerate(row):
                sheet.write(row_index, col_index, data)
        logger.info(f"【{month}】抓取完成")

    work_book.save("耗时统计.xls")

    logger.info("所有数据抓取完成！")
