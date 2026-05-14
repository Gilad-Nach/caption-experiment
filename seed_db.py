import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

# --- Load your CSV ---
# TODO: Replace with the actual path to your CSV file
CSV_PATH = "csv_for_website.csv"  # <-- put your CSV filename here

df = pd.read_csv(CSV_PATH)

# Keep only the columns we need
df = df[["image_url", "image_id", "caption", "error_type"]]

# Drop any rows with missing values in these columns
df = df.dropna(subset=["image_url", "image_id", "caption", "error_type"])

# --- Preview before inserting ---
print(f"Found {len(df)} rows")
print(f"Error type distribution:\n{df['error_type'].value_counts()}\n")

confirm = input("Proceed with seeding? (yes/no): ")
if confirm.lower() != "yes":
    print("Aborted.")
    exit()

# --- Clear existing stimuli (safe to re-run) ---
db.stimuli.delete_many({})

# --- Insert into MongoDB ---
records = df.to_dict(orient="records")
result = db.stimuli.insert_many(records)

print(f"✅ Inserted {len(result.inserted_ids)} stimuli into MongoDB")

# --- Verify distribution ---
pipeline = [{"$group": {"_id": "$error_type", "count": {"$sum": 1}}}]
distribution = list(db.stimuli.aggregate(pipeline))
print("\nDistribution in DB:")
for d in distribution:
    print(f"  {d['_id']}: {d['count']}")