# apps/backend/ai_agent.py

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from weather import get_weather

# Get API key from environment variable (no default for security)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY environment variable is not set. "
        "Please create a .env file in apps/backend/ with your API key."
    )

# Define a travel prompt with weather context
template = """What should I do and see in {destination}? Current weather information: {weather_info} Write me the list of top 15 activities without the title and in the JSON format with JSON objects that look like this: {{ "activity": "activity name", "description": "activity description", "link": "website" }}. Don't write json around it, just the array. No extra spaces. Use double quotes. Description shouldn't exceed 150 characters. Consider the current weather conditions when making recommendations."""

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
    """Return Gemini-generated travel recommendations with weather info"""
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

    print(f"INFO - Getting AI recommendation for {destination} with weather data")

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

