# 1. 获取类中变量
# 下文中 bool143 = True 是类的变量
# 类即对象，也可以看作是获取对象的key
class Example(object):
    bool143 = True
    bool2 = True
    blah = False
    foo = True
    foobar2000 = False
 
example = Example()
# callable 可调用的，startswith 找出非魔法函数的
members = [attr for attr in dir(example) if not callable(getattr(example, attr)) and not attr.startswith("__")]
print (members)   # 输出 ['blah', 'bool143', 'bool2', 'foo', 'foobar2000']
