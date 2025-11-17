from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from ai_agent import get_ai_recommendation

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

@app.get("/api/recommend")
async def recommend(destination: str):
    recommendation = get_ai_recommendation(destination)
    return {"destination": destination, "recommendation": recommendation}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
