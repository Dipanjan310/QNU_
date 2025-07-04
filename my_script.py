import requests
import numpy as np

def fetch_data():
    url = "https://api.github.com"
    response = requests.get(url)
    if response.status_code == 200:
        print("GitHub API is reachable!")
        print("Current Rate Limit Info:")
        print(response.json().get("rate_limit_url", "No info"))
    else:
        print("Failed to reach GitHub API.")

if __name__ == "__main__":
    fetch_data()
