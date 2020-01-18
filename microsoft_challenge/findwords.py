from bs4 import BeautifulSoup
from selenium import webdriver

class FindRelatedWords: 
    def __init__(self, search_term):
        driver = webdriver.PhantomJS()
        url = "https://relatedwords.org/relatedto/" + search_term.replace(' ', '%20')
        driver = driver.get(url)
        print(driver)
        


if __name__ == '__main__':
    FindRelatedWords('test')