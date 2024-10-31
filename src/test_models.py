import requests

def get_available_models(api_key):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get("https://api.together.xyz/models", headers=headers)
    return response.json()

if __name__ == "__main__":
    from config import TOGETHER_API_KEY
    models = get_available_models(TOGETHER_API_KEY)
    print("\nAvailable Models:")
    for model in models:
        if 'chat' in model.get('name', '').lower():
            print(f"- {model['name']}")
