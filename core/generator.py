from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()
    
def get_llm(repo_id: str = "meta-llama/Meta-Llama-3-8B-Instruct") -> ChatHuggingFace:
    """Initialize HuggingFace LLM"""

    repo_id = repo_id or os.environ.getenv("HF_LLM_REPO_ID")
    endpoint = HuggingFaceEndpoint(
        repo_id=repo_id,
        task="text-generation",
        huggingfacehub_api_token= os.environ.getenv("HF_TOKEN"),
        max_new_tokens=1000,
        do_sample=False,
        temperature=0.7,
        top_p=0.9,
    )

    return ChatHuggingFace(llm=endpoint)

def generate_answer(query, repo_id: str = "meta-llama/Meta-Llama-3-8B-Instruct"):
    llm = get_llm(repo_id=repo_id)
    
    result = llm.invoke(query)
    
    return result.context