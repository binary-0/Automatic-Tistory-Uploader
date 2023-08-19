import requests
import sys
import json
import os
import markdown

import readRepoCommits
import getReadmeContents
import summarizeReadme

# System arguments
# For local test purpose
# python {File.py} {access token} {blog name} {repository name}
# arguments = sys.argv
# blogAccessToken = arguments[1]
# blogName = arguments[2]
# repoName = arguments[3]
# repoOwner = arguments[4]
# gitAccessToken = arguments[5]


blogAccessToken = os.environ["INPUT_ACCESSTOKEN"]
blogName = os.environ["INPUT_BLOGNAME"]
Repo_Name = os.environ['GITHUB_REPOSITORY']
repoOwner = str(Repo_Name).split('/')[0]
repoName = str(Repo_Name).split('/')[1]
gitAccessToken = os.environ["INPUT_GITHUBTOKEN"]

postTitleByRepoName = '깃허브 리포지토리 요약: ' + repoName

global contents
contents = ''

def contents_generator():
    global contents
    
    ReadmeMDFile = getReadmeContents.get_readme_from_github(repoOwner, repoName)
    MDfile_plainText = summarizeReadme.process_markdown(ReadmeMDFile)
    summarizedReadmeText = summarizeReadme.generate_summary(MDfile_plainText)
    summarizedReadmeMD = markdown.markdown(summarizedReadmeText)
    #Title 
    contents += '<h1 style="border-left: 20px solid #bdb2ff; border-right: 20px solid #bdb2ff; background-color: #f8f9fa; padding: 15px; text-align: center; font-weight: bold;" data-ke-size="size26">'
    contents += repoName
    contents += '</h1>'
    
    #Table content
    contents += '<blockquote data-ke-style="style3"><b>목차</b><br /><a href="#Readme">1. ReadMe. md</a><br /><a href="#Commithistory">2. Commit History</a></blockquote>'
    
    #Summarized Readme.md
    contents += '<h2 id="Readme" style="padding: 5px; border-left: solid 20px #ffc6ff; border-bottom: solid 10px #ffc6ff; font-size: 25px; font-weight: bold;" data-ke-size="size26">ReadMe.md</h2>'
    contents += getReadmeContents.convert_md_to_html(summarizedReadmeMD)

    contents += '<hr>'
    contents += '<h2 id="Commithistory" style="padding: 5px; border-left: solid 20px #ffc6ff; border-bottom: solid 10px #ffc6ff; font-size: 25px; font-weight: bold;" data-ke-size="size26">Commit History</h2>'

    commits = readRepoCommits.get_commits(repoOwner, repoName, gitAccessToken)
    commitCounter = 1
    
    for commit in commits:
        if commit["commit"]["message"] != '':
            contents += '<p data-ke-size="size14"><a href = "'
            contents += commit["html_url"]
            contents += '">'
            contents += 'No. '
            contents += str(commitCounter)
            contents += ': '
            contents += commit["commit"]["message"]
            contents += '</a></p>'
            commitCounter = commitCounter + 1

def post_blog():
    global contents

    base_url = 'https://www.tistory.com/apis/post/write'
    parameters = {
        'access_token': blogAccessToken,
        'output': 'json',
        'blogName': blogName,
        'title': postTitleByRepoName,
        'content': contents,
        'visibility': '3',
        'category': 'Anything',
        'tag': 'Tistory API Post',
        'acceptComment': '1'
    }

    result = requests.post(base_url, data=parameters)
    print('####Edit Result Log####')
    print(result)

def edit_post(postID):
    global contents

    base_url = 'https://www.tistory.com/apis/post/modify'
    parameters = {
        'access_token': blogAccessToken,
        'output': 'json',
        'blogName': blogName,
        'postId': postID,
        'title': postTitleByRepoName,
        'content': contents,
        'visibility': '3',
        'category': 'Anything',
        'tag': 'Tistory API Post',
        'acceptComment': '1'
    }

    result = requests.post(base_url, data=parameters)
    print('####Edit Result Log####')
    print(result)

def check_postExist():
    base_url = 'https://www.tistory.com/apis/post/list'
    repoExist = False
    postID = ""

    contents_generator()

    for i in range(1, 100):
        parameters = {
            'access_token': blogAccessToken,
            'output': 'json',
            'blogName': blogName,
            'page': i
        }
        
        listData = requests.get(base_url, params=parameters)
        result = json.loads(listData.text)
        print(result)

        try:
            for item in result["tistory"]["item"]["posts"]:
                if item["title"] == postTitleByRepoName:
                    print('Repository post already exists -> Edit')
                    #print existing URL
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
            
if __name__ == "__main__":      
    check_postExist()
