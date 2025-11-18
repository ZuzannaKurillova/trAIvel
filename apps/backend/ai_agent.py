# apps/backend/ai_agent.py

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from weather import get_weather
from rag_service import get_rag_recommendations
import json

# Get API key from environment variable (no default for security)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY environment variable is not set. "
        "Please create a .env file in apps/backend/ with your API key."
    )

# Define a travel prompt with weather context
template = """What should I do and see in {destination}? Current weather information: {weather_info}

CRITICAL: You must respond with ONLY a valid JSON array. No markdown, no code blocks, no explanations.

Return exactly 15 activities in this format:
[
  {{ "activity": "activity name", "description": "activity description", "link": "website URL" }}
]

Requirements:
- ONLY return the JSON array, nothing else
- NO markdown code blocks (no ```json or ```)
- Use double quotes for all strings
- Description max 150 characters
- Include a real website URL for each activity
- Consider the current weather: {weather_info}

Start your response with [ and end with ]"""

prompt = PromptTemplate(input_variables=["destination", "weather_info"], template=template)

# Instantiate the LLM using Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)

# Modern LangChain approach using LCEL (LangChain Expression Language)
chain = prompt | llm

def get_ai_recommendation(destination: str) -> str:
    """Return travel recommendations - from RAG if available, otherwise from Gemini"""
    
    # First, try to get recommendations from RAG database
    rag_activities = get_rag_recommendations(destination)
    
    if rag_activities:
        print(f"INFO - Using RAG data for {destination} ({len(rag_activities)} activities)")
        # Return RAG data as JSON string
        return json.dumps(rag_activities)
    
    # If not in RAG, use Gemini
    print(f"INFO - No RAG data found, using Gemini for {destination}")
    
    # Get weather data
    weather = get_weather(destination)

    # Format weather information
    if "error" not in weather:
        weather_info = (
            f"The current weather in {destination} is {weather['temperature']}°C, "
            f"{weather['description']}, humidity {weather['humidity']}%, "
            f"wind speed {weather['wind_speed']} m/s."
        )
    else:
        weather_info = f"Weather information is currently unavailable. Error: {weather.get('error', 'Unknown')}"

    print(f"INFO - Getting Gemini recommendation for {destination} with weather data")

    try:
        # Use LangChain to get recommendation
        prompt_input = {
            "destination": destination,
            "weather_info": weather_info
        }

        result = chain.invoke(prompt_input)
        return result.content
    except Exception as e:
        print(f"ERROR - Exception occurred: {e}")
        return f"Error getting recommendation: {e}"

