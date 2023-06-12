from .parent_crawl import Crawler
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

class CrawlerAviaSales(Crawler):
    
    def get_html(self):
        chrome_options = Options()
        #chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")

        browser = webdriver.Chrome(options=chrome_options)
        avia_url = f'https://www.aviasales.ru/search/{self.departure_city}{self.date[:2]}{self.date[3:]}{self.destination_city}1'        
        browser.get(avia_url)
        WebDriverWait(browser, timeout = 30).until(lambda d: d.find_element(By.CLASS_NAME, "ticket-desktop"))
        return BeautifulSoup(browser.page_source, 'html.parser')