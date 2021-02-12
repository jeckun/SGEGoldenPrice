def callback(fun, args=(), **kwargs):
    """ 回调函数
    fun: 被回调函数名称
    args: 回调函数的参数
    kwargs: 其他参数
    """
    a = []
    if len(args) != len(fun.__code__.co_varnames):
        raise Exception("参数数量不一致")
    cmd = "fun("
    for i in range(len(fun.__code__.co_varnames)):
        item = "args[%d]" % i
        a.append(item)
    cmd = cmd + ', '.join(a) + ')'
    return eval(cmd)


def add(x, y):
    return x + y


a = callback(add, (2, 4))
print(a)


def text(text):
    return text.replace('\r', '').replace('-', '').replace(
        '\t', '').replace('\n', '').replace(',', '').replace(' ', '')
