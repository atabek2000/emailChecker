import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from sklearn import model_selection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# мәтінді өңдеуге арналған функция
def text_pp(docs):
    # стоп сөздерді жүктеп алу
    stop_words = set(stopwords.words('english'))
    documents = []
    for i in range(0, len(docs)):
        #  мәтіндегі стоп сөздерді өшіру
        text = ' '.join([word for word in word_tokenize(docs[i])  if not word in stop_words])
        # арнайы символдарды өшіріп төменгі регистрге келтіру
        text = re.sub(r'[^A-z ]|[\`\[\]\_]', '', str(text)).lower()
        # жалғыз символдарды өшіру
        text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
        # бірнеше пробелдерді өшіру
        text = re.sub(r'\s+', ' ', text, flags=re.I)
        # лемматизация жасау
        text = text.split()
        stemmer = WordNetLemmatizer()
        text = [stemmer.lemmatize(word) for word in text]
        text = ' '.join(text)
        documents.append(text)
    return documents

#  болжам жасауға арналған функция
def predict(user_text):
    # хабарламалар бар файлды жүктеп алу
    file = 'static/dataset/spam_ham_dataset.csv'
    df = pd.read_csv(file)
    # керек емес бағандарды өшіру
    df.drop('Unnamed: 0', inplace=True, axis=1)
    df.drop('label', inplace=True, axis=1)
    #  қолданушы енгізген мәтінді дата фреймге қосу
    df2 = pd.DataFrame([[user_text, '0']], columns=['text', 'label_num'], index=[5171])
    df = df.append(df2)
    X, y = df.text, df.label_num
    # мәтінді өңдеу
    documents = text_pp(X)
    # векторлы түргке келтіру
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents)
    # оқыту және тестілеу деректеріне бөлу
    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        X, y.astype(int), train_size=5171, shuffle=False)
    # классификация жасау
    classifier = RandomForestClassifier(n_estimators=200, random_state=100)
    classifier.fit(X_train, y_train)
    # қолданушы енгізген мәтінге болжам жасау
    y_pred = classifier.predict(X_test)
    # нәтижені қайтару
    return y_pred