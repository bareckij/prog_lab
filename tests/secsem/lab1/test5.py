import unittest
from io import StringIO
import sys
import asyncio
from src.secsem.lab1.task5 import first_function, second_function, main 

class TestAsyncFunctions(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = self.original_stdout
        self.held_output.close()

    async def test_first_function(self):
        """Тест первой асинхронной функции"""
        await first_function()
        
        output = self.held_output.getvalue().strip().split('\n')
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0], "Функция 1 - первый print")
        self.assertEqual(output[1], "Функция 1 - второй print")
        self.assertEqual(output[2], "Функция 1 - третий print")

    async def test_second_function(self):
        """Тест второй асинхронной функции"""
        await second_function()
        
        output = self.held_output.getvalue().strip().split('\n')
        self.assertEqual(len(output), 4)
        self.assertEqual(output[0], "Функция 2 - первый print")
        self.assertEqual(output[1], "Функция 2 - второй print")
        self.assertEqual(output[2], "Функция 2 - третий print")
        self.assertEqual(output[3], "Функция 2 - четвертый print")

    async def test_main_function(self):
        """Тест основной функции с gather"""
        await main()
        
        output = self.held_output.getvalue().strip().split('\n')
        self.assertEqual(len(output), 7)
        
        self.assertIn("Функция 1 - первый print", output[:2])
        self.assertIn("Функция 2 - первый print", output[:2])
        
        # Проверяем остальные вызовы
        self.assertEqual(output[2], "Функция 1 - второй print")
        self.assertEqual(output[3], "Функция 2 - второй print")
        self.assertEqual(output[4], "Функция 2 - третий print")
        self.assertEqual(output[5], "Функция 1 - третий print")
        self.assertEqual(output[6], "Функция 2 - четвертый print")


if __name__ == '__main__':
    unittest.main()