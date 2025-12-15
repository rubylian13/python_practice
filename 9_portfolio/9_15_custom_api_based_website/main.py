"""
Build a custom website using an API that you find interesting.
"""
from flask import Flask, render_template, request
from data_manager import DataManager

app = Flask(__name__)
data_manager = DataManager()

@app.route("/")
def home():
    brewery_data = data_manager.get_data()
    return render_template("index.html", breweries=brewery_data)

@app.route("/search")
def search_breweries():
    field = request.args.get("field")
    query = request.args.get("query")
    search_data = data_manager.search_breweries_by_value(field, query)
    return render_template("index.html", breweries=search_data)

if __name__ == "__main__":
  app.run(debug=True)