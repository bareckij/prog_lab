import re

class Order:
    def __init__(self, order_number, products, customer_name, delivery_address, phone_number, delivery_priority):
        self.order_number = order_number
        self.products = products
        self.customer_name = customer_name
        self.delivery_address = delivery_address
        self.phone_number = phone_number
        self.delivery_priority = delivery_priority

    def validate_address(self):
        """Проверка правильности адреса."""
        if not self.delivery_address:
            return (1, "no data")
        
        parts = self.delivery_address.split('.')
        if len(parts) != 4:
            return (1, self.delivery_address)
        
        return None

    def validate_phone(self):
        """Проверка правильности номера телефона по шаблону +x-xxx-xxx-xx-xx."""
        if not self.phone_number:
            return (2, "no data")
        
        phone_pattern = r"^\+(\d)-(\d{3})-(\d{3})-(\d{2})-(\d{2})$"
        if not re.match(phone_pattern, self.phone_number):
            return (2, self.phone_number)
        
        return None

    def validate(self):
        """Проверка заказа на ошибки."""
        errors = []
        
        address_error = self.validate_address()
        if address_error:
            errors.append(address_error)
        
        phone_error = self.validate_phone()
        if phone_error:
            errors.append(phone_error)
        
        return errors

    def get_country(self):
        """Извлекаем страну из адреса для сортировки."""
        if self.delivery_address:
            return self.delivery_address.split('.')[0].strip()
        return ""

    def __str__(self):
        """Возвращает строку для сохранения в файл order_country.txt."""
        products_str = ', '.join([f"{item.split()[0]} x{item.split()[1]}" if len(item.split()) > 1 else item for item in self.products])
        region_city_street = self.delivery_address.split('.', 3)[1:]  
        address_str = '. '.join(region_city_street).strip()
        return f"{self.order_number};{products_str};{self.customer_name};{address_str};{self.phone_number};{self.delivery_priority}"
    