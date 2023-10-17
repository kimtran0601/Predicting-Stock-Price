import json
import re
import emoji

urls = dict()

with open("data/startbucks_tiktok_comments.json") as data_file:
    data = json.load(data_file)

    for post in data:
        
        urlString = 'videoWebUrl'

        if('webVideoUrl') in post:
            urlString = 'webVideoUrl'
        
        if post[urlString] not in urls: 
            urls[post[urlString]] = dict()
            urls[post[urlString]]["comments"] = []
        
        urls[post[urlString]]["timestamp"] = post["createTimeISO"]
 
        # Remove emojis from the text
        filtered_text = emoji.replace_emoji(post["text"], replace='')
        print(filtered_text)
        urls[post[urlString]]["comments"].append(filtered_text)
            

formatted_data = json.dumps(urls, indent=4)
with open("data/starbucks_comments.json", "w") as outfile:
        print(formatted_data, file=outfile)