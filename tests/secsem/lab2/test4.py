import unittest
from unittest.mock import patch, MagicMock
import time
import requests
from src.secsem.lab2.task4 import fetch_sync, main_sync  

class TestFetchSync(unittest.TestCase):
    """Тесты для функции fetch_sync"""
    
    @patch('requests.get')
    def test_fetch_sync_returns_correct_format(self, mock_get):
        """Тестирует формат возвращаемой строки"""
        # Настраиваем мок для requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Фиксируем время для предсказуемых результатов
        with patch('time.time', side_effect=[0, 1.5]):
            result = fetch_sync("https://example.com")
            
            self.assertEqual(result, "https://example.com | Status: 200 | Time: 1.50s")
    
    @patch('requests.get')
    def test_fetch_sync_with_different_status(self, mock_get):
        """Тестирует функцию с разными статус-кодами"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with patch('time.time', side_effect=[0, 0.5]):
            result = fetch_sync("https://example.com/not-found")
            
            self.assertEqual(result, "https://example.com/not-found | Status: 404 | Time: 0.50s")

class TestMainSync(unittest.TestCase):
    """Тесты для функции main_sync"""
    
    @patch('src.secsem.lab2.task4.fetch_sync')  # Замените your_module на имя вашего модуля
    @patch('builtins.print')
    def test_main_sync_calls_fetch_for_each_url(self, mock_print, mock_fetch):
        """Тестирует что main_sync вызывает fetch_sync для каждого URL"""
        # Настраиваем мок для fetch_sync
        mock_fetch.side_effect = [
            "https://google.com | Status: 200 | Time: 0.30s",
            "https://youtube.com | Status: 200 | Time: 1.20s",
            "https://reddit.com | Status: 200 | Time: 2.50s",
        ]
        
        # Фиксируем общее время
        with patch('time.time', side_effect=[0, 5.0]):
            main_sync()
            
            # Проверяем что fetch_sync вызывался для каждого URL
            self.assertEqual(mock_fetch.call_count, 3)
            
            # Проверяем вывод
            expected_calls = [
                unittest.mock.call("https://google.com | Status: 200 | Time: 0.30s"),
                unittest.mock.call("https://youtube.com | Status: 200 | Time: 1.20s"),
                unittest.mock.call("https://reddit.com | Status: 200 | Time: 2.50s"),
                unittest.mock.call("\nTotal time (sync): 5.00s"),
            ]
            mock_print.assert_has_calls(expected_calls, any_order=False)
    
    @patch('src.secsem.lab2.task4.fetch_sync')  # Замените your_module на имя вашего модуля
    @patch('requests.get')
    def test_main_sync_with_real_fetch(self, mock_get, mock_fetch):
        """Тестирует интеграцию main_sync с fetch_sync"""
        # Настраиваем моки для requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Фиксируем время для каждого вызова fetch_sync
        time_side_effect = [
            0, 0.3,    # google.com
            0.3, 1.5,  # youtube.com
            1.5, 4.0,  # reddit.com
            0, 4.0     # Общее время (start_total и total_time)
        ]
        
        with patch('time.time', side_effect=time_side_effect):
            main_sync()
            
            # Проверяем что requests.get вызывался для каждого URL
            expected_urls = []
            actual_urls = [call[0][0] for call in mock_get.call_args_list]
            self.assertEqual(actual_urls, expected_urls)

if __name__ == '__main__':
    unittest.main()