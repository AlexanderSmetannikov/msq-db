# import pdfplumber

# # def pdf_to_text(pdf_path):
# #     pdf_doc = fitz.open(pdf_path)
# #     lines = []
# #     for page_num in range(len(pdf_doc)):
# #         page = pdf_doc.load_page(page_num)
# #         text = page.get_text("text")
# #         lines.extend(text.split("\n"))
# #     return text


# def pdf_to_text(pdf_path):
#     lines = []
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             page_txt = page.extract_text()
#             if page_txt:
#                 lines.extend(page_txt.split("\n"))
#     return lines


# text = pdf_to_text("tolst.pdf")

# with open("tolst.txt", 'w') as f:
#     f.write(text)
# # for page in text:
# #     print(page)

with open("tolst.txt", 'r') as file:
    lines = file.read()

parts = lines.split('.')
parts = [part.strip() for part in parts if part.strip()]
print(parts[24172])