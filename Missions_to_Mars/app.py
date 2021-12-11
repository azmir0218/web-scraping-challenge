from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
# Pass connection to the pymongo instance.
mongo = PyMongo(app)


# Route to render index.html template using data from Mongo


@app.route("/")
def index():

    # Find one record of data from the mongo database

    everything_dict = mongo.db.everything_dict.find_one()

    # Return template and data
    return render_template("index.html", mars_info=everything_dict)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    everything_dict = mongo.db.everything_dict
    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    everything_dict.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
