import time 

def logger(func): 
    def wrapper(*args, **kwargs): 
        start_time = time.time()
        result = func(*args, **kwargs)
        exec_time = time.time() - start_time
        print(f"Имя функции: {func.__name__}")
        print(f"Аргументы. Позиционные: {args}, именнованные: {kwargs}")
        print(f'Результат: {result}')
        print(f'Время {exec_time:.6f} секунд')
        return result 
    return wrapper


@logger
def add(a, b):
    return a+b 

add(5, 2)

@logger
def greet(name, greet='Привет!'):
    return greet + ' ' + name 

greet('maksim')