from sentence_transformers import SentenceTransformer

# load only once
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(texts):
    return model.encode(texts)