from threading import Thread


def create_thread(name_thread, daemon):
    def decorator(func):
        def wrapper(num=5000000):
            t = Thread(target=func, args=(num,), daemon=daemon, name=name_thread)
            t.start()
        return wrapper
    return decorator


@create_thread('Take_last_num', False)
def think_about(num):
    list_aggregator = [x ** 3 - x ** 2 for x in range(num)]
    print(list_aggregator[-1])


print('Start of think_about')
think_about()
print('End of think_about')
# 124999900000024999998