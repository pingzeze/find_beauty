# 实现了 __get__、__set__ 或 __delete__ 方法的类是描述符
# 描述符的用法是，创建一个实例，作为另一个类的类属性


class Quantity:
    """描述符类"""
    def __init__(self, storage_name):
        self.storage_name = storage_name

    # 实现__set__即可以看作是描述符类，默认实现__get__方法
    # def __get__(self, instance, owner):
    #     print(f"owner -> {owner}, {id(owner)}")  # 4
    #     print(f"get instance -> {instance.__dict__[self.storage_name]}, {id(instance.__dict__[self.storage_name])}")  # 5
    #     return instance.__dict__[self.storage_name]

    def __set__(self, instance, value):
        print(f"instance -> {instance}")  # 2
        if value > 0:
            # setattr(instance, self.storage_name, value)  # 托管属性和储存属性名称一样，导致使用setattr会造成无限递归
            instance.__dict__[self.storage_name] = value
            print(f"set instance -> {instance.__dict__[self.storage_name]}, {id(instance.__dict__[self.storage_name])}")  # 3
        else:
            raise ValueError('value must be > 0')


class LineItem:
    """托管类"""
    # 托管类属性 == 描述符类实例
    weight = Quantity('weight')
    print(f"weight -> {weight}, {id(weight)}")  # 1

    def __init__(self, description, weight):
        self.description = description
        self.weight = weight
        print(f"self.weight -> {self.weight}, {id(self.weight)}")  # 8

    def subtotal(self):
        return self.weight


truffle = LineItem('White truffle', 100)


"""输出
weight -> <__main__.Quantity object at 0x0132FEB0>, 20119216    托管类属性 == 描述符类实例
instance -> <__main__.LineItem object at 0x018A3E10>            __set__ 中传入的instance == 托管类对象
set instance -> 100, 2036522720
owner -> <class '__main__.LineItem'>, 25925048                  __get__ 中传入owner == 托管类引用 ？？？不理解这里？？？
get instance -> 100, 2036522720
owner -> <class '__main__.LineItem'>, 25925048
get instance -> 100, 2036522720                                 使用self.weight时调用 __get__ 方法
self.weight -> 100, 2036522720                                  描述符实例属性 赋值给 托管类实例属性
"""