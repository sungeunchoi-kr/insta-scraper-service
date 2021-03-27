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
        #chrome_options.add_argument('--proxy-server=%s' % proxy)
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
    match = re.search('Temporarily Locked', page_source)
    if match:
        print('get_followers_ct: detected account locked.')
        raise Exception('get_followers_ct: account locked.')

    match = re.search('edge_followed_by":{"count":(.+?)\}', page_source)
    if match:
        group = match.group(1)
        followers_count = int(group)
        return followers_count

    print('get_followers_ct: search failed with crib="edge_followed_by". ' +
        'Trying other cribs.')

    match = re.search('"userInteractionCount":"(.+?)"\}', page_source)
    if match:
        group = match.group(1)
        followers_count = int(group)
        return followers_count
    else:
        print('get_followers_ct: search failed with crib="userInteractionCount". ' +
            'Wrote page source to "./failed.html".')
        with open('failed.html', 'w') as file:
            file.write(page_source)
        raise Exception('get_followers_ct: search failed. crib="userInteractionCount".')

