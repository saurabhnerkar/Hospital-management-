from chatbot.ai.embedder import get_embedding_model

model = get_embedding_model()

vector = model.embed_query("Hello Hospital")

print(type(vector))

print(len(vector))

print(vector[:10])