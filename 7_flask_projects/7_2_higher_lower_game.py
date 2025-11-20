from flask import Flask
import random

app = Flask(__name__)


@app.route('/')
def main_page():
    return '<h1>Guess a number between 0 and 9. </h1><br>' \
           '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif">'


# converter: https://flask.palletsprojects.com/en/2.3.x/quickstart/#variable-rules
@app.route("/<int:num>")
def guessing_num(num):
    selected_num = random.randint(1, 9)
    input_num = num
    print(f"{num}, {selected_num}")
    if input_num > selected_num:
        return f"<h1>You guessed {input_num}, but the number is lower.</h1> <img " \
               f"src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'>"
    elif input_num < selected_num:
        return f"<h1>You guessed {input_num}, but the number is higher.</h1><img " \
               f"src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'>"
    else:
        return f"<h1>You guessed {input_num}, and it's correct!</h1><img " \
               f"src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'>"


if __name__ == "__main__":
    app.run(debug=True)