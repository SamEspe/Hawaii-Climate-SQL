# Import dependencies
from flask import Flask

# Create app
app = Flask(__name__)

# Routes

# Homepage
@app.route('/')
def homepage():
    print("Homepage requested")
    return("Welcome to Sam's Climate App. <br/> Here are the available routes: <br/>")

# Precipitation

# Stations

# Temperature Observations

# Temperature - all dates after "start"

# Temperature - date range

# Run Flask server
if __name__ == "__main__":
    app.run(debug=True)
