from flask import Flask, render_template

# api => https://api.npoint.io/47e30f462824b47fc0cf
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)