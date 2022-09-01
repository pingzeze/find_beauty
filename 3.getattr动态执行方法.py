# 3. getattr实现动态执行方法
# self 指类实例化对象，_start_{browser_type}_browser 拼接的类方法
function = getattr(self, f"_start_{browser_type}_browser")
function()  # 执行方法

# hassttr 判断对象属性是否存在
# importlib.import_module 动态导包
module = importlib.import_module("tasks." + login_dict["function"])  # 导入模块
if not hasattr(module, "RunTask"):
    logger.error(f"【%s】未找到RunTask类，跳过当前注册，请检查" % login_dict["function"])