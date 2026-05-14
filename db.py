from pymongo import MongoClient
from dotenv import load_dotenv
import os, random

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

def get_sample_stimuli(n_per_category=5):
    """
    Samples an equal number of stimuli from each error category.
    TODO: Once error categories are decided, n_per_category will determine
    how many come from each. Total shown = n_per_category * number_of_categories.
    Currently set to 4 as a placeholder.
    """
    # TODO: Replace with actual category names when decided
    # e.g. ERROR_CATEGORIES = ["missing_object", "wrong_color", "hallucination"]
    ERROR_CATEGORIES = ["Relation", "No Error", "Cardinality", "Attribute"]

    if ERROR_CATEGORIES is None:
        # Fallback: purely random sample of 20 until categories are defined
        pipeline = [{"$sample": {"size": 20}}]
        return list(db.stimuli.aggregate(pipeline))

    sample = []
    for category in ERROR_CATEGORIES:
        docs = list(db.stimuli.aggregate([
            {"$match": {"error_type": category}},
            {"$sample": {"size": n_per_category}}
        ]))
        sample.extend(docs)

    random.shuffle(sample)
    return sample

def save_response(participant_id, ratings):
    """Save a participant's full set of ratings to MongoDB."""
    from datetime import datetime, timezone
    db.responses.insert_one({
        "participant_id": participant_id,
        "submitted_at": datetime.now(timezone.utc),
        "ratings": ratings
    })