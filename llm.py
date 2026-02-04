from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
import httpx
import strings
from dotenv import load_dotenv
 
# Load environment variables from .env
load_dotenv()
 
def llm_call(user_prompt: str) -> str:
    base_url = os.getenv("API_ENDPOINT")
    api_key = os.getenv("API_KEY")
    model = os.getenv("LLM_MODEL")

    client = httpx.Client(verify=False)
 
    # Initialize the OpenAI chat model
    llm = ChatOpenAI(
        base_url=base_url,
        model=model,
        api_key=api_key,
        http_client=client
    )

    system_msg = SystemMessage(content=strings.LLM_SYSTEM_PROMPT)
    user_msg = HumanMessage(content=user_prompt)
 
    # Call the LLM
    try:
        response = llm.invoke([system_msg, user_msg])
        return response.content
    except Exception as e:
        print(f"LLM call failed: {e}")
        return f"The following exception occured while calling the LLM {model}: {e}"
 
if __name__ == "__main__":
    user_prompt = "Who are the major topic that are required for knowledge on developing AI Agnets"
    llm_response = llm_call(user_prompt)
    print(llm_response)