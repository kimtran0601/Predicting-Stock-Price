from apify_client import ApifyClient
import json

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_KEjtWbDL1d7Bx0wRSGHuHJpqEmJAyE1Ixnbe")

posts = {}
list_of_urls = []

run_posts_input = {
        "scrapeLastNDays": 3,
        "profiles": ["starbucks"]
}

posts_run = client.actor("clockworks/tiktok-scraper").call(run_input=run_posts_input)

for item in client.dataset(posts_run["defaultDatasetId"]).iterate_items():
    url = item["webVideoUrl"]
    posts[url] = {}
    posts[url]["timestamp"] = item["createTimeISO"]
    posts[url]["comments"] = []
    list_of_urls.append(url)

run_comments_input = {
        "postURLs": list_of_urls,
        "commentsPerPost": 100,
        "maxRepliesPerComment": 0
    }

    # Run the Actor and wait for it to finish
comments_run = client.actor("clockworks/tiktok-comments-scraper").call(run_input=run_comments_input)

for comment in client.dataset(comments_run["defaultDatasetId"]).iterate_items():
     posts[comment["videoWebUrl"]]["comments"].append(comment["text"])

print(posts)
data = json.dumps(posts, indent=4)
with open("data/starbucks_comments.json", "w") as outfile:
        print(data, file=outfile)