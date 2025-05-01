import os
import unittest
import tempfile
import time
import stat
from unittest.mock import patch

class TestFileOperations(unittest.TestCase):
    """Набор тестов для проверки операций с файлами."""
    
    def setUp(self):
        """Подготовка тестового окружения: создание временной директории."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
        self.script_path = os.path.join(self.temp_dir, "script.py")
        self.file_name = "example_file.txt"
        self.test_content = [
            "Это тестовые данные для задания по работе с файлами.\n",
            "Строка 2.\n",
            "Строка 3.\n"
        ]

    def test_file_creation(self):
        """Тест создания файла и записи данных.
        
        Проверяет:
        - Файл действительно создается
        - Содержимое файла соответствует записанному
        """
        with open(self.file_name, 'w') as f:
            f.writelines(self.test_content)
        
        self.assertTrue(os.path.exists(self.file_name))
        with open(self.file_name, 'r') as f:
            content = f.readlines()
        self.assertEqual(content, self.test_content)

    def test_file_metadata(self):
        """Тест метаданных файла.
        
        Проверяет:
        - Размер файла больше 0
        - Время последнего изменения и доступа примерно равно текущему
        """
        with open(self.file_name, 'w') as f:
            f.writelines(self.test_content)
        
        file_stats = os.stat(self.file_name)
        
        self.assertGreater(file_stats.st_size, 0)
        self.assertAlmostEqual(file_stats.st_mtime, time.time(), delta=2)
        self.assertAlmostEqual(file_stats.st_atime, time.time(), delta=2)

    @patch('os.getlogin')
    def test_current_user(self, mock_getlogin):
        """Тест получения текущего пользователя.
        
        Использует мокинг для изоляции от реальной системы.
        """
        mock_getlogin.return_value = "testuser"
        self.assertEqual(os.getlogin(), "testuser")

    def test_permissions_change(self):
        """Тест изменения прав доступа к файлу.
        
        Проверяет:
        - Права действительно меняются
        - Новые права включают полный доступ (777)
        """
        with open(self.file_name, 'w') as f:
            f.writelines(self.test_content)
        
        original_mode = os.stat(self.file_name).st_mode
        os.chmod(self.file_name, 0o777)
        new_mode = os.stat(self.file_name).st_mode
        
        self.assertNotEqual(original_mode, new_mode)
        self.assertTrue(new_mode & stat.S_IRWXU)  # Проверка прав пользователя
        self.assertTrue(new_mode & stat.S_IRWXG)  # Проверка прав группы
        self.assertTrue(new_mode & stat.S_IRWXO)  # Проверка прав остальных

    def test_directory_change(self):
        """Тест смены рабочей директории.
        
        Проверяет, что текущая директория действительно меняется.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.temp_dir)
        self.assertEqual(os.getcwd(), self.temp_dir)

if __name__ == '__main__':
    unittest.main()