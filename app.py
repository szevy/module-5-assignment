# Flask Application - The Backend Logic
# This is the heart of the web application
from flask import Flask,render_template,request
import joblib

app = Flask(__name__)

# uses the Flask framework to define web routes - "/" for the main page
@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))   # renders HTML template "index.html" --> Frontend - Input Form

# uses the Flask framework to define web routes - "/prediction" for handling the prediction request
@app.route("/prediction",methods=["GET","POST"])
def prediction():
    q = float(request.form.get("q"))

    # load model
    model = joblib.load("dbs.jl")

    # make prediction
    pred = model.predict([[q]])

    return(render_template("prediction.html",r=pred)
    # return(render_template("prediction.html", r=(-50.6*q)+90.2))    # # renders HTML template "prediction.html" --> # Frontend - Output Display

if __name__ == "__main__":
    app.run()