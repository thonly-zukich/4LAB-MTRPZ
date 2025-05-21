import argparse
import requests

BASE_URL = "http://127.0.0.1:8000"

def get_random():
    response = requests.get(f"{BASE_URL}/random_cat")
    data = response.json()
    print("📷:", data["image_url"])
    print("📖:", data["fact"])

def get_top():
    response = requests.get(f"{BASE_URL}/top")
    data = response.json()
    for i, cat in enumerate(data, 1):
        print(f"\n#{i}:")
        print("📷:", cat["image_url"])
        print("📖:", cat["fact"])
        print("❤️:", cat["votes"])

def get_log():
    response = requests.get(f"{BASE_URL}/votes")
    data = response.json()
    for i, vote in enumerate(data, 1):
        print(f"\n[{vote['timestamp']}]")
        print("📷:", vote["image_url"])
        print("📖:", vote["fact"])

parser = argparse.ArgumentParser(description="CLI для Котопедії")
parser.add_argument("command", choices=["random", "top", "log"])
args = parser.parse_args()

if args.command == "random":
    get_random()
elif args.command == "top":
    get_top()
elif args.command == "log":
    get_log()
