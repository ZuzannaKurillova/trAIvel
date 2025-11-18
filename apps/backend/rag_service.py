# apps/backend/rag_service.py
import json
import os
from typing import Optional, List, Dict
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB client
chroma_client = chromadb.Client(Settings(
    persist_directory="./chroma_db",
    anonymized_telemetry=False
))

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Collection name
COLLECTION_NAME = "destinations"

def load_destinations_data():
    """Load destinations data from JSON file"""
    json_path = os.path.join(os.path.dirname(__file__), "less_known_destinations_data.json")
    
    if not os.path.exists(json_path):
        print(f"WARNING - less_known_destinations_data.json not found at {json_path}")
        return []
    
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def initialize_rag_database():
    """Initialize or update the RAG database with destinations data"""
    print("INFO - Initializing RAG database...")
    
    # Load data
    destinations = load_destinations_data()
    
    if not destinations:
        print("WARNING - No destinations data to load")
        return
    
    # Get or create collection
    try:
        collection = chroma_client.get_collection(name=COLLECTION_NAME)
        print(f"INFO - Found existing collection with {collection.count()} documents")
        # Delete and recreate to update
        chroma_client.delete_collection(name=COLLECTION_NAME)
        print("INFO - Deleted old collection")
    except:
        print("INFO - No existing collection found")
    
    collection = chroma_client.create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Travel destinations and activities"}
    )
    
    # Prepare documents for embedding
    documents = []
    metadatas = []
    ids = []
    
    for idx, dest in enumerate(destinations):
        # Create a comprehensive text for embedding
        doc_text = f"{dest['destination']}, {dest['country']}. {dest['description']}"
        
        # Add activities info
        activities_text = " Activities: " + ", ".join([
            f"{act['activity']}: {act['description']}" 
            for act in dest.get('activities', [])
        ])
        doc_text += activities_text
        
        documents.append(doc_text)
        metadatas.append({
            "destination": dest['destination'],
            "country": dest['country'],
            "description": dest['description'],
            "activities": json.dumps(dest.get('activities', []))
        })
        ids.append(f"dest_{idx}")
    
    # Generate embeddings
    print(f"INFO - Generating embeddings for {len(documents)} destinations...")
    embeddings = embedding_model.encode(documents).tolist()
    
    # Add to collection
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"SUCCESS - Added {len(documents)} destinations to RAG database")

def search_destination(query: str, n_results: int = 1) -> Optional[Dict]:
    """
    Search for a destination in the RAG database
    
    Args:
        query: Destination name to search for
        n_results: Number of results to return
    
    Returns:
        Destination data if found, None otherwise
    """
    try:
        collection = chroma_client.get_collection(name=COLLECTION_NAME)
    except:
        print("WARNING - RAG collection not found. Initializing...")
        initialize_rag_database()
        try:
            collection = chroma_client.get_collection(name=COLLECTION_NAME)
        except:
            print("ERROR - Failed to initialize RAG database")
            return None
    
    # First, try exact string match (case-insensitive)
    all_results = collection.get()
    query_lower = query.lower().strip()
    
    for idx, metadata in enumerate(all_results['metadatas']):
        dest_name = metadata['destination'].lower().strip()
        if dest_name == query_lower:
            print(f"INFO - Exact match found for: {metadata['destination']}")
            activities = json.loads(metadata['activities'])
            
            # Ensure each activity has a link field
            for activity in activities:
                if 'link' not in activity:
                    activity['link'] = ''
            
            return {
                "destination": metadata['destination'],
                "country": metadata['country'],
                "description": metadata['description'],
                "activities": activities
            }
    
    # If no exact match, try semantic search
    print(f"INFO - No exact match, trying semantic search for: {query}")
    
    # Generate query embedding
    query_embedding = embedding_model.encode([query]).tolist()
    
    # Search
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    if not results['ids'] or not results['ids'][0]:
        print(f"INFO - No RAG data found for: {query}")
        return None
    
    # Get the best match
    metadata = results['metadatas'][0][0]
    distance = results['distances'][0][0] if 'distances' in results else None
    
    # Use stricter threshold for semantic search (0.5)
    # This prevents "Nitrianske Rudno" from matching "Nitrianske Pravno"
    if distance is not None and distance > 0.5:
        print(f"INFO - Match found but similarity too low (distance: {distance:.2f}) for: {query}")
        return None
    
    print(f"INFO - Semantic match found for: {metadata['destination']} (distance: {distance:.2f}, similarity: {1-distance:.2f})")
    
    # Parse activities back from JSON
    activities = json.loads(metadata['activities'])
    
    # Ensure each activity has a link field (will be filled by Google Places API later)
    for activity in activities:
        if 'link' not in activity:
            activity['link'] = ''  # Placeholder, will be updated by places_service
    
    return {
        "destination": metadata['destination'],
        "country": metadata['country'],
        "description": metadata['description'],
        "activities": activities
    }

def get_rag_recommendations(destination: str) -> Optional[List[Dict]]:
    """
    Get recommendations from RAG database if available
    
    Args:
        destination: Destination name
    
    Returns:
        List of activities if found in RAG, None otherwise
    """
    result = search_destination(destination)
    
    if result and 'activities' in result:
        print(f"SUCCESS - Using RAG data for {destination}")
        return result['activities']
    
    return None

# Initialize database on module import
try:
    initialize_rag_database()
except Exception as e:
    print(f"WARNING - Failed to initialize RAG database on startup: {e}")
