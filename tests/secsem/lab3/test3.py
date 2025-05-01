import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import psutil
import platform
from io import StringIO
import tempfile
import shutil

from  src.secsem.lab3.task3 import (
    clear_screen,
    show_menu,
    get_user_choice,
    show_processes,
    show_process_details,
    terminate_process,
    manage_environment_variables,
    change_process_priority,
    show_system_info,
    main
)

class TestSystemMonitor(unittest.TestCase):

    def setUp(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.original_environ = os.environ.copy()
        
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        
        os.environ = self.original_environ.copy()
        
        shutil.rmtree(self.test_dir)

    @patch('os.system')
    def test_clear_screen_windows(self, mock_system):
        with patch('os.name', 'nt'):
            clear_screen()
            mock_system.assert_called_with('cls')

    @patch('os.system')
    def test_clear_screen_unix(self, mock_system):
        with patch('os.name', 'posix'):
            clear_screen()
            mock_system.assert_called_with('clear')

    def test_show_menu(self):
        show_menu()
        output = sys.stdout.getvalue()
        self.assertIn("Системный монитор и менеджер процессов", output)
        self.assertIn("a) Список всех запущенных процессов", output)
        self.assertIn("g) Выход", output)


    @patch('psutil.process_iter')
    def test_show_processes(self, mock_process_iter):
        mock_proc1 = MagicMock()
        mock_proc1.info = {
            'pid': 1234,
            'name': 'python.exe',
            'username': 'DOMAIN\\user1',
            'status': 'running'
        }
        
        mock_proc2 = MagicMock()
        mock_proc2.info = {
            'pid': 5678,
            'name': 'chrome.exe',
            'username': None,
            'status': 'sleeping'
        }
        
        mock_process_iter.return_value = [mock_proc1, mock_proc2]
        
        show_processes()
        output = sys.stdout.getvalue()
        
        self.assertIn("Список запущенных процессов", output)
        self.assertIn("1234", output)
        self.assertIn("python.exe", output)
        self.assertIn("user1", output)
        self.assertIn("N/A", output)

    @patch('psutil.Process')
    def test_show_process_details_success(self, mock_process):
        mock_proc = MagicMock()
        mock_proc.name.return_value = "python.exe"
        mock_proc.status.return_value = "running"
        mock_proc.username.return_value = "user1"
        mock_proc.create_time.return_value = 1234567890
        mock_proc.cpu_percent.return_value = 12.5
        mock_proc.memory_info.return_value.rss = 1024 * 1024 * 10  
        mock_proc.exe.return_value = "/usr/bin/python"
        mock_proc.cwd.return_value = "/home/user"
        mock_proc.cmdline.return_value = ["python", "script.py"]
        
        mock_process.return_value = mock_proc
        
        with patch('builtins.input', return_value='1234'):
            show_process_details()
            output = sys.stdout.getvalue()
            
            self.assertIn("Детальная информация о процессе PID: 1234", output)
            self.assertIn("Имя: python.exe", output)
            self.assertIn("Использует памяти: 10.00 MB", output)


    @patch('psutil.Process')
    def test_terminate_process_success(self, mock_process):
        mock_proc = MagicMock()
        mock_process.return_value = mock_proc
        
        with patch('builtins.input', side_effect=['1234', 'y']):
            terminate_process()
            mock_proc.terminate.assert_called_once()
            output = sys.stdout.getvalue()
            self.assertIn("был отправлен сигнал на завершение", output)

    @patch('psutil.Process')
    def test_terminate_process_cancel(self, mock_process):
        mock_proc = MagicMock()
        mock_process.return_value = mock_proc
        
        with patch('builtins.input', side_effect=['1234', 'n']):
            terminate_process()
            mock_proc.terminate.assert_not_called()

    def test_manage_environment_variables_show(self):
        os.environ['TEST_VAR'] = 'test_value'
        
        with patch('builtins.input', side_effect=['1', '3']):
            manage_environment_variables()
            output = sys.stdout.getvalue()
            self.assertIn("TEST_VAR=test_value", output)

    def test_manage_environment_variables_set(self):
        with patch('builtins.input', side_effect=['2', 'NEW_VAR', 'new_value', '3']):
            manage_environment_variables()
            self.assertEqual(os.environ['NEW_VAR'], 'new_value')
            output = sys.stdout.getvalue()
            self.assertIn("Переменная NEW_VAR установлена в new_value", output)

    @patch('psutil.Process')
    def test_change_process_priority_success(self, mock_process):
        mock_proc = MagicMock()
        mock_proc.nice.return_value = 0
        mock_process.return_value = mock_proc
        
        with patch('builtins.input', side_effect=['1234', '5']):
            change_process_priority()
            mock_proc.nice.assert_called_with(5)
            output = sys.stdout.getvalue()
            self.assertIn("Приоритет процесса 1234 изменен на 5", output)


    @patch('platform.system')
    @patch('platform.release')
    @patch('platform.version')
    @patch('platform.machine')
    @patch('platform.processor')
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    def test_show_system_info(self, mock_disk, mock_mem, mock_processor, 
                            mock_machine, mock_version, mock_release, mock_system):
        mock_system.return_value = "Linux"
        mock_release.return_value = "5.4.0"
        mock_version.return_value = "#1 SMP Debian"
        mock_machine.return_value = "x86_64"
        mock_processor.return_value = "Intel(R) Core(TM) i7-8650U"
        
        mem_info = MagicMock()
        mem_info.total = 1024 * 1024 * 16  
        mem_info.used = 1024 * 1024 * 8    
        mem_info.free = 1024 * 1024 * 8    
        mem_info.percent = 50.0
        mock_mem.return_value = mem_info
        
        disk_info = MagicMock()
        disk_info.total = 1024 * 1024 * 1024 * 100  
        disk_info.used = 1024 * 1024 * 1024 * 40     
        disk_info.free = 1024 * 1024 * 1024 * 60     
        disk_info.percent = 40.0
        mock_disk.return_value = disk_info
        
        show_system_info()
        output = sys.stdout.getvalue()
        
        self.assertIn("Информация о системе", output)
        self.assertIn("ОС: Linux 5.4.0", output)
        self.assertIn("Всего: 16.00 MB", output)
        self.assertIn("Использовано: 8.00 MB", output)
        self.assertIn("Всего: 100.00 GB", output)


if __name__ == '__main__':
    unittest.main()