from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import json
from dotenv import load_dotenv
import os

load_dotenv()


qdrant_api_url = os.getenv("QDRANT_API_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

qdrant_client = QdrantClient(
    url=qdrant_api_url,
    api_key=qdrant_api_key
)


collection_name = "course_data"

if not qdrant_client.collection_exists(collection_name=collection_name):
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )


model = SentenceTransformer("all-MiniLM-L6-v2")

with open('structured_content_data.json', 'r', encoding='utf-8') as structured_data:
    data = json.load(structured_data)


points = []

for idx, item in enumerate(data):
    combined_text = item["title"] + " " + item["Description"]
    embedding = model.encode(combined_text).tolist()

    points.append(
        PointStruct(
            id=idx,
            vector=embedding,
            payload={
                "title": item["title"],
                "description": item["Description"],
                "link": item["url"],
                "Job levels": item.get("Job levels", ""),
                "Languages": item.get("Languages", ""),
                "Assessment length": item.get("Assessment length", ""),
                "remote_testing":item.get("remote_testing",""),
                "adaptive_irt":item.get("adaptive_irt","")
            }
        )
    )


def chunk_data(data, size=50):
    for i in range(0, len(data), size):
        yield data[i:i + size]

for chunk in chunk_data(points, size=50):
    qdrant_client.upsert(
        collection_name=collection_name,
        points=chunk
    )

print("All data upserted to Qdrant successfully.")
