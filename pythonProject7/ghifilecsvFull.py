import json
import math
from typing import List
import csv

import requests
from bs4 import BeautifulSoup
from pyvi import ViTokenizer
from collections import Counter

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


if __name__ == '__main__':

    positiveLinks: list[str] = []
    negativeLinks: list[str] = []
    neutralLinks: list[str] = []
    posWords = []
    negWords = []
    neuWords = []
    bagWord = []

    with open("PositiveLink.json","r") as file_1:
        positiveLinks = json.load(file_1)
    with open("NegativeLink.json","r") as file_2:
        negativeLinks = json.load(file_2)
    with open("NeutralLink.json","r") as file_3:
        neutralLinks = json.load(file_3)
    file_1.close()
    file_2.close()
    file_3.close()

    links = set(positiveLinks).union(set(negativeLinks)).union(set(negativeLinks))


    posWords = list_word(positiveLinks)
    negWords = list_word(negativeLinks)
    neuWords = list_word(neutralLinks)
    bagWord = posWords + negWords + neuWords

    # Important point
    fre_words = Counter(bagWord)
    fre_pos = Counter(posWords)
    fre_neg = Counter(negWords)
    fre_neu = Counter(neuWords)

    avr_fre = len(bagWord) / len(fre_words)
    temp_dic = fre_words.copy()
    for item in temp_dic:
        if(math.log2(1+avr_fre/fre_words[item])<0.75):
            del(fre_words[item])
            del(fre_pos[item])
            del(fre_neg[item])
            del(fre_neu[item])
        if(str(item).islower() != True):
            del(fre_words[item])
            del(fre_pos[item])
            del(fre_neg[item])
            del(fre_neu[item])


    fre_in_pos = {}
    fre_in_neg = {}
    fre_in_neu = {}
    for item in fre_words:
        fre_in_pos[item] = fre_pos[item]
        fre_in_neg[item] = fre_neg[item]
        fre_in_neu[item] = fre_neu[item]

    #print(lamda_neg)
    sum_all_word = len(fre_words)
    num_pos = 0
    num_neg = 0
    num_neu = 0
    for item in fre_pos:
        num_pos += fre_pos[item]
    for item in fre_neg:
        num_neg += fre_neg[item]
    for item in fre_neu:
        num_neu += fre_neu[item]

    prob_pos = {}
    prob_neg = {}
    prob_neu = {}
    for item in fre_in_pos:
        prob_pos[item] = (fre_in_pos[item]+1)/(num_pos + sum_all_word)
    for item in fre_in_neg:
        prob_neg[item] = (fre_in_neg[item]+1)/(num_neg + sum_all_word)
    for item in fre_in_neu:
        prob_neu[item] = (fre_in_neu[item]+1)/(num_neu + sum_all_word)

    filename1 = 'prob_pos_word.csv'
    with open(filename1, 'w', newline='',encoding='utf8') as file1:
        writer1 = csv.writer(file1)
        writer1.writerow(['Word','Probability'])
        for item in prob_pos:
            writer1.writerow([item,prob_pos[item]])
    file1.close()

    filename2 = 'prob_neg_word.csv'
    with open(filename2, 'w', newline='', encoding='utf8') as file2:
        writer2 = csv.writer(file2)
        writer2.writerow(['Word', 'Probability'])
        for item in prob_neg:
            writer2.writerow([item, prob_neg[item]])
    file2.close()

    filename3 = 'prob_neu_word.csv'
    with open(filename3, 'w', newline='',encoding='utf8') as file3:
        writer3 = csv.writer(file3)
        writer3.writerow(['Word','Probability'])
        for item in prob_neu:
            writer3.writerow([item,prob_neu[item]])
    file3.close()