import json
import re
import os
import csv
from datetime import datetime

# Function to clean a comment
def clean_comment(comment):
    # Remove emojis and non-alphanumeric characters
    cleaned_comment = re.sub(r'[^a-zA-Z0-9\s]', '', comment)
    
    # Normalize whitespace and remove extra spaces
    cleaned_comment = ' '.join(cleaned_comment.split())
    
    # Remove comments that don't contain English words
    english_words = re.findall(r'\b[a-zA-Z]+\b', cleaned_comment)
    cleaned_comment = ' '.join(english_words)
    
    return cleaned_comment

# Function to process, clean the data, and save as CSV with each comment on a new row
def process_and_clean_data_to_csv(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through Instagram and TikTok folders
    for platform_folder in ["instagram", "tiktok"]:
        platform_input_folder = os.path.join(input_folder, platform_folder)
        platform_output_folder = os.path.join(output_folder, platform_folder)

        # Ensure the platform output folder exists
        os.makedirs(platform_output_folder, exist_ok=True)

        # Iterate through files in the platform input folder
        for filename in os.listdir(platform_input_folder):
            if filename.endswith(".json"):
                input_path = os.path.join(platform_input_folder, filename)
                output_path = os.path.join(platform_output_folder, filename.replace('.json', '.csv'))

                with open(input_path, "r") as infile, open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
                    try:
                        data = json.load(infile)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in file {input_path}: {e}")
                        continue  # Skip this file if JSON is invalid

                    csv_writer = csv.writer(outfile)
                    
                    # Write the header for the CSV file
                    csv_writer.writerow(["Date", "Comment"])

                    for url, info in data.items():
                        # Convert timestamp to 'MM-DD-YYYY' format
                        date = datetime.strptime(info["timestamp"].split('T')[0], "%Y-%m-%d").strftime("%m-%d-%Y")
                        for comment in info["comments"]:
                            cleaned_comment = clean_comment(comment)
                            if cleaned_comment:  # Write only non-empty comments
                                csv_writer.writerow([date, cleaned_comment])

# Specify input and output folders
input_folder = "raw_data"
output_folder = "csv_data"

# Process and clean the data and convert to CSV
process_and_clean_data_to_csv(input_folder, output_folder)
