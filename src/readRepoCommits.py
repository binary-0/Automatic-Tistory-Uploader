import requests

def get_commits(_repoOwner, _repoName_Request, _git_access_token):
    #Must be modified
    repoOwner = _repoOwner
    repoName_Request = _repoName_Request
    git_access_token = _git_access_token

    api_url = f"https://api.github.com/repos/{repoOwner}/{repoName_Request}/commits"

    headers = {
        "Authorization": f"Bearer {git_access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    commitsList = []
    commitPage = 1
    while True:
        params= {"page": commitPage}
        git_response = requests.get(api_url, headers=headers, params=params)    

        if git_response.status_code == 200:
            commits = git_response.json()
            if not commits:
                break #No more commits, search is done
            commitsList.extend(commits)
            commitPage = commitPage + 1
        else:
            print("Error")
            break

    return commitsList