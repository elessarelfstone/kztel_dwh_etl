import time


def timeit(measure="mins"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print("Elapsed time : {} minutes {} seconds".
                  format(divmod(end-start, 60)[0], int(divmod(end-start, 60)[1])))
            return result
        return wrapper
    return decorator
