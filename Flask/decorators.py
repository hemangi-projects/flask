# def smart_divide(func):
#     def inner(a, b):
#         print("I am going to divide", a, "and", b)
#         if b == 0:
#             print("Whoops! cannot divide")
#             return
#
#         return func(a, b)
#     return inner
#
#
# @smart_divide
# def divide(a, b):
#     print(a/b)
#
# divide(5,0)
# ======================================================================================================================

def star(func):
    def inner(*args, **kwargs):
        print("*" * 30)
        func(*args, **kwargs)
        print("*" * 30)
    return inner


def percent(func):
    def inner(*args, **kwargs):
        print("%" * 30)
        func(*args, **kwargs)
        print("%" * 30)
    return inner


@percent
@star
def printer(msg):
    print(msg)


printer("Hello")