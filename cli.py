import argparse
import requests

BASE_URL = "http://127.0.0.1:8000"

def get_random():
    response = requests.get(f"{BASE_URL}/random_cat")
    data = response.json()
    print("Image:", data["image_url"], flush=True)
    print("Fact:", data["fact"], flush=True)

def get_top():
    response = requests.get(f"{BASE_URL}/top")
    data = response.json()
    for i, cat in enumerate(data, 1):
        print(f"\n#{i}:", flush=True)
        print("Image:", cat["image_url"], flush=True)
        print("Fact:", cat["fact"], flush=True)
        print("Votes:", cat["votes"], flush=True)

def get_log():
    response = requests.get(f"{BASE_URL}/votes")
    data = response.json()
    for vote in data:
        print(f"\nTime: {vote['timestamp']}", flush=True)
        print("Image:", vote["image_url"], flush=True)
        print("Fact:", vote["fact"], flush=True)

def vote_random():
    # Отримуємо кота
    cat = requests.get(f"{BASE_URL}/random_cat").json()
    # Голосуємо
    vote_response = requests.post(f"{BASE_URL}/vote", json={
        "image_url": cat["image_url"],
        "fact": cat["fact"]
    })

    if vote_response.status_code == 200:
        print("\nSuccess: Vote recorded", flush=True)
        print("Image:", cat["image_url"], flush=True)
        print("Fact:", cat["fact"], flush=True)
    else:
        print("Error: Voting failed", flush=True)

# CLI логіка
parser = argparse.ArgumentParser(description="CLI для Котопедії")
parser.add_argument("command", choices=["random", "top", "log", "vote"])
args = parser.parse_args()

if args.command == "random":
    get_random()
elif args.command == "top":
    get_top()
elif args.command == "log":
    get_log()
elif args.command == "vote":
    vote_random()
