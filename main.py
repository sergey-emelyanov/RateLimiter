import time


class RateLimiter:

    @staticmethod
    def log_calls(func):
        def wrapper(*args, **kwargs):
            print(f'Вызов метода: {func.__name__}')
            print(f'Аргументы {args} {kwargs}')
            result = func(*args, **kwargs)
            return result

        return wrapper

    @staticmethod
    def limit_calls(count, maxcols_per_time):

        def actual_decorator(func):
            kol = 0
            start = time.time()

            def wrapper(*args, **kwargs):
                nonlocal kol
                if kol < count:
                    kol += 1
                    result = func(*args, **kwargs)
                    return result
                else:
                    delta = time.time() - start
                    if delta >= maxcols_per_time:
                        return 'Привышен лимит'
                    else:
                        result = func(*args, **kwargs)
                        return result

            return wrapper

        return actual_decorator

    @staticmethod
    @limit_calls(5, 3)
    @log_calls
    def some_method(a, b):
        return a + b

    @staticmethod
    @limit_calls(5, 3)
    @log_calls
    def another_method():
        return 'Some string'


for i in range(7):
    val = RateLimiter.some_method(i, i)
    time.sleep(1)
    print(val)

for i in range(7):
    val = RateLimiter.another_method()
    time.sleep(0.5)
    print(val)
