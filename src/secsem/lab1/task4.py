def call_limiter(limit):
    def decorator(cls):
        class Wrapped(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._call_counts = {}

            def __getattribute__(self, name):
                attr = super().__getattribute__(name)
                if callable(attr) and not name.startswith('_'):
                    if name not in self._call_counts:
                        self._call_counts[name] = 0
                    
                    def wrapped(*args, **kwargs):
                        if self._call_counts[name] >= limit:
                            raise RuntimeError(f"Метод '{name}' не может быть вызван более {limit} раз")
                        self._call_counts[name] += 1
                        return attr(*args, **kwargs)
                    
                    return wrapped
                return attr
        return Wrapped
    return decorator

@call_limiter(limit=2)
class MyClass:
    def method1(self):
        print("Method 1 called")
    
    def method2(self):
        print("Method 2 called")

obj = MyClass()
