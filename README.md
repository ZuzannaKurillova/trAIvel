# trAIvel

<img width="1329" height="938" alt="Screenshot 2025-11-20 at 16 13 25" src="https://github.com/user-attachments/assets/e269c896-29ce-494d-a56d-3c31262f5ee3" />

trAIvel is an intelligent, agentic travel recommendation system that combines multiple AI technologies to provide accurate, personalized travel suggestions. The system uses a hybrid approach: Retrieval-Augmented Generation (RAG) for curated destinations and Generative AI for broader coverage, ensuring both accuracy and flexibility.
<img width="622" height="297" alt="Screenshot 2025-11-20 at 16 12 48" src="https://github.com/user-attachments/assets/8ab2cbae-0d6d-4c9e-9339-a9126a21bcad" />
<img width="622" height="297" alt="Screenshot 2025-11-20 at 16 12 58" src="https://github.com/user-attachments/assets/af6a4e05-6aab-4a85-92bb-34940cd55641" />
![IMG_2791](https://github.com/user-attachments/assets/9b4ddd42-9470-46c6-bcff-c2e62f2cdc8c)

# Technologies

Retrieval-Augmented Generation (RAG) - Ground truth for curated destinations
Generative AI - Broad coverage with Gemini 2.0 Flash
Multi-Agent Orchestration - Weather, RAG decision, generation, enrichment
Intelligent Fallbacks - Graceful degradation at every layer
Real-Time Enrichment - Photos and URLs from Google Places API
This hybrid approach ensures accuracy for less-known destinations while maintaining flexibility for global coverage, creating a robust and reliable travel recommendation system.

# 🤖 Agentic Components
1. Weather Intelligence Agent
Purpose: Provides real-time weather context for recommendations
Technology: OpenWeather API
Output: Temperature, conditions, humidity, wind speed
Integration: Weather data influences AI recommendations
2. RAG Decision Agent (Knowledge Retrieval)
Purpose: Determines whether to use curated data or generative AI
Technology: ChromaDB + Sentence Transformers
Decision Logic:
IF exact_match(destination):
    RETURN curated_data
ELSE IF semantic_similarity > 0.5:
    RETURN curated_data
ELSE:
    FALLBACK to Generative AI
Benefits: Prevents hallucinations for less-known destinations
3. Generative AI Agent
Purpose: Creates recommendations for destinations not in RAG database
Technology: Google Gemini 2.0 Flash
Context-Aware: Uses weather data to tailor suggestions
Output: 15 activities with descriptions and links
4. Content Enrichment Agent
Purpose: Enhances activities with real photos and official URLs
Technology: Google Places API
Process:
Search for each activity location
Fetch place details (photos, website, Google Maps URL)
Generate photo URLs with API key
Update activity data with real information

# 🧠 RAG (Retrieval-Augmented Generation) System

Two-Tier Matching Strategy

Tier 1: Exact String Match
Speed: O(n) - Fast linear search
Accuracy: 100% for exact matches
Case-insensitive: "Český Krumlov" = "český krumlov"
Use Case: User knows exact destination name

Tier 2: Semantic Search
Technology: Cosine similarity on 384-dim vectors
Threshold: Distance < 0.5 (strict to avoid false positives)
Use Case: Typos, variations, or related terms
Example: "Cesky Krumlov" (no diacritics) → "Český Krumlov"
Why This Matters
Problem: AI models like Gemini can "hallucinate" - generate plausible but incorrect information for less-known destinations.

Solution: RAG provides a ground truth knowledge base:

✅ Verified activities from local sources
✅ Accurate descriptions
✅ Real website links (enhanced by Places API)
✅ No hallucinations
Fallback: For destinations not in RAG, Gemini provides broad coverage while weather context improves relevance.

# 🔄 Request Flow
Detailed Step-by-Step Process
1. USER INPUT
   └─► "Nitrianske Pravno"
        │
        ▼
2. BACKEND RECEIVES REQUEST
   └─► FastAPI endpoint: /api/recommend?destination=Nitrianske+Pravno
        │
        ▼
3. WEATHER AGENT ACTIVATES
   └─► Calls OpenWeather API
   └─► Returns: {temperature: 15, description: "clear sky", ...}
        │
        ▼
4. RAG DECISION AGENT ACTIVATES
   │
   ├─► Step 1: Load all destinations from ChromaDB
   │   └─► collection.get() → All metadata
   │
   ├─► Step 2: Exact Match Check
   │   └─► "nitrianske pravno" == "nitrianske pravno" ✓
   │   └─► MATCH FOUND!
   │
   └─► Step 3: Return Curated Data
       └─► 15 activities from less_known_destinations_data.json
            │
            ▼
5. ENRICHMENT AGENT ACTIVATES
   │
   └─► For each activity:
       │
       ├─► Search Google Places API
       │   └─► Query: "Nitrianske Pravno, Main Square"
       │
       ├─► Fetch place details
       │   └─► Fields: ['name', 'photo', 'website', 'url']
       │
       ├─► Generate photo URL
       │   └─► https://maps.googleapis.com/maps/api/place/photo?...
       │
       └─► Update activity
           └─► activity['imgUrl'] = photo_url
           └─► activity['link'] = official_website || google_maps_url
            │
            ▼
6. RESPONSE ASSEMBLY
   └─► {
         "destination": "Nitrianske Pravno",
         "recommendation": "[{activity, description, link, imgUrl}, ...]",
         "weather": {temperature, description, humidity, wind_speed}
       }
        │
        ▼
7. FRONTEND RENDERING
   └─► Display weather card
   └─► Render 15 activity cards with photos
   └─► Each card links to official website
Alternative Flow (Unknown Destination)
4. RAG DECISION AGENT ACTIVATES
   │
   ├─► Step 1: Exact Match Check
   │   └─► "paris" != any destination in DB ✗
   │
   ├─► Step 2: Semantic Search
   │   └─► Encode "paris" → [0.23, 0.67, ...]
   │   └─► Find nearest vector
   │   └─► Distance: 0.85 > 0.5 threshold ✗
   │
   └─► Step 3: Fallback to Gemini
       │
       ▼
5. GENERATIVE AI AGENT ACTIVATES
   │
   ├─► Construct prompt with weather context
   │   └─► "What should I do in Paris? Weather: 18°C, sunny..."
   │
   ├─► Call Gemini 2.0 Flash
   │   └─► Temperature: 0.7 (creative but controlled)
   │
   └─► Parse JSON response
       └─► 15 activities generated by AI
            │
            ▼
6. ENRICHMENT AGENT ACTIVATES
   └─► (Same as above - fetch photos & URLs)
🛠️ Technology Stack
Frontend
Framework: Angular 18 (Standalone Components)
UI Library: Angular Material
Styling: SCSS with responsive design
State Management: Component-based (reactive)
Backend
Framework: FastAPI (Python)
AI/ML:
LLM: Google Gemini 2.0 Flash (via LangChain)
Embeddings: Sentence Transformers (all-MiniLM-L6-v2)
Vector DB: ChromaDB (persistent local storage)
External APIs:
OpenWeather API (weather data)
Google Places API (photos, URLs)
Environment: Python 3.13 with virtual environment
Data Flow
Protocol: REST API (HTTP/JSON)
CORS: Enabled for localhost:4200
Error Handling: Comprehensive logging and fallbacks
📊 Data Models
Activity Model
interface Activity {
  activity: string;        // Name of the activity
  description: string;     // Brief description (max 150 chars)
  link: string;           // Official website or Google Maps URL
  imgUrl?: string;        // Photo from Google Places API
}
Weather Model
interface Weather {
  temperature: number;     // Celsius (rounded to whole number)
  description: string;     // e.g., "clear sky", "scattered clouds"
  humidity: number;        // Percentage
  wind_speed: number;      // Meters per second
  error?: string;         // If weather fetch fails
}
RAG Destination Model
{
  "destination": "string",
  "country": "string",
  "description": "string",
  "activities": [
    {
      "activity": "string",
      "description": "string"
    }
  ]
}
# 🎨 Key Features
1. Intelligent Source Selection
Automatically chooses between curated data (RAG) and AI generation
Transparent logging shows which source was used
Ensures accuracy for less-known destinations
2. Context-Aware Recommendations
Weather data influences AI suggestions
Real-time conditions considered
Seasonal appropriateness
3. Content Enrichment
Real photos from Google Places
Official website links (not AI-generated)
Fallback to Google Maps URLs if no website exists
4. Responsive Design
Desktop: Weather card beside search bar
Mobile: Weather card stacks below search bar
Activity grid adapts to screen size
5. Error Handling & Fallbacks
Weather API failure → Still provides recommendations
Places API failure → Uses placeholder images
RAG miss → Seamless fallback to Gemini
JSON parse errors → Detailed logging and user feedback
🔐 Security & Best Practices
API Key Management
All API keys stored in .env file (gitignored)
Environment variables loaded via python-dotenv
No hardcoded credentials in source code
Data Privacy
No user data stored
No tracking or analytics
All processing happens server-side
Performance Optimization
Vector database persisted locally (no reindexing on every request)
Embeddings cached in ChromaDB
Efficient exact match check before semantic search
📈 Scalability Considerations
Current Architecture
Local Development: Single-server setup
Vector DB: ChromaDB (local, file-based)
Suitable for: Prototype, demo, small-scale deployment
Production Enhancements
Vector DB: Migrate to Pinecone, Weaviate, or Qdrant (cloud-hosted)
Caching: Redis for API responses
Load Balancing: Multiple FastAPI instances
CDN: For static assets and images
Database: PostgreSQL for user preferences (future feature)
