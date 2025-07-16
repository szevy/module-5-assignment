from flask import Flask, render_template, request
import joblib
from groq import Groq

import os

from openai import OpenAI
#https://console.groq.com/keys
SEALION_API_KEY = os.environ.get("SEALION_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    q = request.form.get("q")
    # db
    return(render_template("main.html"))

@app.route("/llama",methods=["GET","POST"])
def llama():
    return(render_template("llama.html"))

@app.route("/llama_reply",methods=["GET","POST"])
def llama_reply():
    q = request.form.get("q")
    # load model
    client = Groq()
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": q
            }
        ]
    )
    return(render_template("llama_reply.html",r=completion.choices[0].message.content))

@app.route("/deepseek",methods=["GET","POST"])
def deepseek():
    return(render_template("deepseek.html"))

@app.route("/deepseek_reply",methods=["GET","POST"])
def deepseek_reply():
    q = request.form.get("q")
    # load model
    client = Groq()
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
        {
            "role": "user",
            "content": q
        }
        ]
    )
    return(render_template("deepseek_reply.html",r=completion.choices[0].message.content))


@app.route("/sealion", methods=["GET"]) # Route for the initial form page
def sealion():
    return render_template("sealion.html")

# Route to handle the form submission and display the reply
@app.route("/sealion_reply", methods=["POST"])
def sealion_reply(): # This is now the view function directly for the route
    print(">>> METHOD:", request.method)
    print(">>> FORM DATA:", request.form)
    q = request.form.get("q")
    # load model
    client = OpenAI(
        api_key=os.environ['SEALION_API_KEY'],
        base_url="https://api.sea-lion.ai/v1"
    )
    completion = client.chat.completions.create(
        model="aisingapore/Gemma-SEA-LION-v3-9B-IT",
        messages=[
        {
            "role": "user",
            "content":q
        }
        ]
    )
    return(render_template("sealion_reply.html",r=completion.choices[0].message.content))

@app.route("/dbs",methods=["GET","POST"])
def dbs():
    return(render_template("dbs.html"))

@app.route("/prediction",methods=["GET","POST"])
def prediction():
    q = float(request.form.get("q"))
    # load model
    model = joblib.load("dbs.jl")
    # make prediction
    pred = model.predict([[q]])
    return(render_template("prediction.html",r=pred))


@app.route("/telegram",methods=["GET","POST"])
def telegram():
    domain_url = "https://module-5-dbs-241223.onrender.com"
    
    # The following line is used to delete the existing webhook URL for the Telegram bot
    delete_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
    requests.post(delete_webhook_url, json={"url": domain_url, "drop_pending_updates": True})

    # Set the webhook URL for the Telegram bot
    set_webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={domain_url}/webhook"
    webhook_response = requests.post(set_webhook_url, json={"url": domain_url, "drop_pending_updates": True})

    if webhook_response.status_code == 200:
        # set status message
        status = "The telegram bot is running. Please check with the telegram bot. @your_bot"
    else:
        status = "Failed to start the telegram bot. Please check the logs."
    
    return(render_template("telegram.html", status=status))


if __name__ == "__main__":
    app.run()