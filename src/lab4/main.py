from src.lab4.process_orders import process_orders


if __name__ == '__main__':
    input_file = 'src/lab4/textf/orders.txt'
    output_valid_file = 'src/lab4/textf/order_country.txt'
    output_invalid_file = 'src/lab4/textf/non_valid_orders.txt'
    process_orders(input_file, output_valid_file, output_invalid_file)

