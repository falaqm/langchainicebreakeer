import requests
import json
from dotenv import load_dotenv
load_dotenv()
import os

api_key = os.getenv("PROXY_CURL")
headers = {"Authorization": "Bearer " + api_key}
api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
params = {
    "linkedin_profile_url": "https://linkedin.com/in/eden-marco/",
    "extra": "include",
    "github_profile_id": "include",
    "facebook_profile_id": "include",
    "twitter_profile_id": "include",
    "personal_contact_number": "include",
    "personal_email": "include",
    "inferred_salary": "include",
    "skills": "include",
    "use_cache": "if-present",
    "fallback_to_cache": "on-error",
}
response = requests.get(api_endpoint, params=params, headers=headers)
content = response.json()

with open("eden_marco_1.json", "w") as outfile:
    json.dump(content, outfile)
