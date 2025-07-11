from flask import Flask, render_template, request
from feature_extraction import FeatureExtraction
import numpy as np
import re
import joblib
import requests

app = Flask(__name__)

# Load your machine learning model
gbc = joblib.load('model.pkl')

def get_full_url(url):
    try:
        response = requests.get(url, allow_redirects=True)
        return response.url
    except Exception as e:
        return None

@app.route("/")
def home():
    return render_template("index.html", result=None)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["POST"])
def login():
    # Get the URL entered by the user
    url = request.form['url']

    # Validate if the input resembles a URL
    if not re.match(r'^https?://(?:www\.)?[\w\.-]+(?:\.[a-zA-Z]+)+(/[^\s]*)?$', url):
        return render_template("index.html", result="There isn't any URL in text")



    # Get the full URL
    full_url = get_full_url(url)
    if full_url is None:
        # If unable to fetch full URL, use the provided URL
        full_url = url

    # Instantiate FeatureExtraction class
    feature_extractor = FeatureExtraction(full_url)
    
    # Perform feature extraction on the URL
    features = feature_extractor.getFeaturesList()
    
    # Convert features to a NumPy array
    features_array = np.array(features)
    
    # Make prediction using the loaded model
    prediction = gbc.predict(features_array.reshape(1, -1))[0]
    
    # Determine the result based on the prediction
    result = "Safe URL" if prediction == 1 else "Phishing URL"
    
    # Render the template with the result
    return render_template("index.html", result=result, url=full_url)




if __name__ == "__main__":
    app.run(debug=True)







