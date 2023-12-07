from apify_client import ApifyClient
import json

# initialize the ApifyClient with your API token
client = ApifyClient("apify_api_uSIyHxzUx667snZJ2mMDrSEU0Cxk6E0dmXHd")

# dict of posts and urls 
posts = {}
list_of_urls = []

# inputs/ specifications used
company = "target"


# params for web scrape data retrieval
run_posts_input = {
        "resultsPerPage": 1,
        "profiles": [company]
}

# initialize actor and run
posts_run = client.actor("clockworks/tiktok-scraper").call(run_input=run_posts_input)

# iterate through posts 
for item in client.dataset(posts_run["defaultDatasetId"]).iterate_items():
    
    url = item["webVideoUrl"]

    # map each url to respective comments and timestamp
    posts[url] = {}
    posts[url]["timestamp"] = item["createTimeISO"]
    posts[url]["comments"] = []

    # add url to list of urls
    list_of_urls.append(url)

# set up inputs for comments scraper
run_comments_input = {
        "postURLs": list_of_urls,
        "commentsPerPost": 1,
        "maxRepliesPerComment": 0
    }

# Run the comment actor
comments_run = client.actor("clockworks/tiktok-comments-scraper").call(run_input=run_comments_input)

# iterate through comments and append it to the corresponding video
for comment in client.dataset(comments_run["defaultDatasetId"]).iterate_items():
    posts[comment["videoWebUrl"]]["comments"].append(comment["text"])

# save output to json file
data = json.dumps(posts, indent=4)
with open("data/tiktok_target_comments.json", "w") as outfile:
    print(data, file=outfile)