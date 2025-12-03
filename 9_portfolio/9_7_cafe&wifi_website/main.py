"""
Build a website that lists cafes with wifi and power for remote working.
"""
from flask import Flask, render_template
from data_manager import DataManager

app = Flask(__name__)
data_manager = DataManager()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cafe/<city_name>", methods=['GET'])
def cafe(city_name=None):
    cafes_list = data_manager.get_info(city_name)
    return render_template("cafe.html", city_name=city_name, cafes=cafes_list)

if __name__ == "__main__":
  app.run(debug=True)