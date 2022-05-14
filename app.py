from flask import Flask, render_template, request
import re
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():  
    return render_template('index.html')


@app.route('/text', methods=["GET", "POST"])
def text():
    if request.method == "GET":
        return render_template('text.html')
    elif request.method == "POST":
        text = request.form['text']
        if request.form['case'] == 'lower':
            text = text.lower()
        elif request.form['case'] == 'upper':
            text = text.upper()
        if request.form['number'] == '1':
            text = re.sub(r'\d', '', text)
        if request.form['punct'] == '1':
            text = re.sub(r'[^A-zа-яА-ЯІҢҒҮҰҚіңғүұқөӨһҺ ]', '', text)
        if request.form['tab'] == '1':
            text = re.sub(r'\t', '', text)
        if request.form['space'] == '1':
            text = re.sub(r' ', '', text)
        if request.form['symbol'] == '1':
            text = re.sub(r'(^|\s).($|\s)', ' ', text)
        if request.form['l_break'] == '1':
            text = re.sub(r'\n', '', text)
        answer = '<script>$("#user_text").val("'+text+'")</script>'
        return answer


@app.route('/mail')
def mail():
    return render_template('mail.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
