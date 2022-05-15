import numpy as np
import pandas as pd
import math as m
from nltk.stem import WordNetLemmatizer
from sklearn import model_selection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import nltk
import pickle
import gensim


def text_pp(docs):
    stop_words = set(stopwords.words('english'))
    documents = []
    for i in range(0, len(docs)):
        # print(i)
        text = ' '.join([word for word in word_tokenize(docs[i])  if not word in stop_words])
        text = re.sub(r'[^A-z ]|[\`\[\]\_]', '', str(text)).lower()
        text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
        text = re.sub(r'\s+', ' ', text, flags=re.I)
        text = text.split()
        stemmer = WordNetLemmatizer()
        text = [stemmer.lemmatize(word) for word in text]
        text = ' '.join(text)
        documents.append(text)

    return documents

def predict(user_text):
    file = 'static/dataset/spam_ham_dataset.csv'
    df = pd.read_csv(file)
    df.drop('Unnamed: 0', inplace=True, axis=1)
    df.drop('label', inplace=True, axis=1)
    df2 = pd.DataFrame([[user_text, '0']], columns=['text', 'label_num'], index=[5171])
    df = df.append(df2)
    X, y = df.text, df.label_num

    documents = text_pp(X)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents)
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y.astype(int), train_size=5171, shuffle=False)
    classifier = RandomForestClassifier(n_estimators=200, random_state=100)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    return y_pred