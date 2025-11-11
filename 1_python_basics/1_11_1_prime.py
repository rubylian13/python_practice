def is_prime(num):
    if num == 2:
        return True
    if num == 1:
        return False

    for i in range(2, num):
        # Check if the number (num) can be divided by the potential prime number
        if num % i == 0:
            return False
    return True

number = int(input("Enter a number: "))
print(is_prime(number))