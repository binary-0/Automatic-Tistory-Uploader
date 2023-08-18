import requests
import sys
import json
import os
import readRepoCommits

#System arguments
#python {File.py} {access token} {blog name} {repository name}
#arguments = sys.argv

# access_token = os.environ["INPUT_ACCESSTOKEN"]
# blogName = os.environ["INPUT_BLOGNAME"]
# repoName = os.environ['GITHUB_REPOSITORY']
# repoName = str(repoName)

arguments = sys.argv

access_token = arguments[1]
blogName = arguments[2]
repoName = arguments[3]

global contents
contents = ''

def contents_generator():
    #ReadMe 읽고 맨 위에 쓰고
    global contents

    commits = readRepoCommits.get_commits()
    commitCounter = 1

    for commit in commits:
        if commit["message"] != '':
            contents += '<p>'
            contents += 'Commit message No. '
            contents += str(commitCounter)
            contents += ': '
            contents += commit["message"]
            contents += '</p>'
            commitCounter = commitCounter + 1

def post_blog():
    global contents

    base_url = 'https://www.tistory.com/apis/post/write'
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
    print(result)

def edit_post(postID):
    global contents

    base_url = 'https://www.tistory.com/apis/post/modify'
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
    print(result)

def check_postExist():
    base_url = 'https://www.tistory.com/apis/post/list'
    repoExist = False
    postID = ""

    contents_generator()

    for i in range(1, 100):
        parameters = {
            'access_token': access_token,
            'output': 'json',
            'blogName': blogName,
            'page': i
        }
        
        listData = requests.get(base_url, params=parameters)
        result = json.loads(listData.text)
        print(result)

        try:
            for item in result["tistory"]["item"]["posts"]:
                if item["title"] == repoName:
                    print('Repository post already exists -> Edit')
                    repoExist = True
                    postID = item["id"]
                    break
            
            if repoExist is True:
                edit_post(postID)
                break

        except Exception as e:
            print('Page overflowed - Post does not exist -> Post')
            print(e)

            post_blog()
            break
            
#post_blog()
check_postExist()
