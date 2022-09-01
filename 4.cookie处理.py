# 4. cookie处理
# split("|", 1) 已第一个 | 为分割，返回列表

"""原生cookie
[
 {'domain': 'etax.qingdao.chinatax.gov.cn', 'httpOnly': True, 'name': 'PORTAL_SESSIONID', 'path': '/', 'secure': False, 'value': 'HPv4HW2E4Zo24w8xgDoZe31doJiv_FyDG4iUAfuwVTRqaorJmqtG!409761532'}, 
 {'domain': 'etax.qingdao.chinatax.gov.cn', 'httpOnly': True, 'name': 'SSO_SESSIONID', 'path': '/', 'secure': False, 'value': '3EX4HSIgUYeMDyPQtrcE0QYGCRol9ssczYsp7NCrnmgzuIVLrEDC!274811488!-1587463982'}, 
 {'domain': 'etax.qingdao.chinatax.gov.cn', 'httpOnly': False, 'name': 'SF_cookie_42', 'path': '/', 'secure': False, 'value': '60742684'}
 ]
"""

ck = browser_base.driver.get_cookies()
cookie_list = [f'{item["name"]}={item["value"]}' for item in ck]
cookie_str = ";".join(cookie_list)

"""cookie_str
'PORTAL_SESSIONID=HPv4HW2E4Zo24w8xgDoZe31doJiv_FyDG4iUAfuwVTRqaorJmqtG!409761532;SSO_SESSIONID=3EX4HSIgUYeMDyPQtrcE0QYGCRol9ssczYsp7NCrnmgzuIVLrEDC!274811488!-1587463982;SF_cookie_42=60742684'
"""

cookies = dict([item.split("=", 1) for item in cookie_str.split(";")])  # List[List[str, str]]

"""cookies
{'PORTAL_SESSIONID': 'HPv4HW2E4Zo24w8xgDoZe31doJiv_FyDG4iUAfuwVTRqaorJmqtG!409761532', 
'SSO_SESSIONID': '3EX4HSIgUYeMDyPQtrcE0QYGCRol9ssczYsp7NCrnmgzuIVLrEDC!274811488!-1587463982', 
'SF_cookie_42': '60742684'}
"""
