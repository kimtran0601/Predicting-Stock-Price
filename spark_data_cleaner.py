import time 
# Record the start time
start_time = time.time()

from pyspark.sql import SparkSession
from pyspark.sql.functions import collect_list, concat_ws, col, to_date
import os

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Merging Comments") \
    .getOrCreate()

# Define input and output folders
input_folder = "csv_data"
output_folder = "merged_data"

# Define the list of company names
companies = ["starbucks", "target", "nike"]


# Iterate through companies
for company_name in companies:
    # Read CSV files for the current company
    df_list = []
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".csv") and company_name in filename:
                input_path = os.path.join(root, filename)

                # Read CSV and select relevant columns
                df = spark.read.option("header", "true").csv(input_path)
                df = df.select("Date", "Comment")

                df_list.append(df)

    # Concatenate DataFrames for the current company
    if df_list:
        merged_df = df_list[0]
        for i in range(1, len(df_list)):
            merged_df = merged_df.union(df_list[i])

        # Group by date and aggregate comments
        merged_df = merged_df.groupBy("Date").agg(concat_ws(", ", collect_list("Comment")).alias("Comment"))

        # Save the merged DataFrame as a CSV file
        output_path = f"{output_folder}/{company_name}_merged_comments.csv"
        merged_df.write.option("header", "true").csv(output_path)

        print(f"Merged comments for {company_name} saved to {output_path}")

# Stop the Spark Session
spark.stop()

# Record the end time
end_time = time.time()

# Calculate and print the execution time
execution_time = end_time - start_time
print(f"Execution Time: {execution_time} seconds")
