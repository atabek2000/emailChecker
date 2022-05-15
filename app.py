from flask import Flask, render_template, request
import numpy as np
import re
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from random import randrange
app = Flask(__name__)
app.debug = True

def htmlspecialchars(text):
    return (
        text.replace("&", "&amp;").
        replace('"', "&quot;").
        replace("<", "&lt;").
        replace(">", "&gt;")
    )

@app.route('/')
def index():  
    return render_template('index.html')


@app.route('/text', methods=["GET", "POST"])
def text():
    if request.method == "GET":
        return render_template('text.html')
    elif request.method == "POST":
        # Қолданушы мәтінін алу
        text = htmlspecialchars(request.form['text'])
        text2 = htmlspecialchars(request.form['text'])
        # кіші әріптерге өзгерту
        if request.form['case'] == 'lower':
            text = text.lower()
        # үлкен әріптерге өзгерту
        elif request.form['case'] == 'upper':
            text = text.upper()
        # сандарды өшіру
        if request.form['number'] == '1':
            text = re.sub(r'\d', '', text)
        # пунктуацияларды өшіру
        if request.form['punct'] == '1':
            text = re.sub(r'[^A-zа-яА-ЯІҢҒҮҰҚіңғүұқөӨһҺ ]', '', text)
        # табуляцияны өшіру
        if request.form['tab'] == '1':
            text = re.sub(r'\t', '', text)
        # жалғыз символдарды өшіру
        if request.form['symbol'] == '1':
            text = re.sub(r'(^|\s).($|\s)', ' ', text)
        # пробелдерді өшіру
        if request.form['space'] == '1':
            text = re.sub(r' ', '', text)
        # жол үзілімдерін өшіру
        if request.form['l_break'] == '1':
            text = re.sub(r'\n', '', text)
        # ең көп кездесетін сөздер
        plt.figure()
        count1 = Counter(text2.split()).most_common(20)
        df1 = pd.DataFrame.from_dict(count1)
        df1 = df1.rename(columns={0: "words", 1: "count"})
        df1.plot.bar(legend=False, color='green')
        y_pos = np.arange(len(df1["words"]))
        plt.xticks(y_pos, df1["words"])
        plt.title('Сурет-1. Ең көп кездесетін сөздер')
        plt.xlabel('Сөздер')
        plt.ylabel('Саны')
        plt.savefig('static/images/count_word.png')
        # ең көп кездесетін символдар
        plt.figure()
        count1 = Counter(text2).most_common(20)
        df1 = pd.DataFrame.from_dict(count1)
        df1 = df1.rename(columns={0: "words", 1: "count"})
        df1.plot.bar(legend=False, color='green')
        y_pos = np.arange(len(df1["words"]))
        plt.xticks(y_pos, df1["words"])
        plt.title('Сурет-2. Ең көп кездесетін символдар')
        plt.xlabel('Символдар')
        plt.ylabel('Саны')
        plt.savefig('static/images/count_symbol.png')
        # қолданушыға қайтатын жауап
        answer = '<script>$("#user_text").val(htmlspecialchars_decode("'+text+'"));$("#text_images").html("");$("#text_images").append("<img src=\\"/static/images/count_word.png?version='+str(randrange(0,10000))+'\\"><img src=\\"/static/images/count_symbol.png?version='+str(randrange(0,10000))+'\\">")</script>'
        return answer


@app.route('/mail', methods=["GET", "POST"])
def mail():
    if request.method == 'GET':
        return render_template('mail.html')
    elif request.method == 'POST':
        from static.library.mail_predict import predict
        mail_type = predict(request.form['text'])
        if mail_type == 1:
            text = 'Бұл хабарлама <span class=\\"text-danger\\">спам</span>'
        else:
            text = 'Бұл хабарлама <span class=\\"text-success\\">спам емес</span>'
        return '<script>window_alert("<h5>'+text+'</h5>")</script>'


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
