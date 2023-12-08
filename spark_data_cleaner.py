from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, to_date, collect_list, regexp_replace
import os
import time

def readAndCleanData(spark, path):
    # Read JSON data into a Spark DataFrame
    df = spark.read.json(path)

    # Explode the comments array into individual rows
    df = df.withColumn("comment", explode(col("comments")))

    # Convert timestamp to date and remove non-alphanumeric characters from comments
    df = df.withColumn("date", to_date("timestamp", "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")) \
           .withColumn("comment", regexp_replace(col("comment"), "[^a-zA-Z0-9\\s]", ""))

    # Group by date and collect comments into a list
    df = df.groupBy("date").agg(collect_list("comment").alias("comments"))

    return df

def saveData(df, company, output_folder, output_format):
    # Create the output folder if it doesn't exist
    output_path = os.path.join(output_folder, f"{company}_Merged.{output_format}")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save DataFrame in the specified format
    if output_format == "csv":
        df.write.option("header", "true").csv(output_path)

def processCompanies(spark, companies):
    for company in companies:
        # Define paths for Instagram and TikTok data
        ig_path = f"raw_data/instagram/ig_{company}_comments.json"
        tt_path = f"raw_data/tiktok/tt_{company}_comments.json"

        # Read and clean both datasets
        ig_df = readAndCleanData(spark, ig_path)
        tt_df = readAndCleanData(spark, tt_path)

        # Merge Instagram and TikTok data
        all_data_df = ig_df.union(tt_df)

        # Save data in CSV format in specified folders
        saveData(all_data_df, company, "CleanedAndMergedData", "csv")
        saveData(all_data_df, company, "SentimentAnalysis", "csv")

def main():
    # Start measuring time
    start_time = time.time()

    # Initialize a Spark session
    spark = SparkSession.builder.appName("SocialMediaCommentsProcessing").getOrCreate()

    # List of companies
    companies = ["Starbucks", "Target", "Nike"]
    processCompanies(spark, companies)

    # Stop the Spark session
    spark.stop()

    # Calculate and print execution duration
    end_time = time.time()
    duration = end_time - start_time
    print(f"Execution time: {duration:.2f} seconds")

if __name__ == '__main__':
    main()
