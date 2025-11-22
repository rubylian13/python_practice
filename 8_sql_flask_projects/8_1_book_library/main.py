from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import sqlite3

app = Flask(__name__)
Bootstrap(app)

all_books = [
    {
        "title": "nice book",
        "author": "somebody",
        "rating": 3
    }
]


def get_db_connection():
    conn = sqlite3.connect('books-collection.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    books = all_books
    return render_template("index.html", books=books)


# init the table
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS books ("
                   "id INTEGER PRIMARY KEY, "
                   "title varchar(250) NOT NULL UNIQUE, "
                   "author varchar(250) NOT NULL, "
                   "rating FLOAT NOT NULL)")
    cursor.close()
    conn.close()
except sqlite3.Error as err:
    print("Error creating table:", err)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get('title')
        author = request.form.get('author')
        rating = request.form.get('rating')

        # update the table
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO books (title, author, rating) VALUES (?, ?, ?)"
        cursor.execute(sql, (title, author, rating))
        cursor.execute(f"INSERT INTO books VALUES(1, '{title}', '{author}', '{rating}')")
        conn.commit()

        cursor.close()
        conn.close()

        return render_template('success.html')
    else:
        return render_template('add.html')


@app.route('/success')
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)