import requests
import sys
import json
import os
import readRepoCommits
import markdown

#System arguments
#python {File.py} {access token} {blog name} {repository name}
#arguments = sys.argv

blogAccessToken = os.environ["INPUT_ACCESSTOKEN"]
blogName = os.environ["INPUT_BLOGNAME"]
Repo_Name = os.environ['GITHUB_REPOSITORY']
repoName = str(Repo_Name).split('/')[0]
repoOwner = str(Repo_Name).split('/')[1]
gitAccessToken = os.environ["INPUT_GITHUBTOKEN"]

# arguments = sys.argv
# blogAccessToken = arguments[1]
# blogName = arguments[2]
# repoName = arguments[3]
# repoOwner = arguments[4]
# gitAccessToken = arguments[5]

global contents
contents = ''

def convert_md_to_html(md_content):
    html_content = markdown.markdown(md_content)
    return html_content

def get_readme_from_github(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/README.md'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        readme_data = response.json()
        
        # Check if the response contains a 'content' key
        if 'content' in readme_data:
            import base64
            readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
            return readme_content
        else:
            print("README content not found in the response.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching README from GitHub: {e}")
        return None

def contents_generator():
    #ReadMe 읽고 맨 위에 쓰고
    global contents
    
    contents += convert_md_to_html(get_readme_from_github(repoOwner , repoName))
    
    commits = readRepoCommits.get_commits(repoOwner, repoName, gitAccessToken)
    commitCounter = 1
    
    for commit in commits:
        if commit["commit"]["message"] != '':
            contents += '<p>'
            contents += 'Commit message No. '
            contents += str(commitCounter)
            contents += ': '
            contents += commit["commit"]["message"]
            contents += '</p>'
            commitCounter = commitCounter + 1

def post_blog():
    global contents

    base_url = 'https://www.tistory.com/apis/post/write'
    parameters = {
        'access_token': blogAccessToken,
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
        'access_token': blogAccessToken,
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
