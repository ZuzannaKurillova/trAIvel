# RAG (Retrieval-Augmented Generation) System

## Overview

The RAG system prevents Gemini from hallucinating about less-known destinations by using a local vector database with verified information.

## How It Works

1. **Data Storage**: Destinations and activities are stored in `destinations_data.json`
2. **Vector Database**: ChromaDB creates embeddings using `sentence-transformers`
3. **Semantic Search**: When a user searches for a destination, the system:
   - First checks the RAG database using semantic similarity
   - If found (similarity > 0.3), returns verified data
   - If not found, falls back to Gemini AI

## Architecture

```
User Query → RAG Search → Found? → Return RAG Data
                       ↓
                       No
                       ↓
                  Gemini AI → Return AI Data
```

## Files

- **`less_known_destinations_data.json`**: Source data for less-known destinations (edit this to add new places)
- **`rag_service.py`**: RAG logic, vector database management, and search
- **`ai_agent.py`**: Modified to check RAG first, then Gemini
- **`chroma_db/`**: Vector database storage (auto-generated, gitignored)

## Adding New Destinations

Edit `less_known_destinations_data.json` and add entries in this format:

```json
{
  "destination": "City Name",
  "country": "Country Name",
  "description": "Brief description of the destination",
  "activities": [
    {
      "activity": "Activity Name",
      "description": "Activity description (max 150 chars)"
    }
  ]
}
```

**Note**: The `link` field is optional. If not provided, it will be automatically fetched from Google Places API.

### Tips for Adding Data:

1. **Be specific**: Use full destination names (e.g., "Český Krumlov" not just "Krumlov")
2. **Add 5-15 activities**: Enough variety for users
3. **Keep descriptions concise**: Max 150 characters for activities
4. **Include context**: Country name helps with disambiguation
5. **Skip the link field**: Google Places API will fetch official websites automatically

## Reindexing

The database automatically rebuilds when:
- The backend starts
- A search is performed and the collection doesn't exist

To manually trigger reindexing, restart the backend after editing `less_known_destinations_data.json`.

## Example Destinations Included

1. **Český Krumlov, Czech Republic** - Medieval town with castle
2. **Kotor, Montenegro** - Coastal town with fortified walls
3. **Mostar, Bosnia and Herzegovina** - Historic city with Ottoman bridge

## Technical Details

- **Embedding Model**: `all-MiniLM-L6-v2` (384 dimensions, fast and accurate)
- **Vector DB**: ChromaDB (local, persistent)
- **Distance Threshold**: 1.0 (lower distance = higher similarity, 0.0 = perfect match)
- **Search Results**: Top 1 match returned

## Benefits

✅ **No hallucinations** for known destinations
✅ **Verified information** from curated sources
✅ **Real website links** instead of AI-generated URLs
✅ **Fast retrieval** with semantic search
✅ **Fallback to AI** for unknown places
✅ **Easy to maintain** - just edit JSON file

## Monitoring

Check backend logs for:
- `INFO - Using RAG data for {destination}` - RAG hit
- `INFO - No RAG data found, using Gemini for {destination}` - RAG miss
- `SUCCESS - Added X destinations to RAG database` - Indexing complete

## Future Enhancements

- Add more destinations over time
- Include seasonal recommendations
- Add user ratings/reviews
- Multi-language support
- Image URLs in RAG data
