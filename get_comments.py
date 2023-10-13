from apify_client import ApifyClient
import json

# Initialize the ApifyClient with your API token
# client = ApifyClient("apify_api_uSIyHxzUx667snZJ2mMDrSEU0Cxk6E0dmXHd")

# Prepare the Actor input
run_input = {
    "directUrls": ["https://www.instagram.com/nike/"],
    "resultsType": "details",
    "resultsLimit": 1,
    "searchType": "user",
    "searchLimit": 1,
}

# # Run the Actor and wait for it to finish
# run = client.actor("apify/instagram-api-scraper").call(run_input=run_input)

# for item in client.dataset(run["defaultDatasetId"]).iterate_items():
#     j = json.dumps(item, indent=2)

# l = []
# for value in j.lastestPosts:
#     l.append(value)

# print(l)
# with open("sample.json", "w") as outfile:
#     outfile.write(j)

f = open('sample.json')
data = json.load(f)

l = []
for post in data['latestPosts']:
    l.append(post["url"])

print(l)