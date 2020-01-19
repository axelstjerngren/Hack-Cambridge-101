from bs4 import BeautifulSoup
from selenium import webdriver

class FindRelatedWords: 
    def __init__(self, search_term):
        driver = webdriver.PhantomJS()
        url = "https://relatedwords.org/relatedto/" + search_term.replace(' ', '%20')
        driver.get(url)
        links = driver.find_element_by_class_name("words").find_elements_by_tag_name("a")
        
        self.words = []
        for link in links:
            self.words.append(link.text)
        print(self.words)



if __name__ == '__main__':
    FindRelatedWords('new word change')
