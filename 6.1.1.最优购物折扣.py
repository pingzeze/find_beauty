from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')  # fidelity 积分

"""
策略假如一个网店制定了下述折扣规则。
有 1000 或以上积分的顾客，每个订单享 5% 折扣。
同一订单中，单个商品的数量达到 20 个或以上，享 10% 折扣。
订单中的不同商品达到 10 个或以上，享 7% 折扣。
"""


class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:  # 上下文
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)    # discount的传参self，即是Order对象
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


class Promotion(ABC):  # 策略：抽象基类
    @abstractmethod
    def discount(self, order):
        """返回折扣金额（正值）"""
        pass


class FidelityPromo(Promotion):  # 第一个具体策略
    """为积分为1000或以上的顾客提供5%折扣"""
    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0


class BulkItemPromo(Promotion):  # 第二个具体策略
    """单个商品为20个或以上时提供10%折扣"""
    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * .1
        return discount


class LargeOrderPromo(Promotion):  # 第三个具体策略
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * .07
        return 0


# promos = [FidelityPromo(), BulkItemPromo(), LargeOrderPromo()]
# globals() 返回字典，包含当前模块(非调用模块)的所有函数方法类
"""类似于
{'Promotion': <class '__main__.Promotion'>,
 'FidelityPromo': <class '__main__.FidelityPromo'>,
 'BulkItemPromo': <class '__main__.BulkItemPromo'>,
 'LargeOrderPromo': <class '__main__.LargeOrderPromo'>}
"""
promos = [v() for k, v in globals().items() if k.endswith("Promo")]  # 新增优惠，不用每次修改promos列表


def best_promo(order):
    """选择可用的最佳折扣"""
    return max(promo.discount(order) for promo in promos)   # 取得最佳策略


if __name__ == '__main__':
    globals()
    joe = Customer('John Doe', 0)
    ann = Customer('Ann Smith', 1100)
    cart = [LineItem('banana', 4, .5), LineItem('apple', 10, 1.5), LineItem('watermellon', 5, 5.0)]
    print(Order(joe, cart, best_promo))  # <Order total: 42.00 due: 42.00>
    print(Order(ann, cart, best_promo))  # <Order total: 42.00 due: 39.90>
