# Backend - Python FastAPI

This is the backend application for trAIvel, built with FastAPI and Google Gemini AI.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your real Gemini API key
# Get your API key from: https://makersuite.google.com/app/apikey
```

**IMPORTANT:** Never commit the `.env` file to GitHub! It's already in `.gitignore`.

4. Run the server:
```bash
python main.py
```

Or use Nx:
```bash
nx serve backend
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `GET /` - Welcome message
- `GET /api/health` - Health check
- `GET /api/recommend?destination=Paris` - Get AI travel recommendations

## Security

- API keys are loaded from `.env` file (gitignored)
- Never hardcode API keys in source code
- Use `.env.example` as a template
