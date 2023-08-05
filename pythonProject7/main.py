from flask import Flask, request, render_template
import flask_cors
from Final import implement_analysis_article, analysis_an_company, print_links_of_company, add_article

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


@app.route('/database', methods=['GET', 'POST'])
def paste_database():
    if request.method == 'POST':
        positive_links = request.form['positiveLinks']
        neutral_links = request.form['neutralLinks']
        negative_links = request.form['negativeLinks']

        # Convert the received strings back to arrays
        positive_links = positive_links.split('\n')
        neutral_links = neutral_links.split('\n')
        negative_links = negative_links.split('\n')

        if isinstance(positive_links, list):
            print("positive_links is an array (list)")
        else:
            print("positive_links is not an array (list)")

        add_article(positive_links, neutral_links, negative_links)

        return "1"  # You can return any response here

    return render_template('form.html')



if __name__ == '__main__':
    app.run(port=5000)
