class _calc:
    """Class _calc so it can be imported into other python files...."""

    def add(self, first_number, second_number):
        """
        Function to add two numbers.
        Take value from variables first_number and second_number.
        """
        return first_number + second_number

    def sub(self, first_number, second_number):
        """
        Function to substract one number from another.
        Take value from variables first_number and second_number.
        """
        return first_number - second_number

    def mltpl(self, first_number, second_number):
        """
        Function to multiply two numbers.
        Take value from variables first_number and second_number.
        """
        return first_number * second_number

    def div(self, first_number, second_number):
        """
        Function to divide one number by another.
        Take value from variables first_number and second_number.
        """
        try:
            return first_number / second_number
        except ZeroDivisionError:
            return "You can't divide by zero"


def main():
    """
    Main function.
    Takes two variables, operation and print calculations to terminal.
    Also creates exemple variable.
    """
    calculator = _calc()
    while True:
        first_number = float(input("Enter first number: "))
        second_number = float(input("Enter second number: "))
        choice = input("Choose operation(+, -, *, /): ")
        match (choice):
            case "+":
                print(calculator.add(first_number, second_number))
            case "-":
                print(calculator.sub(first_number, second_number))
            case "*":
                print(calculator.mltpl(first_number, second_number))
            case "/":
                print(calculator.div(first_number, second_number))


if __name__ == "__main__":
    main()
