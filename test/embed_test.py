# from langchain_huggingface.embeddings import HuggingFaceEmbeddings

# embeddings = HuggingFaceEmbeddings(
#     model_name="intfloat/multilingual-e5-small",
#     model_kwargs={"device": "mps"}
# )

# result = embeddings.embed_query("ayam 2 potong")

# print(len(result))
# print(result[:5])

# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer(
#     "intfloat/multilingual-e5-large", 
#     device="mps"
# )

# result = model.encode("ayam 2 potong", normalize_embeddings=True)

# print(len(result))
# print(result[:5])