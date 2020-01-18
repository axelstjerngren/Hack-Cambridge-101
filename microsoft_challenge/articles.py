from newspaper import Article
from nltk import tokenize
import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

class ArticleAnalysis:
    
    def __init__(self):
        self.client = self.authenticateClient()

    def authenticateClient(self):
        # Connect to client 
        credentials = CognitiveServicesCredentials("7c3e42fb63c34c249400dadc01c57fb7")
        text_analytics_client = TextAnalyticsClient(
            endpoint="https://westcentralus.api.cognitive.microsoft.com/", credentials=credentials)
        return text_analytics_client

    def build_document(self, sentences):
        sentences = tokenize.sent_tokenize(article) # Split into sentences
        documents = []
        for i, sent in enumerate(sentences):
            documents.append({"id":str(i), "language": "en", "text": sent})
        return documents

    def parseArticle(self, url):
        # Take a URL, spit out text
        article = Article(url)
        article.download()
        article.parse()
        return article.text

    def sentiment_score(self, article):
        # Calculate the sentiment score of an article
        

        response = self.client.sentiment(
            documents = self.build_document(article)
        )
        counter = 0
        total_score = 0
        for document in response.documents:
            counter += 1

            total_score += document.score
        return total_score/counter # Average sentiment score
           

    def entity_recognition(self, article):
        response = self.client.entities(
            documents = self.build_document(article)
        )

        entities = {}

        for document in response.documents:
            for entity in document.entities:

                entities[entity.name] = {
                    "type" : entity.type, 
                    "sub-type": entity.sub_type,
                    "score" : 0
                    }

                for match in entity.matches:
                    entities[entity.name]['score'] = match.entity_type_score
        
        return entities
    
    def key_phrases(self, article):
        sentences = tokenize.sent_tokenize(article) # Split into sentences
        document = ''
        for sent in sentences:
            document += ' ' + sent
        
        response = self.client.key_phrases(documents= self.build_document(article))
        for document in response.documents:
            print("Document Id: ", document.id)
            print("\tKey Phrases:")
            for phrase in document.key_phrases:
                print("\t\t", phrase)



if __name__ == '__main__':
    analysis = ArticleAnalysis()
    article = analysis.parseArticle("https://www.bbc.co.uk/news/uk-politics-51161808")

    analysis.sentiment_score(article)
    analysis.entity_recognition(article)
    analysis.key_phrases(article)


