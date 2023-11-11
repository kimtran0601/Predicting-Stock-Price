import json
import re
import emoji
import pandas as pd

urls = dict()
dates = dict()

with open("data/ig_target_comments.json") as data_file:
    data = json.load(data_file)

    for url in data:
        date = data[url]["timestamp"][0:10]
   
        if date not in dates:
            dates[date] = dict()
            dates[date]["comments"] = []


    
        for comment in data[url]["comments"]:
            # Remove emojis from the text
            filtered_text = emoji.replace_emoji(comment, replace='')
            dates[date]["comments"].append(filtered_text)
                
with open("data/cleaned_data/tiktok/target_full_comments_cleaned.json") as data_file:
    data = json.load(data_file)

    for url in data:
        date = data[url]["timestamp"][0:10]
   
        if date not in dates:
            dates[date] = dict()
            dates[date]["comments"] = []

        for comment in data[url]["comments"]:
            # Remove emojis from the text
            filtered_text = emoji.replace_emoji(comment, replace='')
            dates[date]["comments"].append(filtered_text)
        




df = pd.DataFrame(dates)
df = (df.T)
df.to_excel('target.xlsx')

#formatted_data = json.dumps(urls, indent=4)
#with open("data/cleaned_data/nike_full_comments_cleaned_ig.json", "w") as outfile:
 #       print(formatted_data, file=outfile)