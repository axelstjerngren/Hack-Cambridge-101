import requests
import json

class FindArticles:
    
    def __init__(self, words):
        
        self.urls = []

        for word in words:
            url = ('https://newsapi.org/v2/everything?q=' + word + '&from=2020-01-18&sortBy=popularity&apiKey=5f153f6f958246f4a1f708a1c540f6ea')

            response = requests.get(url)
            articles = json.loads(response.text)



            for article in articles['articles']:
                self.urls.append(article['url'])

if __name__ == "__main__":
    words = [
        'GATTACA',
        'designer babies',
        'playing god',
        'bioterrorism',
        'artificial life',
        'bioweapons',
        'rogue synthetic biologist',
        'biological warfare',
        'biosecurity',
        'igem',
        'responsible innovation'
    ]

    FindArticles(words)