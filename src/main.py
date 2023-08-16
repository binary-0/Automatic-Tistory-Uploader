import requests
import sys
from bs4 import BeautifulSoup

arguments = sys.argv
access_token = arguments[1]

def post_blog():
    base_url = 'https://www.tistory.com/apis/post/write'

    title = 'Hello World'
    contents = '<p>Hello World</p>'
    contents += '<h2>Does this HTML work?</h2>'

    parameters = {
        'access_token': access_token,
        'output': '{output-type}',
        'blogName': 'Binary-Zero',
        'title': title,
        'content': contents,
        'visibility': '3',
        'category': 'Anything',
        'tag': 'Tistory API Post',
        'acceptComment': '1'
    }

    result = requests.post(base_url, params=parameters)
    result = BeautifulSoup(result.text)
    print(result.prettify())

post_blog()