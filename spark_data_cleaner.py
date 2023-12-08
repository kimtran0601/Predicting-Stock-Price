# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, col
import os

# Function to process data for each company
def processCompanies(spark, companies):
    for company in companies:
        # Define paths for Instagram and TikTok data
        ig_path = f"raw_data/instagram/ig_{company}_comments.json"
        tt_path = f"raw_data/tiktok/tt_{company}_comments.json"

        # Read Instagram data into a Spark DataFrame
        ig_df = spark.read.json(ig_path)
        # Read TikTok data into a Spark DataFrame
        tt_df = spark.read.json(tt_path)

        # Iterate over both DataFrames to clean and merge
        for df in [ig_df, tt_df]:
            # Convert timestamp to date and clean comments by removing non-alphanumeric characters
            df = df.withColumn("timestamp", col("timestamp").cast("date")) \
                   .withColumn("comments", regexp_replace(col("comments"), "[^a-zA-Z0-9\\s]", "")) \
                   .groupBy("timestamp").agg(collect_list("comments").alias("comments"))

            # Merge Instagram and TikTok data
            all_data_df = ig_df.union(tt_df)

        # Define the output path for CSV files
        csv_output_path = f"CleanedAndMergedData/{company}_Merged"
        # Create the directory if it doesn't exist
        if not os.path.exists(csv_output_path):
            os.makedirs(csv_output_path)
        # Write the DataFrame to CSV
        all_data_df.write.option("header", "true").csv(csv_output_path)

        # For Excel output, convert to Pandas DataFrame
        # Define the output path for Excel files
        excel_output_path = f"SentimentAnalysis/{company}_Merged.xlsx"
        # Create the directory if it doesn't exist
        if not os.path.exists("SentimentAnalysis"):
            os.makedirs("SentimentAnalysis")
        # Convert Spark DataFrame to Pandas DataFrame
        pandas_df = all_data_df.toPandas()
        # Write the Pandas DataFrame to Excel
        pandas_df.to_excel(excel_output_path, index=False)

# Initialize a Spark Session
spark = SparkSession.builder.appName("CommentsProcessing").getOrCreate()

# List of companies to process
companies = ["Starbucks", "Target", "Nike"]
# Process each company
processCompanies(spark, companies)
