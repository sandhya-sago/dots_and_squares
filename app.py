import sys
import os
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__), 'dots_and_squares')))
from flask import Flask, render_template
from dots_and_squares import dots_and_squares


# create instance of Flask app
app = Flask(__name__)

# create route that renders index.html template
@app.route("/")
@app.route("/game")
def index():
    render_template("index.html")
    dots_and_squares.main()
    return "Great Game"
    # return render_template("index.html", mars=mars_info[0])

if __name__ == "__main__":
    app.run(debug=True)