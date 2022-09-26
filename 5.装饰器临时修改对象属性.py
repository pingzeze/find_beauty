# 使用装饰器临时修改对象属性
# 装饰器适用于方法中，判断对象是否包含指定属性
def set_temporary_attr_value(attr, value, *, obj=None):
    """
    临时改变某个类属性的值，函数运行完毕之后恢复
    :param attr: 类属性名
    :param value: 属性值
    :param obj: 需要修改属性的对象
    :return: 
    """
    def handler(func):  # 不在装饰器函数中传递func，使得装饰器可以使用参数进行操作
        def inner(self, *args, **kwargs):
            obj_ = obj if obj is not None else self  # obj 类实例化对象
            if not hasattr(obj_, attr):
                raise ValueError(f"对象:{obj_.__class__.__name__} 缺失属性: {attr}")
            his_value = getattr(obj_, attr)
            setattr(obj_, attr, value)
            try:
                # 一般func不需要传递self
                res = func(self, *args, **kwargs)   # 可能会修改self的属性，重新传参self
            finally:
                setattr(obj_, attr, his_value)
            return res

        return inner

    return handler

class Test:
    @set_temporary_attr_value("is_auto_switch_frame", True, obj=browser_base)
    def test_1(self):
        pass