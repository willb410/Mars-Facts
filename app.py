import os

from flask import Flask, redirect, render_template
from flask_pymongo import PyMongo

import scrape_mars

# Set the file path to run Flask app
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_app')

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()

    # Return template and data
    try: 
        return render_template("index.html", news_title = destination_data['news_title'], 
                                         news_p = destination_data['news_p'], 
                                         featured_image = destination_data['featured_image'], 
                                         mars_tweet = destination_data['mars_tweet'], 
                                         hemisphere_image_urls = destination_data['hemisphere_image_urls'], )
    except: 
        return redirect("/scrape")

    
# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)