import csv
import json
import math

import requests
from bs4 import BeautifulSoup
from pyvi import ViTokenizer

article_content = []

cleaned_content_of_each_article = []


def get_article(link: str):
    content = requests.get(link)
    # print(content.text)
    soup = BeautifulSoup(content.content, 'html.parser')
    # get article content (<p> tag)
    found_content = soup.find_all("div", class_="detail__content")
    # print(soup.get_text())
    return str(found_content)


def clean_content(article: str):
    str_list = list(article)
    i = 0
    while i != len(str_list):
        if str_list[i] == '<':
            while str_list[i] != '>':
                str_list[i] = ''
                i = i + 1
            if str_list[i] == '>':
                str_list[i] = ''
        i = i + 1
    res = ''.join(str_list)
    bad_word = ['.', ',', '(', ')', '...', '"', '+', ':']
    for i in bad_word:
        res = res.replace(i, '')
    return res


def split_word(article_text: str):
    words = ViTokenizer.tokenize(article_text)
    # link the word that containing 2-3 words by '_', return a string
    list_words = words.split()
    # split the string into meaning word in Vietnamese
    return list_words


def list_word(list_link: list):
    list_word = []
    for link in list_link:
        doc = clean_content(get_article(link))
        for word in split_word(doc):
            list_word.append(word)
    return list_word


def count_fre_in_article(list_word: list, word: str):
    count = 0
    if (word in list_word):
        for item in list_word:
            if (item == word):
                count = count + 1
    return count

def read_csv_file(filename: str):
    prob_word = {}
    with open(filename, 'r',encoding='utf8') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            key = row[0]
            value_str = row[1]
            value = float(value_str)
            prob_word[key] = value
    return prob_word

def analysis_an_article(link: str):
    word_in_article = split_word(clean_content(get_article(link)))
    prob_words = {}
    prob_words = read_csv_file('prob_pos_word.csv')
    vector = [0 for _ in range(len(prob_words))]
    i = -1
    for item in prob_words:
        i = i + 1
        vector[i] = count_fre_in_article(word_in_article, item)
    positive_point = 60 / 150
    negative_point = 52 / 150
    neutral_point = 38 / 150
    prob_pos = read_csv_file('prob_pos_word.csv')
    prob_neg = read_csv_file('prob_neg_word.csv')
    prob_neu = read_csv_file('prob_neu_word.csv')

    j = 0
    for item in prob_words:
        positive_point *= math.pow(prob_pos[item] * 1000, vector[j])
        negative_point *= math.pow(prob_neg[item] * 1000, vector[j])
        neutral_point *= math.pow(prob_neu[item] * 1000, vector[j])
        j += 1

    pos_percent = 100 * (positive_point) / (positive_point + negative_point + neutral_point)
    neg_percent = 100 * (negative_point) / (positive_point + negative_point + neutral_point)
    neu_percent = 100 * (neutral_point) / (positive_point + negative_point + neutral_point)
    '''
    print("Positive point: ", pos_percent)
    print("Negative point: ", neg_percent)
    print("Neutral point: ", neu_percent)
    '''
    res = []
    res.append(pos_percent)
    res.append(neg_percent)
    res.append(neu_percent)
    return res

def implement_analysis_article(link: str):
    result = analysis_an_article(link)
    print("Positive point: ", result[0])
    print("Negative point: ", result[1])
    print("Neutral point: ", result[2])

    round_percent_pos = round(result[0], 2)
    round_percent_neg = round(result[1], 2)
    round_percent_neu = round(result[2], 2)

    sentiment = str(round_percent_pos) \
                + " " + str(round_percent_neg) \
                + " " + str(round_percent_neu)

    return sentiment

def get_links_of_company(name: str):
    links = []
    baseUrl = 'https://vneconomy.vn/'
    url = 'https://search.hemera.com.vn/search/1/' + name + '/time/1'
    response = requests.get(url)
    # Get returned json object
    data = response.json()

    for i in range(0, len(data['List'])):
        links.append(baseUrl + data['List'][i]['UrlArticle'] + '.htm')
        # Output all article's content to an array

    url = 'https://search.hemera.com.vn/search/1/' + name + '/time/2'
    response = requests.get(url)
    data = response.json()
    if (len(data['List']) > 0):
        for i in range(0, len(data['List'])):
            links.append(baseUrl + data['List'][i]['UrlArticle'] + '.htm')
    return links

def print_links_of_company(name: str):
    links = get_links_of_company(name)
    print(links)
    return links

def analysis_an_company(name: str):
    links = get_links_of_company(name)
    positive = 0
    negative = 0
    neutral = 0
    for item in links:
        result = analysis_an_article(item)
        if result[0] > result[1] and result[0] > result[2]:
            positive += 1
        elif result[1] > result[0] and result[1] > result[2]:
            negative += 1
        else:
            neutral += 1
    print("The development situation of this company: ")
    print("Positive status: ",positive/(positive + negative + neutral)* 100 ,"%")
    print("Negative status: " , negative/(positive + negative + neutral)* 100 , "%")
    print("Neutral status: ", neutral/(positive + negative + neutral)* 100 , "%")

    round_percent_pos = round(positive/(positive + negative + neutral)* 100, 2)
    round_percent_neg = round(negative/(positive + negative + neutral)* 100, 2)
    round_percent_neu = round(neutral/(positive + negative + neutral)* 100, 2)

    sentiment = str(round_percent_pos) \
                + " " + str(round_percent_neg) \
                + " " + str(round_percent_neu)

    return sentiment


def add_article(pos_links, neu_links, neg_links):
    with open("PositiveLink.json", "r") as file1:
        positive_links = json.load(file1)
    with open("NegativeLink.json", "r") as file2:
        negative_links = json.load(file2)
    with open("NeutralLink.json", "r") as file3:
        neutral_links = json.load(file3)

    positive_links.extend(pos_links)
    negative_links.extend(neu_links)
    neutral_links.extend(neg_links)

    with open("PositiveLink.json", "w") as file1:
        json.dump(positive_links, file1)
    with open("NegativeLink.json", "w") as file2:
        json.dump(negative_links, file2)
    with open("NeutralLink.json", "w") as file3:
        json.dump(neutral_links, file3)












