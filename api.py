import os
import uuid
from datetime import datetime
from pathlib import Path
from flask import Flask, Response, request
from flask_restful import Resource, Api
from waitress import serve
import base64

from scraper import Scraper

#
# Environment Variables:
#   PORT - The port on which the api service runs [default=8080]
#   SELENIUM_PROXY - The proxy to use.
#   CHROME_DRIVER_PATH - The path to the chrome driver [default='./chromedriver']
#

app = Flask(__name__)
api = Api(app)

scrape = Scraper()

##### begin api route definitions #####
@app.route('/api/instagram/users/<username>', methods=['POST'])
def getInstagramUserInfo(username):
    try:
        print('POST /api/instagram/users/<username={}>'
              .format(username))

        info = scrape.instagram_user_info(username)
        return info
    except Exception as e:
        return { 'error': repr(e) }

if __name__ == '__main__':
    port = os.environ.get('PORT') or 8080
    serve(app, host='0.0.0.0', port=port)

