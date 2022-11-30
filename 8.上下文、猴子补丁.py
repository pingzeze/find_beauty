# 使用@contextmanager实现上下文管理
# 猴子补丁实现，动态绑定
import contextlib

@contextlib.contextmanager  # 1. 实现上下文管理
def looking_glass():
    import sys
    original_write = sys.stdout.write  # 将原本实现赋值给变量
    def reverse_write(text):
        original_write(text[::-1])
    sys.stdout.write = reverse_write  # 猴子补丁，动态绑定方法到write上
    msg = ''
    try:                    # 2
        yield 'JABBERWOCKY'  # 输出值，作为as的接受
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write # 还原
        if msg:
            print(msg)

# 1. yield前类比为 __enter__，yield后类比为 __exit__
# 2. 如果在 with 块中抛出了异常，Python 解释器会将其捕获，然后在 looking_glass 函数的 yield 表达式里再次抛出。
#    但是，那里没有处理错误的代码，因此 looking_glass 函数会中止，永远无法恢复成原来的 sys.stdout.write 方法，导致系统处于无效状态。


with looking_glass() as what:
    print('Alice, Kitty and Snowdrop')  # 输出：pordwonS dna yttiK ,ecilA
    print(what)                         # 输出：YKCOWREBBAJ

"""
contextlib.contextmanager 装饰器会把函数包装成实现__enter__ 和 __exit__ 方法的类。
这个类的 __enter__ 方法有如下作用。
(1) 调用生成器函数，保存生成器对象（这里把它称为 gen）。
(2) 调用 next(gen)，执行到 yield 关键字所在的位置。
(3) 返回 next(gen) 产出的值，以便把产出的值绑定到 with/as 语句中的目标变量上。

with 块终止时，__exit__ 方法会做以下几件事。
(1) 检查有没有把异常传给 exc_type；如果有，调用gen.throw(exception)，在生成器函数定义体中包含 yield 关键字的那一行抛出异常。
(2) 否则，调用 next(gen)，继续执行生成器函数定义体中 yield 语句之后的代码。
"""