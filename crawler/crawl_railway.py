from .parent_crawl import Crawler
from dict_translit import dict_city_translit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import datetime

class CrawlerRailway(Crawler):
    
    def get_html(self):
        
        dep_city = dict_city_translit[self.departure_city]
        dest_city = dict_city_translit[self.destination_city]
        date = self.date + '.' + str(datetime.datetime.now().year)
        
        chrome_options = Options()
        #chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        
        train_url = f'https://жд-билеты.сайт/kupit-zhd-bilety/#/{dep_city}/{dest_city}?date={date}'
        
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(train_url)
        WebDriverWait(browser, timeout = 30).until(lambda d: d.find_element(By.CLASS_NAME, "wg-train-options__wrap"))
        
        return BeautifulSoup(browser.page_source, 'html.parser')