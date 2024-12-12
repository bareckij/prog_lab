from src.lab4.ClassOrder import Order

def process_orders(input_file, output_valid_file, output_invalid_file):
    orders = []
    invalid_orders = []
    
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(';')
            if len(parts) != 6:
                continue  
            order_number, products_str, customer_name, delivery_address, phone_number, delivery_priority = parts
            products = products_str.split(', ')
            
            order = Order(order_number, products, customer_name, delivery_address, phone_number, delivery_priority)
            
            errors = order.validate()
            if errors:
                for error in errors:
                    invalid_orders.append(f"{order.order_number};{error[0]};{error[1]}")
            else:
                orders.append(order)
    
    orders.sort(key=lambda x: (x.get_country(), {'MAX': 1, 'MIDDLE': 2, 'LOW': 3}[x.delivery_priority]))
    
    with open(output_valid_file, 'w', encoding='utf-8') as file:
        for order in orders:
            file.write(str(order) + "\n")
    
    with open(output_invalid_file, 'w', encoding='utf-8') as file:
        for error in invalid_orders:
            file.write(error + "\n")


if __name__ == '__main__':
    process_orders()
