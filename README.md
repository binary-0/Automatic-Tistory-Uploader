# Introduction

**Automatic-Tistory-Uploader** is a github action that automatically posts information about repositories to Tistory blogs.

- This action automatically uploads:
  - **Summary of Repository** Utilizing the [NLTK](https://www.nltk.org) Module
  - **README.md** 
  - **Commit History** including commit messages, commit IDs, and corresponding URLs

- Automatically uploaded posts offer new visitors with a rapid, comprehensive overview of the repository's contents and history.

- It also empowers users to establish GitHub Events for the automatic uploading of posts to Tistory. (ex. Push, Pull requests ...)

## How To Use
We used Tistory Open API in this project. To find more information of the API, click on the [Link](https://tistory.github.io/document-tistory-apis/).

### Create Access Tokens
Firstly, create your Tistory blog and issue an token to access the blog.
See the follwing blog's instruction if you don't know how to issue a Tistory access token:
<https://joel-helloworld.tistory.com/59>

Then, we want you to store your access token in GitHub Secrets for security.

![image](https://github.com/binary-0/Automatic-Tistory-Uploader/assets/50437138/7ba417d5-7c01-478f-954c-b81ba7ebe655)

Go to repository setting and clink on 'Secrets and variables / Actions'.

![image](https://github.com/binary-0/Automatic-Tistory-Uploader/assets/50437138/881d25c8-1347-44bf-8c3b-fca0c492644c)

Then click the 'New repository secret' button, and add your Tistory access token.

![image](https://github.com/binary-0/Automatic-Tistory-Uploader/assets/50437138/aea3ea1e-1858-4154-9abe-0ccac79d55e9)

The name of the secret variable is up to you, but make sure it is recognizable for future use.

You don't have to worry about your GitHub access token. When GitHub Action is executed, it will be automatically moved by secret variable in order to read your README.md file and commit history.

In other words for newbies of GitHub Actions: Note that the `GITHUB_TOKEN` is **NOT** a personal access token. A GitHub Actions runner automatically creates a `GITHUB_TOKEN` secret to authenticate in your workflow. So, you can start to deploy immediately without any configuration.

### Set Up Your Repository
1. Create a folder named .github and create a workflows folder inside it, if it doesn't exist.
2. Create a new file named tistory-blog-action.yml with the following contents inside the workflows folder:
```
-----YML File here-------
```
3. Replace the above 'BlogName' with your own blog name. Tokens were processed on GitHub secret variable earlier, so you don't have to modify them.
4. You can initiate the process by either **git push** and allowing it to execute automatically, or you have the option to manually activate it for an immediate outcome using workflow_dispatch event.

## Inputs

| Input|	Description	| Default Value| Required |
|-|-|-|-|
|`Accesstoken`|Tstory Access token| | O |
|`BlogName`|Name of the Tstroy Blog|| O |
|`GithubToken`|Secret GITHUB_TOKEN|| O |
|~~`visibility`~~|~~Visibility of the Blog Post~~|`3`|X|
|~~`category`~~|~~Category ID~~|`0`| X|
|~~`acceptComment`~~|~~Allow comments to be written to post~~|`1`| X |
> **Note**: visibility, category, and acceptComment inputs are currently only available as default values and will be updated later

> Click [here](https://tistory.github.io/document-tistory-apis/apis/v1/post/write.html) to learn more about these inputs

## Technical Flow
![그림1](https://github.com/binary-0/Automatic-Tistory-Uploader/assets/50437138/fe5b3abe-ce2e-47fb-9f92-0055cda7dde1)

## Contributors

|<img alt="Jinyoung Lee" src="https://avatars.githubusercontent.com/u/50437138?v=4" width="100"/> | <img alt="Hyoje Sung" src="https://avatars.githubusercontent.com/u/77618270?v=4" width="100"/> |
|:-----:|:-----:|
| [Jinyoung Lee](https://github.com/binary-0) | [Hyoje Sung](https://github.com/Heukma)  |
