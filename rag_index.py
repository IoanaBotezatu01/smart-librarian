import json
import os
import argparse
from typing import List, Dict

import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

DATA_PATH = os.path.join("data", "book_summaries.json")
CHROMA_PATH = os.path.join("chroma")
COLLECTION_NAME = "book_summaries"


def load_data() -> List[Dict]:
    """Load book summaries dataset from JSON file."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_collection():
    """Rebuild ChromaDB collection from scratch using book summaries."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    embed_model = os.getenv("EMBED_MODEL", "text-embedding-3-small")

    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in .env file")

    # Create persistent Chroma client
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # OpenAI embedding function
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name=embed_model,
    )

    # Delete old collection (if exists) and create new one
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=openai_ef,
    )

    # Load and insert data
    rows = load_data()
    ids, docs, metas = [], [], []

    for i, row in enumerate(rows):
        ids.append(f"book-{i}")
        docs.append(
            f"Title: {row['title']}\n"
            f"Summary: {row['short_summary']}\n"
            f"Themes: {', '.join(row['themes'])}"
        )
        metas.append({"title": row["title"], "themes": row["themes"]})

    collection.add(ids=ids, documents=docs, metadatas=metas)
    print(f"✔ Loaded {len(ids)} documents into collection '{COLLECTION_NAME}' at {CHROMA_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rebuild", action="store_true", help="Rebuild the index from scratch"
    )
    args = parser.parse_args()

    if args.rebuild:
        build_collection()
    else:
        # Lazy build if index is missing
        if not os.path.isdir(CHROMA_PATH) or not os.listdir(CHROMA_PATH):
            print("Index not found – building now...")
            build_collection()
        else:
            print("Index already exists – nothing to do.")
