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

import random
import re

from collections import Counter
from nltk.corpus import stopwords


def index(request):

    return render(request, 'index.html')

def dashboard(request, search_term = None):

    if search_term != None:
        words = FindRelatedWords(search_term).words[0:10]
        urls = FindArticles(words).urls
        urls = random.sample(urls, len(urls)//2)

        analysis = ArticleAnalysis()
        text = ''
        for url in urls:
            text += analysis.parseArticle(url)
            

        stoplist = stopwords.words('english')
        stoplist.extend(["said", "The"]) # stoplist already includes "i", "it", "you"
        clean = [word for word in re.split(r"\W+", text.lower()) if word not in stoplist]
        top_10 = Counter(clean).most_common(15)
        print(top_10)

        print('Done')
        #analysis.sentiment_score(article)
        #analysis.entity_recognition(article)
        key_words = analysis.key_phrases(text)
        print(Counter(key_words).most_common(15))

    return render(request, 'dashboard.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/<str:search_term>', dashboard),
    re_path(r'^$', index, name='index'),
]
