# trAIvel

trAIvel is an intelligent, agentic travel recommendation system that combines multiple AI technologies to provide accurate, personalized travel suggestions. The system uses a hybrid approach: Retrieval-Augmented Generation (RAG) for curated destinations and Generative AI for broader coverage, ensuring both accuracy and flexibility.

<img width="1329" height="938" alt="Screenshot 2025-11-20 at 16 13 25" src="https://github.com/user-attachments/assets/e269c896-29ce-494d-a56d-3c31262f5ee3" />

# Simple use
Simply type a destination and click search (like on basic Google page). The app will 
1. search for the actual weather (OpenWeather API)
2. gets 15 activities that are suitable in the destination in the current weather (Gemini)
3. searches for the appropriate image and url for the activity (Google Places API)
   
User can hover over the cards and see the description of the activity. Clicking it will take user to the link of the activity (or at least its location in Google Maps).
The less known locations have been added via RAG, user can test Nitrianske Pravno and Zilina, places in Slovakia that didn't get very good results previously (mostly hallucinations) but via RAG we can see interesting activities for these places. Other places can be added later.

# Technologies

- Retrieval-Augmented Generation (RAG) - Ground truth for curated destinations
- Generative AI - Broad coverage with Gemini 2.0 Flash
- Multi-Agent Orchestration - Weather, RAG decision, generation, enrichment
- Intelligent Fallbacks - Graceful degradation at every layer
- Real-Time Enrichment - Photos and URLs from Google Places API
- This hybrid approach ensures accuracy for less-known destinations while maintaining flexibility for global coverage, creating a robust and reliable travel recommendation system.

# Architecture

More details can be found here: https://github.com/ZuzannaKurillova/trAIvel/blob/main/ARCHITECTURE.md

# Getting started

https://github.com/ZuzannaKurillova/trAIvel/blob/main/GETTING_STARTED.md
