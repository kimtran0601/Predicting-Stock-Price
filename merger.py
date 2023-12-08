import os
import csv
from collections import defaultdict

# Define input and output folders
input_folder = "csv_data"
output_folder = "merged_data"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Initialize a defaultdict to store comments by date for each company
comments_by_company = defaultdict(lambda: defaultdict(list))

# Define the list of company names
companies = ["starbucks", "target", "nike"]

# Iterate through the files in the input folder
for company_name in companies:
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".csv") and company_name in filename:
                input_path = os.path.join(root, filename)
                
                # Read the CSV file
                with open(input_path, mode='r', encoding='utf-8') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    next(csv_reader)  # Skip the header row
                    
                    for row in csv_reader:
                        date, comment = row
                        comments_by_company[company_name][date].append(comment)

# Create merged output files for each company
for company_name, comments_by_date in comments_by_company.items():
    output_path = os.path.join(output_folder, f"{company_name}_merged_comments.csv")

    # Write the merged comments to the output file
    with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
        csv_writer = csv.writer(outfile)
        
        # Write the header row
        csv_writer.writerow(["Date", "Comments"])
        
        # Write the merged comments for each date
        for date, comments in comments_by_date.items():
            csv_writer.writerow([date, ', '.join(comments)])

    print(f"Merged comments for {company_name} saved to {output_path}")
