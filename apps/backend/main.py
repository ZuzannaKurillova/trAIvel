from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from ai_agent import get_ai_recommendation
from places_service import get_place_info_batch
import json

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="trAIvel Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to trAIvel API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

def clean_json_response(text: str) -> str:
    """Clean JSON response from LLM - remove markdown code blocks"""
    # Remove ```json and ``` markers
    text = text.strip()
    if text.startswith('```json'):
        text = text[7:]  # Remove ```json
    elif text.startswith('```'):
        text = text[3:]  # Remove ```
    
    if text.endswith('```'):
        text = text[:-3]  # Remove trailing ```
    
    return text.strip()

@app.get("/api/recommend")
async def recommend(
    destination: str,
    include_images: bool = Query(default=True, description="Include place images from Google Places API")
):
    # Get AI recommendations
    recommendation = get_ai_recommendation(destination)
    
    print(f"\n=== RAW AI RESPONSE ===")
    print(f"Length: {len(recommendation)} chars")
    print(f"First 200 chars: {recommendation[:200]}")
    print(f"Last 100 chars: {recommendation[-100:]}")
    print(f"======================\n")
    
    # Clean the response (remove markdown code blocks if present)
    cleaned_recommendation = clean_json_response(recommendation)
    
    # Parse the JSON response
    try:
        activities = json.loads(cleaned_recommendation)
        
        if not isinstance(activities, list):
            print(f"ERROR - Expected list, got {type(activities)}")
            return {
                "destination": destination,
                "recommendation": recommendation,
                "error": "Invalid response format - expected array"
            }
        
        print(f"SUCCESS - Parsed {len(activities)} activities")
        
        # Add images and update URLs if requested
        if include_images:
            activities = get_place_info_batch(activities, destination)
            recommendation = json.dumps(activities)
        else:
            recommendation = json.dumps(activities)
            
    except json.JSONDecodeError as e:
        print(f"ERROR - JSON Parse Error: {e}")
        print(f"Attempted to parse: {cleaned_recommendation[:500]}")
        return {
            "destination": destination,
            "recommendation": recommendation,
            "error": f"Failed to parse JSON: {str(e)}",
            "raw_response": recommendation[:1000]  # First 1000 chars for debugging
        }
    except Exception as e:
        print(f"ERROR - Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return {
            "destination": destination,
            "recommendation": recommendation,
            "error": f"Unexpected error: {str(e)}"
        }
    
    return {"destination": destination, "recommendation": recommendation}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
