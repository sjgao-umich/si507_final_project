from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import spacy
import datetime
from spacy.lang.en.stop_words import STOP_WORDS
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import sys
import os
import secrets


#Ask for input:
def input_keyword():
    keyword = input('Enter a word that you want to search for. Enter "quit" to end the program.')
    return keyword

def input_newkeyword(keyword):
    new_keyword = input(f'Enter a word that you want to compare with [{keyword}]. Enter "quit" to end the program.')
    return new_keyword

def input_begindate():
    begin_date = input('Enter the begin date (e.g.20200101)')
    return begin_date

def input_enddate():
    end_date = input('Enter the end date (e.g.20200202)')
    return end_date

#Collecting data:
def make_request(baseurl, params):
    response = requests.get(baseurl,params)
    results = response.json()
    return results

#Caching:
FIB_CACHE = {}
def get_words_from_article(website_url):
    article_text = requests.get(website_url)
    soup = BeautifulSoup(article_text.text,'html.parser')
    article_p = soup.find_all(class_='css-axufdj evys1bk0')
    p_list = []
    for p in article_p:
        p_list.append(p.text)
    return p_list

def get_words_from_article_with_cache(website_url):
    if website_url in FIB_CACHE:
	    print('Using Cache')
	    return FIB_CACHE[website_url]
    else:
	    FIB_CACHE[website_url] = get_words_from_article(website_url)
	    print('Fetching')
	    return FIB_CACHE[website_url]

#Generate word list:
def generate_word_list(results):
    if results['response']['docs'][0]['web_url']:
        url_01 = results['response']['docs'][0]['web_url']
        text_01 = get_words_from_article_with_cache(url_01)
    else:
        text_01 = []
    if len(results['response']['docs'])>=2:
        url_02 = results['response']['docs'][1]['web_url']
        text_02 = get_words_from_article_with_cache(url_02)
    else:
        text_02 = []
    if len(results['response']['docs'])>=3:
        url_03 = results['response']['docs'][2]['web_url']
        text_03 = get_words_from_article_with_cache(url_03)
    else:
        text_03 = []
    if len(results['response']['docs'])>=4:
        url_04 = results['response']['docs'][3]['web_url']
        text_04 = get_words_from_article_with_cache(url_04)
    else:
        text_04 = []
    if len(results['response']['docs'])>=5:
        url_05 = results['response']['docs'][4]['web_url']
        text_05 = get_words_from_article_with_cache(url_05)
    else:
        text_05 = []
    word_list = text_01
    word_list.extend(text_02)
    word_list.extend(text_03)
    word_list.extend(text_04)
    word_list.extend(text_05)

    word_list_nostop = []
    word_str = ''
    for sentence in word_list:
        word_str += sentence
    word_str = word_str.lower()
    word_str = re.sub(r'[^\w\s]+', ' ', word_str)
    new_word_list = word_str.split()
    for word in new_word_list:
        if word not in STOP_WORDS:
            if len(word) >3:
                word_list_nostop.append(word)

    return word_list_nostop

#Draw word cloud:
def draw_word_cloud(word_list_nostop):
    text_word_nostop = str(word_list_nostop)
    text_word_nostop = text_word_nostop.replace("'",'')
    text_wordcloud = WordCloud(max_font_size=40).generate(text_word_nostop)
    plt.imshow(text_wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

#Save word cloud:
def save_word_cloud(word_list_nostop):
    text_word_nostop = str(word_list_nostop)
    text_word_nostop = text_word_nostop.replace("'",'')
    text_wordcloud = WordCloud(max_font_size=40).generate(text_word_nostop)
    plt.imshow(text_wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(f'/Users/gaoshijie/Documents/umich/courses/Winter_2021/si507/Homework/Final_Project/final_project_result_csv/{keyword}_wordcloud.png')

#Count words and save them to a csv file:
def count_words(word_list_nostop, keyword):
    word_freq = []
    for w in word_list_nostop:
        word_freq.append(word_list_nostop.count(w))
    print('================================')
    df_word_count = pd.DataFrame({'word':word_list_nostop,'frequency':word_freq})
    df_word_count.drop_duplicates(subset='word',inplace=True)
    df_word_count = df_word_count.sort_values(by='frequency',ascending=False)
    df_word_count.to_csv(f'/Users/gaoshijie/Documents/umich/courses/Winter_2021/si507/Homework/Final_Project/final_project_result_csv/word_count_{keyword}.csv',index=0)
    top_10_words = df_word_count.head(10)
    return top_10_words

#Draw bar plot comparing the two keywords:
def generate_bar_plot(word_list_A, word_list_B, keyword, new_keyword):
    word_list_A = word_list_A.set_index('word')
    word_list_B = word_list_B.set_index('word')
    f, (ax1, ax2) = plt.subplots(2)
    word_list_A.plot(ax = ax1, kind = 'bar', rot=90)
    ax1.title.set_text(f'{keyword}')
    word_list_B.plot(ax = ax2, kind = 'bar', rot=90)
    ax2.title.set_text(f'{new_keyword}')
    plt.show()

#Save bar plot:
def save_bar_plot(word_list_A, word_list_B, keyword, new_keyword):
    word_list_A = word_list_A.set_index('word')
    word_list_B = word_list_B.set_index('word')
    f, (ax1, ax2) = plt.subplots(2)
    word_list_A.plot(ax = ax1, kind = 'bar', rot=90)
    ax1.title.set_text(f'{keyword}')
    word_list_B.plot(ax = ax2, kind = 'bar', rot=90)
    ax2.title.set_text(f'{new_keyword}')
    plt.savefig(f'/Users/gaoshijie/Documents/umich/courses/Winter_2021/si507/Homework/Final_Project/final_project_result_csv/{keyword}_{new_keyword}_barplot.png')
#Restart the program:
def restart():
    print("argv was",sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")
    os.execv(sys.executable, ['python'] + sys.argv)
    print('================================')

if __name__ == "__main__":
#Input Word A:
    keyword = input_keyword()
    if keyword == 'quit':
        quit()
    begin_date = input_begindate()
    end_date = input_enddate()
    baseurl = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
    api_key = secrets.api_key
    params = {'q':keyword,'api-key':api_key,
    'begin_date': begin_date, 'end_date': end_date}

    results = make_request(baseurl, params)
    #generate word list:
    word_list_nostop = generate_word_list(results)
    #word A's top 10 relative words:
    top_10_words_of_keyword_A = count_words(word_list_nostop, keyword)
#Two options: word cloud & compare with another word
    decision = input('Option 1: Draw a word cloud. Please enter "cloud". \nOption 2: Compare with another word. Please enter "compare". \nOption 3: Enter "quit" to end the program.')
    #Draw word cloud for word A:
    if decision == 'cloud':
        draw_word_cloud(word_list_nostop)
        print('================================')
        decision = input('Option 1: Enter "Y" to save your word cloud. \nOption 2: Enter "N" to continue without saving your word cloud.')
        if decision == 'Y':
            save_word_cloud(word_list_nostop)
            print('================================')
        elif decision == 'N':
            print('================================')
            pass
        #After drawing word cloud, user can choose to quit, or to input another word to compare them:
        decision = input('Option 1: Enter "compare" to enter another word you that want to compare with. \nOption 2: Enter "quit" to end the program.')
    #Input word B:
    if decision == 'compare':
        print('================================')
        new_keyword = input_newkeyword(keyword)
        if new_keyword == 'quit':
            decision = 'quit'
            print('Bye bye!')
            quit()
        new_params = {'q':new_keyword,'api-key':api_key,'begin_date': begin_date, 'end_date': end_date}
        new_word_results = make_request(baseurl, new_params)
        new_word_list_nostop = generate_word_list(new_word_results)
        top_10_words_of_keyword_B = count_words(new_word_list_nostop, new_keyword)

        print(f'Top 10 relevant words of {keyword}: ')
        print(top_10_words_of_keyword_A)
        print('================================')
        print(f'Top 10 relevant words of {new_keyword}: ')
        print(top_10_words_of_keyword_B)
        generate_bar_plot(top_10_words_of_keyword_A, top_10_words_of_keyword_B, keyword, new_keyword)
        print('================================')
        decision = input('Option 1: Enter "Y" to save your barplot. \nOption 2: Enter "N" to continue without saving your barplot.')
        if decision == 'Y':
            save_bar_plot(top_10_words_of_keyword_A, top_10_words_of_keyword_B, keyword, new_keyword)
            print('================================')
        elif decision == 'N':
            print('================================')
            pass
        decision = input('Option 1: Enter "quit" to end the program. \nOption 2: Enter "restart" to restart the program.')
    if decision == 'quit':
        print('Bye bye!')
        quit()
    if decision == 'restart':
        restart()
    else:
        print('Invalid input. Please try again.')
        restart()
