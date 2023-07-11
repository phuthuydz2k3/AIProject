from flask import Flask, request, render_template
import flask_cors
from Final import implement_analysis_article, analysis_an_company, print_links_of_company

app = Flask(__name__)
flask_cors.CORS(app)


@app.route('/sentiment', methods=['GET', 'POST'])
def produce_sentiment():
    if request.method == 'POST':
        url = request.form['url']

        return implement_analysis_article(url)

    return render_template('form.html')


@app.route('/sentimentCompany', methods=['GET', 'POST'])
def produce_sentiment1():
    if request.method == 'POST':
        company = request.form['company']

        return analysis_an_company(company)

    return render_template('form.html')


@app.route('/sentimentPrintLinks', methods=['GET', 'POST'])
def produce_sentiment2():
    if request.method == 'POST':
        company = request.form['company']

        return print_links_of_company(company)

    return render_template('form.html')


if __name__ == '__main__':
    app.run(port=5000)
