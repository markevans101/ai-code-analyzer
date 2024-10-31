import requests
import json
from config import TOGETHER_API_KEY

def test_together():
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Test with a simple completion
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": "Analyze this code:\n\ndef hello():\n    print('Hello, World!')\n\nProvide feedback.",
        "max_tokens": 512,
        "temperature": 0.7,
    }
    
    response = requests.post(
        "https://api.together.xyz/v1/completions",
        headers=headers,
        json=data
    )
    
    print("\nAPI Response:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("Testing Together AI API...")
    test_together()
