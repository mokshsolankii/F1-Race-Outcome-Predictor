import requests
import json

url = "https://claude.ai/api/shared_conversations/14f9bb3e-52e0-4064-bd4a-8d6b04afa002"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}

try:
    response = requests.get(url, headers=headers)
    print("Status Code:", response.status_code)
    if response.status_code == 200:
        data = response.json()
        with open("C:/Users/moksh/.gemini/antigravity/brain/ee26e5fb-f672-40cc-8109-bae8616c62a2/scratch/claude_chat.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print("Success! Saved to claude_chat.json")
    else:
        print("Response body:", response.text[:500])
except Exception as e:
    print("Error:", e)
