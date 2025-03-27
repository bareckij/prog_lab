import time

def logger(show=True):
    def decorator(cls):
        def log_methods(method):
            def wrapper(*args, **kwargs):
                class_name = args[0].__class__.__name__
                method_name = method.__name__

                print(f'Имя класса {class_name}')
                print(f'Имя метода {method_name}')
                print(f"Аргументы.{args[1:]}")
                start_time = time.time()
                result = method(*args, **kwargs)
                exec_time = time.time() - start_time
                print(f'Время выполнения {exec_time}')
                print(f'Результат {result}')
                return result
            return wrapper
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value): 
                is_magic = attr_name.startswith('__') and attr_name.endswith('__')
                if not is_magic or show: 
                    setattr(cls, attr_name, log_methods(attr_value))
        return cls
    return decorator


@logger(show=True) 
class MyClass:
    def __init__(self, value):
        self.value = value
    
    def add(self, a, b):
        return a + b
    
    def __str__(self):
        return f"MyClass with value: {self.value}"

obj = MyClass(10)  # __init__ будет залогирован
print(obj.add(2, 3))  # add будет залогирован
print(str(obj))  # __str__ будет залогирован