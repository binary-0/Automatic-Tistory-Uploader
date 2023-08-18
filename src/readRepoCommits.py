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

    git_response = requests.get(api_url, headers=headers)

    if git_response.status_code == 200:
        commits = git_response.json()
        print("Total commits:", len(commits))

        # Print commit messages
        return commits
    else:
        print("Error:", git_response.status_code)
        return 0

    # lines = subprocess.check_output(
    #     ['git', 'log'], stderr=subprocess.STDOUT
    # ).decode("utf-8").split('\n')
    # commits = []
    # current_commit = {}

    # def save_current_commit():
    #     title = current_commit['message'][0]
    #     message = current_commit['message'][1:]
    #     if message and message[0] == '':
    #         del message[0]
    #     current_commit['title'] = title
    #     current_commit['message'] = '\n'.join(message)
    #     commits.append(current_commit)

    # for line in lines:
    #     if not line.startswith(' '):
    #         if line.startswith('commit '):
    #             if current_commit:
    #                 save_current_commit()
    #                 current_commit = {}
    #             current_commit['hash'] = line.split('commit ')[1]
    #         else:
    #             try:
    #                 key, value = line.split(':', 1)
    #                 current_commit[key.lower()] = value.strip()
    #             except ValueError:
    #                 pass
    #     else:
    #         current_commit.setdefault(
    #             'message', []
    #         ).append(leading_4_spaces.sub('', line))
    # if current_commit:
    #     save_current_commit()

    # return commits
    # for commit in commits:
    #     if commit["message"] != '':
    #         print(commit["message"])