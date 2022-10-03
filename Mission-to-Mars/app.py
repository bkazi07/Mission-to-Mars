{
  "metadata": {
    "language_info": {
      "codemirror_mode": {
        "name": "python",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.8"
    },
    "kernelspec": {
      "name": "python",
      "display_name": "Python (Pyodide)",
      "language": "python"
    }
  },
  "nbformat_minor": 4,
  "nbformat": 4,
  "cells": [
    {
      "cell_type": "code",
      "source": "# Import dependencies\nfrom flask import Flask, render_template, redirect, url_for\nfrom flask_pymongo import PyMongo\nimport Scraping\n\n# Setting up Flask\napp = Flask(__name__)\n\n# Use flask_pymongo to set up mongo connection\n\napp.config[\"MONGO_URI\"] = \"mongodb://localhost:27017/mars_app\"\nmongo = PyMongo(app)\n\n# Determine route for HTML page\n\n@app.route(\"/\")\ndef index():\n    mars = mongo.db.mars.find_one()\n    return render_template(\"index.html\", mars = mars)\n\n@app.route(\"/scrape\")\ndef scrape():\n    mars = mongo.db.mars\n    mars_data = scraping.scrape_all()\n    mars.update({}, mars_data, upsert=True)\n    return redirect('/', code=302)\n\nif __name__ == \"__main__\":\n    app.run()\n\n",
      "metadata": {},
      "execution_count": null,
      "outputs": []
    }
  ]
}