import markdown
import requests

def convert_md_to_html(md_content):
    html_content = markdown.markdown(md_content, extensions=['markdown.extensions.tables'])
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