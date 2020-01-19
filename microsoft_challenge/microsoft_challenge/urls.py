"""microsoft_challenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.shortcuts import render
from findwords import FindRelatedWords
from findarticles import FindArticles
from articles import ArticleAnalysis
import threading
import random
import re

import time
from pytrends.request import TrendReq


from collections import Counter
from nltk.corpus import stopwords


def index(request):

    return render(request, 'index.html')

def dashboard(request, search_term = None):

    if search_term != None:
        
        try:
            start = time.time()
            words = FindRelatedWords(search_term).words[0:4]
            end = time.time()
            print(end-start)
        except:
            words = [search_term]
        start = time.time()
        urls = FindArticles(words).urls
        end = time.time()
        print(end-start)

        start = time.time()
        if len(urls) > 20:
            urls = random.sample(urls, 20)
        end = time.time()
        print(end-start)

        analysis = ArticleAnalysis()
        text = ''

        start = time.time()
        topic_sentiment = []
        titles = []
        people = {}
        locations = {}
        for url in urls:
            article, title, author = analysis.parseArticle(url)
            text += article 
            topic_sentiment.append(analysis.sentiment_score(article))

            for k,v in analysis.entity_recognition(article).items():
                if v['type'] == 'Person':
                    if k not in people:
                        people[k] = 1
                    else:
                        people[k] = people[k] + 1
                if v['type'] == 'Location':
                    if k not in locations:
                        locations[k] = 1
                    else:
                        locations[k] = locations[k] + 1

            titles.append((title, url, author))
        print(topic_sentiment)
        end = time.time()
        print(end-start)

        start = time.time()
        stoplist = stopwords.words('english')
        stoplist.extend(["said", "The"]) # stoplist already includes "i", "it", "you"
        clean = [word for word in re.split(r"\W+", text.lower()) if word not in stoplist]
        top_10 = Counter(clean).most_common(15)
        print(top_10)
        end = time.time()
        print(end-start)

        print('Done')
        
        


        key_phrases = analysis.key_phrases(text)
        key_phrases = [key for key, _ in Counter(key_phrases).most_common(10)]

        #pytrends = TrendReq(hl='en-US', tz=360)
        #kw_list = [key_phrases]
        #pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

    people = sorted(people, key=people.get, reverse=True)[0:5]
    print(people)
    print(key_phrases)
    print(top_10)
    if len(titles) > 5:
        titles = random.sample(titles, 5)
    print(titles)
    return render(request, 'dashboard.html', 
        {"average_sentiment" : sum(topic_sentiment)/len(topic_sentiment),
        "wordcloud" : top_10,
        "titles" : titles,
        'people' : people,
        'locations' : locations
        }
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/<str:search_term>', dashboard),
    re_path(r'^$', index, name='index'),
]
