from apify_client import ApifyClient
import json

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_uSIyHxzUx667snZJ2mMDrSEU0Cxk6E0dmXHd")

# Prepare the Actor input
run_input = {
    "directUrls": ["https://www.instagram.com/nike/"],
    "resultsType": "posts",
    "resultsLimit": 50,
    "searchType": "user",
}

# Run the Actor and wait for it to finish
run = client.actor("apify/instagram-api-scraper").call(run_input=run_input)

d = {}
l = []
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    url = item["url"]
    d[url] = {}
    d[url]["timestamp"] = item["timestamp"]
    d[url]["comments"] = []
    l.append(url)

run_comments_input = {
    "directUrls": l,
    "resultsLimit": 50,
}

run_comments = client.actor("apify/instagram-comment-scraper").call(run_input=run_comments_input)


for comment in client.dataset(run_comments["defaultDatasetId"]).iterate_items():
    print(comment)
    d[comment["postUrl"]]["comments"].append(comment["text"])



with open("nike_comments.json", "w") as outfile:
    json.dumps(d, indent=4)
    
print("\n")
print(d)
