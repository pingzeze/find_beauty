# 实现动态属性获取json数据
# 实例.属性 方式获取预期数据
# 通过 __getattr__ 方法实现“虚拟属性”，当访问不存在的属性时（如 obj.no_such_attribute），即时计算属性的值。


import json
from collections import abc

test1 = """
{
  "Schedule": {
    "conferences": [
      {
        "serial": 115
      }
    ],
    "events": [
      {
        "serial": 34505,
        "name": "Why Schools Don´t Use Open Source to Teach Programming",
        "event_type": "40-minute conference session",
        "time_start": "2014-07-23 11:30:00",
        "time_stop": "2014-07-23 12:10:00",
        "venue_serial": 1462,
        "description": "Aside from the fact that high school programming...",
        "website_url": "http://oscon.com/oscon2014/public/schedule/detail/34505",
        "speakers": [
          157509
        ],
        "categories": [
          "Education"
        ]
      }
    ],
    "speakers": [
      {
        "serial": 157509,
        "name": "Robert Lefkowitz",
        "photo": null,
        "url": "http://sharewave.com/",
        "position": "CTO",
        "affiliation": "Sharewave",
        "twitter": "sharewaveteam",
        "bio": "Robert ´r0ml´ Lefkowitz is the CTO at Sharewave, a startup..."
      }
    ],
    "venues": [
      {
        "serial": 1462,
        "name": "F151",
        "category": "Conference Venues"
      }
    ]
  }
}"""


class FrozenJSON:
    """一个只读接口，使用属性表示法访问JSON类对象
    """

    def __new__(cls, arg):
        """构造方法，返回一个实例
        1. 始终都是类的静态方法
        2. 如果__new__()没有返回cls（即当前类）的实例，
           那么当前类的__init__()方法是不会被调用的，只会调用被返回的那个类的构造方法
        """
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)  # 返回object.__new__(FrozenJSON)，FrozenJSON类实例
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]  # 1
        else:
            return arg

    def __init__(self, mapping):
        """初始化方法，接受__new__的实例为第一个参数"""
        self.__data = {}
        for key, value in mapping.items():
            # 防止出现关键字，导致异常
            key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):  # hasattr 判断实例是否有对应属性 eg.实例.属性
            return getattr(self.__data, name)
        else:
            return FrozenJSON(self.__data[name])


raw_feed = json.loads(test1)
feed = FrozenJSON(raw_feed)
len(feed.Schedule_.speakers_)
sorted(feed.Schedule_.keys())
talk = feed.Schedule_.events_[0]
print(talk.name_)


"""对 # 1 重点解释
返回[FrozenJSON(item1), FrozenJSON(item2)]，然后对列表中项都会再调用构造方法初始化
可以通过下标方式获取对应实例：feed.Schedule_.events_[0]
"""

class Test2:
    def __new__(cls, a_):
        if isinstance(a_, abc.MutableSequence):  # 如果写成 def __new__(cls, a_): return [cls(item) for item in a_] 会进入死循环
            return [cls(item) for item in a_]
        elif isinstance(a_, str):
            return super().__new__(cls)
        else:
            return a_

    def __init__(self, a_):
        self.a_ = a_


test2 = Test2(["777", 888])  # test2[1].a_ 输出888
test3 = Test2("777")         # test3.a_    输出"777"
test4 = Test2(777)           # test4       输出777