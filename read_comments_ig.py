import json
import re
import emoji

urls = dict()

with open("data/ig_target_comments.json") as data_file:
    data = json.load(data_file)

    newData = json.dumps(data, indent=4, ensure_ascii=False)
            
with open("data/ig_target_comments_modified.json", "w") as outfile:
    outfile.write(newData)
    print(newData, file=outfile)