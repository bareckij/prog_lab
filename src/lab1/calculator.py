class calc: 
    def add(self, a, b):
        return (a + b)
    def sub(self, a, b): 
        return (a - b)   
    def mltpl(self, a, b):
        return (a * b) 
    def div(self, a, b):
        try: 
            return (a/b)
        except ZeroDivisionError:
            return "You can't divide by zero"

def main():
    calculator = calc()
    while True:
        a = float(input('Enter first number: '))
        b = float(input('Enter second number: '))
        choice = input('Choose operation(+, -, *, /): ')
        match(choice):
            case '+':
                print(calculator.add(a, b))
            case '-':
                print(calculator.sub(a, b))
            case '*':
                print(calculator.mltpl(a, b))
            case '/':
                print(calculator.div(a, b))
if __name__ == "__main__":
    main()