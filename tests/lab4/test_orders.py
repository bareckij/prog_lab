
import unittest


from src.lab4.ClassOrder import Order
class TestOrderProcessing(unittest.TestCase):

    def test_validate_address_valid(self):
        order = Order("12345", ["Яблоки", "Макароны"], "Иванов Иван", "Россия. Москва. Москва. Тверская", "+7-912-345-67-89", "MAX")
        self.assertIsNone(order.validate_address())

    def test_validate_address_invalid(self):
        # Ошибка в адресе (недостаточно частей)
        order = Order("12345", ["Яблоки", "Макароны"], "Иванов Иван", "Россия. Москва", "+7-912-345-67-89", "MAX")
        self.assertEqual(order.validate_address(), (1, "Россия. Москва"))

        # Адрес пустой
        order = Order("12345", ["Яблоки", "Макароны"], "Иванов Иван", "", "+7-912-345-67-89", "MAX")
        self.assertEqual(order.validate_address(), (1, "no data"))

    def test_validate_phone_valid(self):
        order = Order("12345", ["Яблоки", "Макароны"], "Иванов Иван", "Россия. Москва. Москва. Тверская", "+7-912-345-67-89", "MAX")
        self.assertIsNone(order.validate_phone())

    def test_validate_phone_invalid(self):
        # Невалидный номер
        order = Order("12345", ["Яблоки", "Макароны"], "Иванов Иван", "Россия. Москва. Москва. Тверская", "79123456789", "MAX")
        self.assertEqual(order.validate_phone(), (2, "79123456789"))

        # Пустой номер
        order = Order("12345", ["Яблоки", "Макароны"], "Иванов Иван", "Россия. Москва. Москва. Тверская", "", "MAX")
        self.assertEqual(order.validate_phone(), (2, "no data"))

    def test_validate_multiple_errors(self):
        # Ошибка в адресе и телефоне
        order = Order("12345", ["Яблоки", "Макароны"], "Иванов Иван", "", "79123456789", "MAX")
        errors = order.validate()
        self.assertEqual(len(errors), 2)
        self.assertIn((1, "no data"), errors)
        self.assertIn((2, "79123456789"), errors)

    def test_get_country(self):
        order = Order("12345", ["Яблоки", "Макароны"], "Иванов Иван", "Россия. Москва. Москва. Тверская", "+7-912-345-67-89", "MAX")
        self.assertEqual(order.get_country(), "Россия")

        order = Order("12345", ["Яблоки", "Макароны"], "Иванов Иван", "Италия. Рим. Рим. Колизей", "+39-061-234-56-78", "MIDDLE")
        self.assertEqual(order.get_country(), "Италия")

    def test_order_str(self):
        order = Order("12345", ["Яблоки", "Макароны"], "Иванов Иван", "Россия. Москва. Москва. Тверская", "+7-912-345-67-89", "MAX")
        self.assertEqual(str(order), "12345;Яблоки, Макароны;Иванов Иван;Москва.  Москва.  Тверская;+7-912-345-67-89;MAX")



if __name__ == "__main__":
    unittest.main()
