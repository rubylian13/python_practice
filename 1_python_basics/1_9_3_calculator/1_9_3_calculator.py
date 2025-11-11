import calculator_art


def add(n1, n2):
    return n1 + n2


def subtract(n1, n2):
    return n1 - n2


def multiply(n1, n2):
    return n1 * n2


def divide(n1, n2):
    return n1 / n2


operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide
}


def calculator():
    print(calculator_art.logo)
    should_accumulate = True
    number1 = float(input("What is the first number?: "))

    while should_accumulate:
        for symbol in operations:
            print(symbol)
        operation_symbol = input("Pick an Operation: ")
        number2 = float(input("What is the next number?: "))
        answer = operations[operation_symbol](number1, number2)
        print(f"{number1} {operation_symbol} {number2} = {answer}")

        choice = input(
            f"Type 'y' to continue calculating with {answer}, or type 'n' to start a new calculation: ").lower()
        if choice == "y":
            number1 = answer
        else:
            should_accumulate = False
            print("\n" * 50)
            calculator()


calculator()