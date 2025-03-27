import unittest
from io import StringIO
import sys
from src.secsem.lab1.task4 import call_limiter

class TestCallLimiterDecorator(unittest.TestCase):
    def setUp(self):
        # Перехватываем stdout для проверки вывода
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        # Восстанавливаем stdout
        sys.stdout = self.original_stdout
        self.held_output.close()

    def test_method_within_limit(self):
        """Тест вызовов в пределах лимита"""
        @call_limiter(limit=2)
        class TestClass:
            def test_method(self):
                return "success"
        
        obj = TestClass()
        self.assertEqual(obj.test_method(), "success")
        self.assertEqual(obj.test_method(), "success")

    def test_method_exceeds_limit(self):
        """Тест превышения лимита вызовов"""
        @call_limiter(limit=1)
        class TestClass:
            def test_method(self):
                return "success"
        
        obj = TestClass()
        obj.test_method()
        with self.assertRaises(RuntimeError) as context:
            obj.test_method()
        
        self.assertEqual(str(context.exception),
                        "Метод 'test_method' не может быть вызван более 1 раз")

    def test_multiple_methods(self):
        """Тест нескольких методов"""
        @call_limiter(limit=1)
        class TestClass:
            def method1(self):
                pass
            
            def method2(self):
                pass
        
        obj = TestClass()
        obj.method1()
        obj.method2()
        
        with self.assertRaises(RuntimeError):
            obj.method1()
        
        with self.assertRaises(RuntimeError):
            obj.method2()

    def test_private_methods_unlimited(self):
        """Тест что приватные методы не ограничены"""
        @call_limiter(limit=1)
        class TestClass:
            def public_method(self):
                pass
            
            def _private_method(self):
                pass
        
        obj = TestClass()
        obj._private_method()
        obj._private_method()  # Не должно вызывать ошибку
        
        obj.public_method()
        with self.assertRaises(RuntimeError):
            obj.public_method()

if __name__ == '__main__':
    unittest.main()