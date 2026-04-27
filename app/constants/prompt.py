from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template = """You are an academic assistant.

Use ONLY the context below to answer the question.
If the answer is not in the context, say "Not found in provided material".

Context:
{context}

Question:
{query}

Answer:
""",
input_variables=["context", "query"]
)
