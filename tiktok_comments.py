from apify_client import ApifyClient
import json

# Initialize the ApifyClient with your API token
# client = ApifyClient("apify_api_KEjtWbDL1d7Bx0wRSGHuHJpqEmJAyE1Ixnbe")
client = ApifyClient("apify_api_uSIyHxzUx667snZJ2mMDrSEU0Cxk6E0dmXHd")


posts = {}
list_of_urls = []

run_posts_input = {
        "resultsPerPage": 250,
        "profiles": ["target"]
}

posts_run = client.actor("clockworks/tiktok-scraper").call(run_input=run_posts_input)

for item in client.dataset(posts_run["defaultDatasetId"]).iterate_items():
    url = item["webVideoUrl"]
    posts[url] = {}
    posts[url]["timestamp"] = item["createTimeISO"]
    posts[url]["comments"] = []
    list_of_urls.append(url)

with open("data/tiktok_nike_posts.json") as data_file:
    data = json.load(data_file)
    url_field = "webVideoUrl"
    for item in data:
          list_of_urls.append(item[url_field])

print(list_of_urls)
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
with open("data/tiktok_target_comments.json", "w") as outfile:
        print(data, file=outfile)