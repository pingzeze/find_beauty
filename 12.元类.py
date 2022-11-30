"""元类
所有类都是 type 的实例，最终都是 object 的子类。但是元类是 type 的子类，因此可以作为制造类的工厂。
object 是 type 的实例，而 type 是 object 的子类。type 是自身的实例
type(类名, (父类, ), {属性}) 可以创建自定义类的实例: type("AAA", (object, ), {"say1": 111})
type(对象) isinstance(对象, 类) 都可以查看实例由什么类创建; instance 还可以判断父类
"""