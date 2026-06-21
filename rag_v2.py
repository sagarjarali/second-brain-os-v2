import warnings
warnings.filterwarnings("ignore")
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.PersistentClient(path="./schemes")

collection = client.get_or_create_collection(name="schemes")

with open("schemes.json", "r") as file:
    text = file.read()

chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

print("Number of chunks found:", len(chunks))

if collection.count() == 0:
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk]
        )
    print("Schemes loaded into database successfully!")
else:
    print("Database already loaded. Skipping.")

def get_relevant_schemes(question):
    question_embedding = model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results = 2
    )
    return results['documents'][0]