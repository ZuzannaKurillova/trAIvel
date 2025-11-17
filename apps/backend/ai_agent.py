# apps/backend/ai_agent.py

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Get API key from environment variable (no default for security)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY environment variable is not set. "
        "Please create a .env file in apps/backend/ with your API key."
    )

# Define a travel prompt
template = "You are a travel assistant. Suggest activities and must-see places in {destination}."
prompt = PromptTemplate(input_variables=["destination"], template=template)

# Instantiate the LLM using Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)

# Modern LangChain approach using LCEL (LangChain Expression Language)
chain = prompt | llm

def get_ai_recommendation(destination: str) -> str:
    """Return AI-generated travel recommendations for a given destination"""
    try:
        result = chain.invoke({"destination": destination})
        return result.content
    except Exception as e:
        return f"Error getting recommendation: {str(e)}"
