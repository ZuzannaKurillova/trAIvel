# apps/backend/places_service.py
import os
import googlemaps
from typing import Optional

# Get API key from environment variable
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")

if GOOGLE_PLACES_API_KEY:
    GOOGLE_PLACES_API_KEY = GOOGLE_PLACES_API_KEY.strip('"').strip("'")
    print(f"INFO - Google Places API key loaded (length: {len(GOOGLE_PLACES_API_KEY)})")
else:
    print("WARNING - GOOGLE_PLACES_API_KEY not set. Using placeholder images.")

# Initialize Google Maps client
gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY) if GOOGLE_PLACES_API_KEY else None

def get_place_photo(query: str, destination: str = "") -> Optional[str]:
    """
    Get a photo URL for a place using Google Places API
    
    Args:
        query: The search query (e.g., "Eiffel Tower" or "Louvre Museum")
        destination: Optional destination to add context (e.g., "Paris")
    
    Returns:
        Photo URL or None if not found
    """
    if not gmaps:
        print("WARNING - Google Maps client not initialized. Check GOOGLE_PLACES_API_KEY!")
        return None
    
    print(f"\n=== FETCHING PHOTO FOR: {query} ===")
    
    try:
        # Combine query with destination for better results
        search_query = f"{query}, {destination}" if destination else query
        
        print(f"1. Searching Places API: '{search_query}'")
        
        # Search for the place
        places_result = gmaps.places(query=search_query)
        
        status = places_result.get('status')
        print(f"2. API Status: {status}")
        
        if status != 'OK':
            print(f"   ERROR: API returned status '{status}'")
            if status == 'REQUEST_DENIED':
                print("   → Check if Places API is enabled in Google Cloud Console")
                print("   → Verify API key has Places API permissions")
            return None
        
        if not places_result.get('results'):
            print(f"3. No results found")
            return None
        
        # Get the first result
        place = places_result['results'][0]
        place_id = place.get('place_id')
        place_name = place.get('name', 'Unknown')
        
        print(f"3. Found: '{place_name}' (ID: {place_id[:20]}...)")
        
        if not place_id:
            return None
        
        # Get place details including photos
        print(f"4. Fetching place details...")
        place_details = gmaps.place(place_id=place_id, fields=['name', 'photo'])
        
        detail_status = place_details.get('status')
        print(f"5. Details Status: {detail_status}")
        
        if detail_status != 'OK':
            print(f"   ERROR: Details API returned '{detail_status}'")
            return None
        
        photos = place_details.get('result', {}).get('photos', [])
        
        if not photos:
            print(f"6. No photos available for this place")
            return None
        
        print(f"6. Found {len(photos)} photo(s)")
        
        # Get the first photo reference
        photo_reference = photos[0].get('photo_reference')
        
        if not photo_reference:
            print(f"7. No photo reference in response")
            return None
        
        # Construct the photo URL
        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={GOOGLE_PLACES_API_KEY}"
        
        print(f"7. ✓ Photo URL generated successfully")
        print(f"=== END ===\n")
        return photo_url
        
    except Exception as e:
        print(f"ERROR - Exception: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print(f"=== END (ERROR) ===\n")
        return None


def get_place_photo_batch(activities: list, destination: str) -> list:
    """
    Get photos for multiple activities
    
    Args:
        activities: List of activity dicts with 'activity' field
        destination: The destination city/location
    
    Returns:
        List of activities with 'imgUrl' field added
    """
    # Default fallback image - a nice travel-themed placeholder
    DEFAULT_IMAGE = "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=400&h=300&fit=crop"
    
    for activity in activities:
        activity_name = activity.get('activity', '')
        photo_url = get_place_photo(activity_name, destination)
        
        if photo_url:
            activity['imgUrl'] = photo_url
        else:
            # Use Unsplash as fallback (free, no API key needed)
            activity['imgUrl'] = DEFAULT_IMAGE
    
    return activities
