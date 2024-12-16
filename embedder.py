from sentence_transformers import SentenceTransformer
import pdfplumber
import numpy as np

# def pdf_to_text(pdf_path):
#     lines = []
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             page_txt = page.extract_text()
#             if page_txt:
#                 lines.extend(page_txt.split("\n"))
#     return lines
#
parts = ["Кому князь Василий был обязан своими первыми шагами по службе?"]
# text = pdf_to_text("ch.pdf")
# with open("tolst.txt", 'r') as file:
#     lines = file.read()

# parts = lines.split('.')
# parts = [part.strip() for part in parts if part.strip()]

model = SentenceTransformer("deepvk/USER-bge-m3", device='cuda')
# model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens", device='cuda')
embeddings = model.encode(parts, batch_size=32, normalize_embeddings=True, device="cuda") 

# with open("vecs.txt", 'w') as file:
#     file.write(np.array2str(embeddings))

np.save('../query.npy', embeddings)
