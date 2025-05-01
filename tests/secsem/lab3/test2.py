import os
import unittest
import tempfile
import shutil
from unittest.mock import patch

class TestDirectoryOperations(unittest.TestCase):
    """Тесты для операций с директориями и файлами."""
    
    def setUp(self):
        """Создание временной тестовой среды."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        # Создаем исходный файл как в основном скрипте
        self.original_file = 'example_file.txt'
        with open(self.original_file, 'w') as f:
            f.write("Пример содержимого файла\n")

    def tearDown(self):
        """Очистка тестовой среды."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_file_copy(self):
        """Тест копирования файла."""
        copied_file = 'copied_file.txt'
        shutil.copy2(self.original_file, copied_file)
        
        self.assertTrue(os.path.exists(copied_file))
        with open(copied_file, 'r') as f:
            content = f.read()
        self.assertEqual(content, "Пример содержимого файла\n")

    def test_file_rename_and_move(self):
        """Тест переименования и перемещения файла."""
        renamed_file = 'renamed_file.txt'
        os.rename(self.original_file, renamed_file)
        
        nested_dirs = os.path.join('dir1', 'dir2')
        os.makedirs(nested_dirs)
        
        destination = os.path.join(nested_dirs, renamed_file)
        shutil.move(renamed_file, destination)
        
        self.assertTrue(os.path.exists(destination))
        self.assertFalse(os.path.exists(renamed_file))

    def test_directory_operations(self):
        """Тест операций с директориями."""
        # Создаем пустую директорию и удаляем
        empty_dir = 'empty_dir'
        os.makedirs(empty_dir)
        self.assertTrue(os.path.exists(empty_dir))
        os.rmdir(empty_dir)
        self.assertFalse(os.path.exists(empty_dir))
        
        # Создаем вложенные директории
        nested_dir = os.path.join('deep', 'nested', 'dir')
        os.makedirs(nested_dir)
        self.assertTrue(os.path.exists(nested_dir))

    def test_directory_listing(self):
        """Тест вывода содержимого директорий."""
        # Создаем тестовые файлы и директории
        os.makedirs('test_dir')
        with open(os.path.join('test_dir', 'test_file.txt'), 'w') as f:
            f.write("Тестовый файл\n")
        
        # Проверяем содержимое основной директории
        items = os.listdir('.')
        self.assertIn('test_dir', items)
        self.assertIn(self.original_file, items)
        
        # Проверяем содержимое вложенной директории
        os.chdir('test_dir')
        items = os.listdir('.')
        self.assertIn('test_file.txt', items)
        os.chdir('..')

    def test_directory_walk(self):
        """Тест рекурсивного обхода директорий."""
        # Создаем тестовую структуру
        os.makedirs(os.path.join('parent', 'child'))
        with open(os.path.join('parent', 'file1.txt'), 'w') as f:
            f.write("Файл 1\n")
        with open(os.path.join('parent', 'child', 'file2.txt'), 'w') as f:
            f.write("Файл 2\n")
        
        # Собираем информацию об обходе
        walk_data = []
        for root, dirs, files in os.walk('.'):
            walk_data.append((root, sorted(dirs), sorted(files)))
        
        expected = [
            ('.', ['parent'], [self.original_file]),
            (os.path.join('.', 'parent'), ['child'], ['file1.txt']),
            (os.path.join('.', 'parent', 'child'), [], ['file2.txt'])
        ]
        
        self.assertEqual(walk_data, expected)

if __name__ == '__main__':
    unittest.main()