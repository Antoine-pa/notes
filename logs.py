from time import time

def log(func):
    def wrapper(*args, **kwargs):
        t = time()
        val = func(*args, **kwargs)
        t = time() - t
        with open("logs.txt", "w") as f:
            f.write("args : " + " ".join([str(arg) for arg in args]) + "\nkwargs : " + " ".join(str(kwarg[0]) + ' = ' + str(kwarg[1]) for kwarg in kwargs.items()) + "\ntime : " + str(t) + "\nvalue return : " + str(val))
        return val
    return wrapper

def w(*t):
    with open("output_log.txt", "w") as f:
        f.write(str(t))