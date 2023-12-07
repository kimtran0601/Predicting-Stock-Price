import csv
import json
import emoji
import pandas as pd
from datetime import datetime

urls = dict()
dates = dict()

# fields used for setting which files to retrieve
company = "starbucks"
ig_path = "data/raw_data/instagram/ig_{}_comments.json".format(company)
tt_path = "data/raw_data/tiktok/tt_{}_comments.json".format(company)

# cleans data and inputs comments into one object
def getCleanedData(path):
    # iterate through instagram raw data
    with open(path) as data_file:
        data = json.load(data_file)
        
        for url in data:

            # format timestamp string
            date_string = data[url]["timestamp"]
            date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
            date_object = datetime.strptime(date_string, date_format)
            date_only_string = date_object.strftime("%Y-%m-%d")
            
            dates[url] = dict()
            dates[url]["timestamp"] = date_only_string
            dates[url]["comments"] = []
            for comment in data[url]["comments"]:
                
                # Remove emojis from the text
                filtered_text = emoji.replace_emoji(comment, replace='')
                dates[url]["comments"].append(filtered_text)
    
# clean both datasets    
getCleanedData(ig_path)
getCleanedData(tt_path) 

# reformat such that dates are the keys which maps to comments
merged = dict()
for post in dates:
    if dates[post]["timestamp"] not in merged:
        merged[dates[post]["timestamp"]] = list()
    
    for comment in dates[post]["comments"]:
        merged[dates[post]["timestamp"]].append(comment)

# output to csv
formatted_data = json.dumps(merged, indent=4)
with open("{}_merged.csv".format(company), "w") as outfile:
   writer = csv.writer(outfile)
   for key, value in merged.items():
        writer.writerow([key, value])