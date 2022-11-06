# 通过不使用可变类型参数和浅复制实现防御性参数
# 不可变类型参数：int、str、tuple

# 可变类型参数会造成指向同一地址修改形参同步修改了实参值

# 正确示例
class TwilightBus:
    """校车功能：实现对上车下车校车人名列表"""
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)  # 对传入参数做浅复制
    def pick(self, name):
        self.passengers.append(name)
    def drop(self, name):
        self.passengers.remove(name)
basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
bus = TwilightBus(basketball_team)
bus.passengers[0] = 'li'
bus.drop('Tina')
bus.drop('Pat')
print(basketball_team)  # ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
print(bus.passengers)   # ['li', 'Maya', 'Diana']，对passengers和basketball_team指向不同地址

# 使用可变类型作为参数的默认值
class TwilightBus2:
    """校车功能：实现对上车下车校车人名列表"""
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers  # self.passengers和passengers参数指向同一地址
    def pick(self, name):
        self.passengers.append(name)
    def drop(self, name):
        self.passengers.remove(name)
basketball_team2 = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
bus2 = TwilightBus2(basketball_team2)
bus2.passengers[0] = 'li'
bus2.drop('Tina')
bus2.drop('Pat')
print(basketball_team2)  # ['li', 'Maya', 'Diana']  修改passengers时也会对basketball_team2指向同一地址的修改
print(bus2.passengers)   # ['li', 'Maya', 'Diana']

# 实例共享同一默认参数
class TwilightBus3:
    """校车功能：实现对上车下车校车人名列表"""
    def __init__(self, passengers=[]):
        self.passengers = passengers  # self.passengers和passengers参数指向同一地址
    def pick(self, name):
        self.passengers.append(name)
    def drop(self, name):
        self.passengers.remove(name)
bus3 = TwilightBus3()
bus3.pick('Tina')
print(bus3.passengers)
bus4 = TwilightBus3()
print(TwilightBus3.__init__.__defaults__)   # (['Tina'],) __defaults__ 输出函数默认参数，元组形式返回
print(bus4.passengers)  # bus3bus4对象实参使用默认参数，都指向同一地址，因此bus3修改bus4同步修改
