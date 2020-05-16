import time


def decorator_outer_with_arguments(decorator_arg):
    print("Зовнішній декоратор отимав аргумент:", decorator_arg)

    def my_decorator(func):
        print(f"Внутрішнім декоратор отримав арумент {decorator_arg}, переданий від зовнінього")

        def wrapper(function_arg1, function_arg2):
            print(f"Wrapper - обгортка навколо декорованої функції. Вона може працювати зі всіма аргументами:\n"
                  f"\t- і декоратора: {decorator_arg} \n"
                  f"\t- і функції: {function_arg1}, {function_arg2}\n"
                  f"Також Wrapper передає відповідні, але не всі аргументи далі в декоровану функцію:")

            start_time = time.time()
            for i in range(decorator_arg):
                result = func(function_arg1, function_arg2)

            print(f"\nНазва виконаної функції: '{func.__name__}', "
                  f"\nкількість відпрацьованих ітерацій для цієї функції в підсумку становить: {decorator_arg},"
                  f"\nа загальний час виконання всіх ітерацій - {time.time() - start_time} с")

        return wrapper

    return my_decorator


@decorator_outer_with_arguments(5)
def decorated_function_with_arguments(function_arg1, function_arg2):
    print("Декорована функція, що приймає тільки свої аргументи: {0}"
          " {1}".format(function_arg1, function_arg2))
    temp_list = []
    for i in range(function_arg1):
        temp_list.append(i**function_arg2 - (i-1)**function_arg2)
    print(temp_list[-1])


decorated_function_with_arguments(100000, 3)

