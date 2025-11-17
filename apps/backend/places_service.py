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

def get_place_info(query: str, destination: str = "") -> dict:
    """
    Get photo URL and website for a place using Google Places API
    
    Args:
        query: The search query (e.g., "Eiffel Tower" or "Louvre Museum")
        destination: Optional destination to add context (e.g., "Paris")
    
    Returns:
        Dict with 'photo_url' and 'website' or empty dict if not found
    """
    if not gmaps:
        print("WARNING - Google Maps client not initialized. Check GOOGLE_PLACES_API_KEY!")
        return {}
    
    print(f"\n=== FETCHING INFO FOR: {query} ===")
    
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
            return {}
        
        if not places_result.get('results'):
            print(f"3. No results found")
            return {}
        
        # Get the first result
        place = places_result['results'][0]
        place_id = place.get('place_id')
        place_name = place.get('name', 'Unknown')
        
        print(f"3. Found: '{place_name}' (ID: {place_id[:20]}...)")
        
        if not place_id:
            return {}
        
        # Get place details including photos and website
        print(f"4. Fetching place details...")
        place_details = gmaps.place(place_id=place_id, fields=['name', 'photo', 'website', 'url'])
        
        detail_status = place_details.get('status')
        print(f"5. Details Status: {detail_status}")
        
        if detail_status != 'OK':
            print(f"   ERROR: Details API returned '{detail_status}'")
            return {}
        
        result = place_details.get('result', {})
        
        # Debug: Show all available keys
        print(f"6. Available fields in result: {list(result.keys())}")
        
        photos = result.get('photos', [])
        website = result.get('website')
        url = result.get('url')
        
        print(f"7. website field: {website}")
        print(f"8. url field: {url}")
        
        place_info = {}
        
        # Get photo URL
        if photos:
            print(f"9. Found {len(photos)} photo(s)")
            photo_reference = photos[0].get('photo_reference')
            
            if photo_reference:
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={GOOGLE_PLACES_API_KEY}"
                place_info['photo_url'] = photo_url
                print(f"10. ✓ Photo URL generated")
        else:
            print(f"9. No photos available")
        
        # Get website URL - prefer official website, fallback to Google Maps URL
        final_url = website or url
        if final_url:
            place_info['website'] = final_url
            print(f"11. ✓ Using URL: {final_url[:60]}...")
        else:
            print(f"11. No website/URL available")
        
        print(f"=== END ===\n")
        return place_info
        
    except Exception as e:
        print(f"ERROR - Exception: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print(f"=== END (ERROR) ===\n")
        return {}


def get_place_info_batch(activities: list, destination: str) -> list:
    """
    Get photos and websites for multiple activities
    
    Args:
        activities: List of activity dicts with 'activity' field
        destination: The destination city/location
    
    Returns:
        List of activities with 'imgUrl' and 'link' fields updated
    """
    # Default fallback image - a nice travel-themed placeholder
    DEFAULT_IMAGE = "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=400&h=300&fit=crop"
    
    for activity in activities:
        activity_name = activity.get('activity', '')
        place_info = get_place_info(activity_name, destination)
        
        # Update photo URL
        if place_info.get('photo_url'):
            activity['imgUrl'] = place_info['photo_url']
        else:
            # Use Unsplash as fallback
            activity['imgUrl'] = DEFAULT_IMAGE
        
        # Update website URL (prefer Google Places URL over Gemini's)
        if place_info.get('website'):
            activity['link'] = place_info['website']
            print(f"   → Updated link for '{activity_name}': {place_info['website'][:50]}...")
    
    return activities
