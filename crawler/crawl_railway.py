from crawler.parent_crawl import Crawler
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

class CrawlerRailway(Crawler):
    
    def get_html(self):
        chrome_options = Options()
        #chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        
        train_url = f'https://жд-билеты.сайт/kupit-zhd-bilety/#/{self.departure_city}/{self.destination_city}?date={self.date}.{datetime.now().year}'
        
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(train_url)
        WebDriverWait(browser, timeout = 30).until(lambda d: d.find_element(By.CLASS_NAME, "wg-train-options__wrap"))
        
        return BeautifulSoup(browser.page_source, 'html.parser')