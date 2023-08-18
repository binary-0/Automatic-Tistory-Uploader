import requests
import sys
from bs4 import BeautifulSoup
import json

#System arguments
#python {File.py} {access token} {blog name} {repository name}
arguments = sys.argv

access_token = arguments[1]
blogName = arguments[2]
repoName = arguments[3]

def post_blog():
    base_url = 'https://www.tistory.com/apis/post/write'

    contents = '<p>Hello World</p>'
    contents += '<h2>Does this POST work?</h2>'

    parameters = {
        'access_token': access_token,
        'output': 'json',
        'blogName': blogName,
        'title': repoName,
        'content': contents,
        'visibility': '3',
        'category': 'Anything',
        'tag': 'Tistory API Post',
        'acceptComment': '1'
    }

    result = requests.post(base_url, params=parameters)
    result = BeautifulSoup(result.text)
    print(result.prettify())

def edit_post(postID):
    base_url = 'https://www.tistory.com/apis/post/modify'

    contents = '<p>Hello World</p>'
    contents += '<h2>Does this EDIT work?</h2>'
    
    parameters = {
        'access_token': access_token,
        'output': 'json',
        'blogName': blogName,
        'postId': postID,
        'title': repoName,
        'content': contents,
        'visibility': '3',
        'category': 'Anything',
        'tag': 'Tistory API Post',
        'acceptComment': '1'
    }

    result = requests.post(base_url, params=parameters)
    result = BeautifulSoup(result.text)
    print(result.prettify())

def check_postExist():
    base_url = 'https://www.tistory.com/apis/post/list'
    repoExist = False
    postID = ""

    for i in range(1, 100):
        parameters = {
            'access_token': access_token,
            'output': 'json',
            'blogName': blogName,
            'page': i
        }
        
        listData = requests.get(base_url, params=parameters)
        result = json.loads(listData.text)
        print(i)
        print(result)

        try:
            for item in result["tistory"]["item"]["posts"]:
                if item["title"] == repoName:
                    print('Repository post already exists')
                    repoExist = True
                    postID = item["id"]
                    break
            
            if repoExist is True:
                edit_post(postID)
                break

        except Exception as e:
            print('Page overflowed - Post does not exist')
            print(e)

            post_blog()
            break
            
#post_blog()
check_postExist()