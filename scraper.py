import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from PIL import Image
import time
import re

class Scraper:

    chrome_driver_path = None
    driver = None
    last_run_time = 0

    def __init__(self):
        chrome_driver_path = os.environ.get('CHROME_DRIVER_PATH') or './chromedriver'
        proxy = os.environ.get('SELENIUM_PROXY') or ''

        chrome_options = Options()
        #chrome_options.headless = True
        chrome_options.add_argument('--proxy-server=%s' % proxy)
        chrome_options.add_argument("user-data-dir=selenium")

        print('Scraper: setting up driver.')
        self.driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)
        print('Scraper: driver setup done.')

    def instagram_user_info(self, username):
        url = 'https://instagram.com/{}'.format(username)
        print('instagram_user_info: getting page <{}>.'.format(url))
        self.driver.get(url)
        print('instagram_user_info: got page <{}>.'.format(url))

        page_source = self.driver.page_source

        followers_count = get_followers_ct_method(page_source)

        return { 'followers_count': followers_count }


def get_followers_ct_method(page_source):
    match = re.search('edge_followed_by":{"count":(.+?)\}', page_source).group(1)
    followers_count = int(match)
    return followers_count


