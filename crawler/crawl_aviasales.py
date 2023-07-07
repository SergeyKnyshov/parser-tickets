from crawler.parent_crawl import Crawler
from crawler.dict_sokr import dict_city
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

class CrawlerAviaSales(Crawler):
    
    def get_html(self):
        
        dep_city = dict_city[self.departure_city]
        dest_city = dict_city[self.destination_city]
        date = self.date[:2]+self.date[3:]
        
        chrome_options = Options()
        #chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")

        browser = webdriver.Chrome(options=chrome_options)
        avia_url = f'https://www.aviasales.ru/search/{dep_city}{date}{dest_city}1'        
        browser.get(avia_url)
        WebDriverWait(browser, timeout = 30).until(lambda d: d.find_element(By.CLASS_NAME, "ticket-desktop"))
        return BeautifulSoup(browser.page_source, 'html.parser')