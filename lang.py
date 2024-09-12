import numpy as np
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

vectors = np.load("../vecs.npy")
print(vectors.shape)

embeddings = HuggingFaceEmbeddings(model_name="deepvk/USER-bge-m3")
index = faiss.IndexFlatL2(vectors.shape[1])

res = faiss.StandardGpuResources()
index = faiss.index_cpu_to_gpu(res, 0, index)
index.add(vectors)

documents = [
    Document(page_content=f"Document {i}") for i in range(vectors.shape[0])
]

docstore = InMemoryDocstore({str(i): doc for i, doc in enumerate(documents)})

index_to_docstore_id = {i: str(i) for i in range(vectors.shape[0])}

vec_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=docstore,
    index_to_docstore_id=index_to_docstore_id,
)

results = vec_store.similarity_search(
    "Какие внутренние черты и конфликты присущи князю Андрею Болконскому, как они меняются на протяжении романа",
    k=4,
)


for result in results:
    print(result)

with open("../tolst.txt", 'r') as file:
    lines = file.read()

parts = lines.split('.')
parts = [part.strip() for part in parts if part.strip()]
print(parts[10931])
print("------------------")
print(parts[5825])
print("------------------")
print(parts[2858])
print("------------------")
print(parts[16393])