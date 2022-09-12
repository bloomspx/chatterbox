from flask import Flask, render_template, request, redirect
from transformers import pipeline
from html_to_csv import extract_content
from bs4 import BeautifulSoup
import pandas as pd
import requests, os, time, sys

app = Flask(__name__)

model = "siebert/sentiment-roberta-large-english"
nlp = pipeline("sentiment-analysis", model=model, tokenizer=model)

def get_prediction(texts, model):
    new_df = pd.DataFrame(columns=["Content","Label", "Score"])

    for index in range(len(texts)):
        preds = model(texts[index])
        print(preds)
        pred_sentiment = preds[0]["label"]
        pred_score = preds[0]["score"]

        # write data into df
        new_df.at[index, "Label"] = pred_sentiment
        new_df.at[index, "Score"] = pred_score
        # write text
        new_df.at[index, "Content"] = "".join((texts[index]))

    new_df.to_csv("data/results.csv", index=False)
    results = new_df
    return results

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/convert', methods=['GET'])
def render_convert():
    return render_template("convert.html")

@app.route('/convert', methods=['POST'])
def convert():
    try:
        url = request.form.get('url')
        print(url)
        page=requests.get(url) 
    except Exception as e:    
        error_type, error_info = sys.exc_info()      
        print ('ERROR FOR LINK:',url)                     
        print (error_type, 'Line:', error_info.tb_lineno)

    time.sleep(4)
    soup = BeautifulSoup(page.text, "html.parser")

    ## extract article content
    textContent = soup.find_all('div', attrs={'class':'text'})
    print(textContent)
    paragraphs = []

    for i in textContent:
        para = i.find_all('p')
        for j in para:
            content = j.getText().strip()
            paragraphs.append(content)

    df = pd.DataFrame(paragraphs)
    df.to_csv("data/news.csv", index=False)
    data = pd.read_csv("data/news.csv")
    texts = data.values.tolist()
    message = ""
    for i in texts:
        message += "".join(i)
    results = get_prediction(texts, nlp)

    return render_template('result.html', text = message, prediction = results)


@app.route('/predict', methods=['GET'])
def render_predict():
    return render_template("predict.html")


@app.route('/predict', methods=['POST'])
def predict():
    file_data = request.files['file']
    filename = file_data.filename
    ## save file locally
    if filename != "":
        file_data.save(os.path.join('data', filename))
    data = pd.read_csv('data/{}'.format(filename))
    texts = data.values.tolist()
    message = ""
    for i in texts:
        message += "".join(i)
    results = get_prediction(texts, nlp)

    return render_template('result.html', text = message, prediction = results)

if __name__ == '__main__':
    app.run(debug=True)