from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pickle
import json
import re
import os
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

ps = PorterStemmer()
tfidf = TfidfVectorizer()

app = Flask(__name__, static_folder='client/build', static_url_path='')
CORS(app)

spamMail = pickle.load(open('spamMail.pkl','rb'))

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/api",methods=["POST"])
@cross_origin()
def spam():
    
    def stemming(content):
        stemmed_content = re.sub('[^a-zA-Z]',' ',content)
        stemmed_content = stemmed_content.lower()
        stemmed_content = stemmed_content.split()
        stemmed_content = [ps.stem(words) for words in stemmed_content if not words in stopwords.words('english')]
        stemmed_content = ' '.join(stemmed_content)
        return stemmed_content


    df = pd.read_csv('spam.csv')
    df['spam'] = pd.get_dummies(df['Category'],drop_first=True)
    df = df.drop(['Category'], axis=1)
    df['Message'] = df['Message'].apply(stemming)
    Z = tfidf.fit_transform(df['Message'])
    y = df['spam']
    Z_train, Z_test, y_train, y_test = train_test_split(Z, y, test_size=0.2)
    model = LogisticRegression()
    model.fit(Z_train, y_train)


    message = request.json["message"]
    message = stemming(message)

    mess = tfidf.transform([message])
    y = model.predict(mess)[0]
    y = int(y)

    if y == 1:
        return str("Spam")
    return str("Ham")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)