from app.constants.prompt import prompt
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

def build_prompt(context, query):
    return prompt.format(
        context = context, 
        query = query
    )
    
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