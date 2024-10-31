import requests
from urllib.parse import urlparse

def validate_github_url(url):
    """Validate and parse a GitHub repository URL."""
    try:
        parsed = urlparse(url)
        
        # Check if it's a GitHub URL
        if 'github.com' not in parsed.netloc:
            return False, "Not a GitHub URL"
            
        # Extract owner and repo name from path
        parts = parsed.path.strip('/').split('/')
        if len(parts) < 2:
            return False, "Invalid repository path"
            
        return True, {
            'owner': parts[0],
            'repo': parts[1]
        }
    except Exception as e:
        return False, f"Error parsing URL: {str(e)}"

def get_repo_info(url):
    """Get basic information about a GitHub repository."""
    # First validate the URL
    is_valid, result = validate_github_url(url)
    if not is_valid:
        print(f"Error: {result}")
        return None
        
    # GitHub API endpoint
    api_url = f"https://api.github.com/repos/{result['owner']}/{result['repo']}"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return {
                'name': data['name'],
                'description': data['description'],
                'stars': data['stargazers_count'],
                'language': data['language'],
                'created_at': data['created_at'],
                'last_updated': data['updated_at'],
                'topics': data.get('topics', []),
                'url': data['html_url']
            }
        else:
            print(f"Error: Unable to fetch repository data (Status code: {response.status_code})")
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Test the function
if __name__ == "__main__":
    test_url = "https://github.com/langchain-ai/langchain"
    repo_info = get_repo_info(test_url)
    if repo_info:
        print("\nRepository Information:")
        for key, value in repo_info.items():
            print(f"{key}: {value}")
