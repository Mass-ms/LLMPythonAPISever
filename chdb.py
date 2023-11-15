import os
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="./db")

openai_api_key = os.environ["TOKEN_OPENAI"]
openai_embedding = embedding_functions.OpenAIEmbeddingFunction(
    api_key = openai_api_key, model_name="text-embedding-ada-002",
)

collection = client.get_or_create_collection(
    name="memories",embedding_function=openai_embedding
)

memories = [
"2023-06-01 06:00:00 ミルクが残りわずかしかない",
"2023-06-01 06:10:00 コーンフレークが半分以上残っている",
"2023-06-01 06:30:00 子どもが朝食にコーンフレークにミルクをかけて食べている",
"2023-06-01 06:40:00 TVが付いている",
"2023-06-01 06:50:00 コンロの火が付いている",
"2023-06-01 06:55:00 コンロの火が消えている",
"2023-06-01 07:00:00 コーヒーポットがコーヒーでいっぱいになっている",
"2023-06-01 07:10:00 子供が今日の夕ご飯はカレーがいいと言っている",
"2023-06-01 07:15:00 カレールーの在庫がない",
"2023-06-01 07:20:00 たまねぎの在庫がない",
"2023-06-01 07:20:00 ニンジンは3本残っている",
"2023-06-01 07:20:00 鶏肉が少し残っている",
"2023-06-01 07:20:00 ジャガイモの在庫がない",
"2023-06-01 07:40:00 TVのスイッチがオフになった",
"2023-06-01 07:50:00 子どもが出かけた",
"2023-06-01 08:00:00 コーヒーポットが空になった"
]

documents = [] #テキストデータ
metadatas = [] #テキストデータに関連するデータ(検索時に利用できる)
ids = [] #documentに一意に振るID

for i, d in enumerate(memories):
  metadatas.append({
    "date":d[:19]})
  documents.append(d[20:])
  ids.append(f"id{i}")
  
for d, m, i in zip(documents, metadatas, ids):
  collection.add(
    documents=d, 
    metadatas=m,
    ids=i)
  
result = collection.query(
query_texts="今日の晩御飯の料理名を考えてください。",n_results=1)
print(result)
result_str = result['documents']