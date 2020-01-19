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
import json

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
        top_10 = Counter(clean).most_common(150)
        print(top_10)
        end = time.time()
        print(end-start)

        print('Done')
        
        


        key_phrases = analysis.key_phrases(text)
        key_phrases = [key for key, _ in Counter(key_phrases).most_common(4)]

        try:
            pytrends = TrendReq(hl='en-US', tz=360)
            kw_list = [key_phrases]
            pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='', gprop='')
            trends = pytrends.interest_over_time()
            trends.drop(['isPartial'], inplace = True)
        except:
            pass

        people = sorted(people, key=people.get, reverse=True)[0:5]
 
        if len(titles) > 5:
            titles = random.sample(titles, 5)
        print(titles)
        return render(request, 'dashboard.html', 
            {
            "sentiment" : json.dumps(topic_sentiment),
            "average_sentiment" : sum(topic_sentiment)/len(topic_sentiment),
            "wordcloud" : top_10,
            "titles" : titles,
            'people' : people,
            'locations' : locations
            }
        )

    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        kw_list = ['test', 'word', 'whoops']
        pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='', gprop='')
        trends = pytrends.interest_over_time()
    except:
        pass

    return render(request, 'dashboard.html', 
            {
            "time_series" : trends.to_json(),
            "sentiment" : json.dumps([0.5,0.2,0.4,0.8,0.1,0.4]),
            "average_sentiment" : 0.3,
            "wordcloud" : ["The CRISPR system in bacteria and archaea provides adaptive immunity against mobile genetic elements. Type III CRISPR systems detect viral RNA, resulting in the activation of two regions of the Cas10 protein: an HD nuclease domain (which degrades viral DNA)1,2 and a cyclase domain (which synthesizes cyclic oligoadenylates from ATP)3,4,5. Cyclic oligoadenylates in turn activate defence enzymes with a CRISPR-associated Rossmann fold domain6, sculpting a powerful antiviral response7,8,9,10 that can drive viruses to extinction7,8. Cyclic nucleotides are increasingly implicated in host–pathogen interactions11,12,13. Here we identify a new family of viral anti-CRISPR (Acr) enzymes that rapidly degrade cyclic tetra-adenylate (cA4). The viral ring nuclease AcrIII-1 is widely distributed in archaeal and bacterial viruses and in proviruses. The enzyme uses a previously unknown fold to bind cA4 specifically, and a conserved active site to rapidly cleave this signalling molecule, allowing viruses to neutralize the type III CRISPR defence system. The AcrIII-1 family has a broad host range, as it targets cA4 signalling molecules rather than specific CRISPR effector proteins. Our findings highlight the crucial role of cyclic nucleotide signalling in the conflict between viruses and their hosts."],
            "titles" : [('The kill-switch for CRISPR that could make gene-editing safer','https://www.nature.com/articles/d41586-020-00053-0','Elie Dolgin'),('This CRISPR tool costs $10,000. Researchers made a version that costs 23 cents','https://www.inverse.com/article/62213-crispr-gene-editing-electroporator-cheap',
            'Thor Benson'),('Analysis of CRISPR baby documents reveals more ethical violations','https://www.newscientist.com/article/2229233-analysis-of-crispr-baby-documents-reveals-more-ethical-violations/',
            'Michael Le Page'),('Should We Alter the Human Genome? Let Democracy Decide','https://blogs.scientificamerican.com/observations/should-we-alter-the-human-genome-let-democracy-decide/','Krishanu Saha, J. Benjamin Hurlbut, Sheila Jasanoff'),('Emendo Biotherapeutics Nabs $61M for “Next-Generation CRISPR” R&D',
            'https://xconomy.com/new-york/2020/01/15/emendo-biotherapeutics-nabs-61m-for-next-generation-crispr-rd/','Frank Vinluan')],
            'people' : ['Alan Davidson','Joe Bondy-Denomy','David Shaw','Saad Bhamla'],
            'locations' : json.dumps(['San Francisco', 'Quebec City', 'Toronto','Georgia']),
            }
        )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/<str:search_term>', dashboard),
    path('dashboard/', dashboard),
    re_path(r'^$', index, name='index'),
]
