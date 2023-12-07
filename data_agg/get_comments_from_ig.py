from apify_client import ApifyClient
import json

# initialize the ApifyClient with your API token
client = ApifyClient("apify_api_uSIyHxzUx667snZJ2mMDrSEU0Cxk6E0dmXHd")

# fields
company = "target"

# prepare the post web scraper for instagram
run_input = {
    "directUrls": ["https://www.instagram.com/{company}/"],
    "resultsType": "posts",
    "resultsLimit": 1,
    "searchType": "user",
}

# Run the posts actor and wait for it to finish
run = client.actor("apify/instagram-api-scraper").call(run_input=run_input)

d = {} # maps url to comments and timestamp
l = [] # list of urls

# iterates through posts and saves url and timestamp
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    url = item["url"]
    d[url] = {}
    d[url]["timestamp"] = item["timestamp"]
    d[url]["comments"] = []
    l.append(url)

# inputs for comments scraper
run_comments_input = {
    "directUrls": l,
    "resultsLimit": 1,
}

# run comments scraper
run_comments = client.actor("apify/instagram-comment-scraper").call(run_input=run_comments_input)

# appends the comment to the corresponding url mapping
for comment in client.dataset(run_comments["defaultDatasetId"]).iterate_items():
    print(comment)
    d[comment["postUrl"]]["comments"].append(comment["text"])

# prints data to a json file
with open("ig_{}_comments.json".format(company), "w") as outfile:
    json.dump(d, outfile, indent=4)
