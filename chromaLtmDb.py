import datetime
import json
import os

import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="./db")

openai_api_key = os.environ["TOKEN_OPENAI"]
openai_embedding = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,
    model_name="text-embedding-ada-002",
)

collection = client.get_or_create_collection(
    name="long-term-memory",
    metadata={"timestamp": "time", "role": "role"},
    embedding_function=openai_embedding,
)


def add_data(document, role):
    docs = [document]
    ids = [str(collection.count())]
    metadatas = [{"timestamp": str(datetime.datetime.now()), "role": role}]

    collection.add(ids=ids, metadatas=metadatas, documents=docs)

    return


def query_data(query_text, size):
    result = collection.query(
        query_texts=query_text, n_results=size, include=["metadatas", "documents"]
    )
    return result


def get_from_db(query_text):
    result = query_data(query_text, 10)
    return json.dumps(result)


if __name__ == "__main__":
    result = query_data("ラーメン", 10)
    print(result["documents"])
