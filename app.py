from flask import Flask, render_template, request
import requests
import os
from datetime import datetime, timezone

app = Flask(__name__)

TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAM2D0gEAAAAAUPcTIL%2F%2BMX08b92OKIkhifGwGzs%3DGVS6nlKP53y2m4SLJ6bmOrsejoMp9WNZoWbbr8PL8vjK03HKh5"

def get_tweets_by_keywords(keywords):
    query = " OR ".join(keywords)
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&tweet.fields=created_at,author_id&max_results=10"
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []

def get_username(user_id):
    url = f"https://api.twitter.com/2/users/{user_id}"
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]["username"]
    return "unknown"

def format_age(timestamp):
    tweet_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    delta = now - tweet_time
    return f"{int(delta.total_seconds())}s ago"

@app.route('/', methods=['GET', 'POST'])
def home():
    tweets = []
    handles = []
    keywords = []

    if request.method == 'POST':
        handles = request.form.get('handles', '').split(',')
        keywords = request.form.get('keywords', '').split(',')

        tweets = get_tweets_by_keywords([kw.strip() for kw in keywords if kw.strip()])
        for tweet in tweets:
            tweet["age"] = format_age(tweet["created_at"])
            tweet["username"] = get_username(tweet["author_id"])
            tweet["url"] = f"https://twitter.com/{tweet['username']}/status/{tweet['id']}"

    return render_template('index.html', tweets=tweets, handles=handles, keywords=keywords)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
