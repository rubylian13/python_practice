import time

def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)
        function()
        function()
    return wrapper_function

@delay_decorator
def say_hello():
    print("Hello")

#With the @ syntactic sugar
@delay_decorator
def say_bye():
    print("Bye")

#Without the @ syntactic sugar
def say_greeting():
    print("Hiii How are you?")
decorated_function = delay_decorator(say_greeting)
decorated_function()