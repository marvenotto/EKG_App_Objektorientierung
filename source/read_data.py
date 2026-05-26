import os
import json

# --- Dynamic Path Resolution ---
# Determine the absolute path of the current script (located in the 'source' directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Navigate one level up to the main project root directory
PROJECT_ROOT = os.path.join(BASE_DIR, "..")

# Define global paths for data assets and images
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "person_db.json")
PICTURE_DIR = os.path.join(PROJECT_ROOT, "data", "pictures")


def load_person_data():
    """
    Loads and parses the entire JSON user database.
    
    Returns:
        list: A list of dictionaries containing person records, 
              or an empty list if the file is missing.
    """
    if not os.path.exists(DATA_PATH):
        print(f"Error: Database file not found at {DATA_PATH}")
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_person_list():
    """
    Generates a list of full names for UI selection components.
    
    Returns:
        list: Formatted strings of "Firstname Lastname" for all records.
    """
    data = load_person_data()
    return [f"{p['vorname']} {p['nachname']}" for p in data]


def get_person_dict():
    """
    Creates a lookup dictionary indexed by full name for fast O(1) data retrieval.
    
    Returns:
        dict: A mapping of "Firstname Lastname" to their respective profile data.
    """
    data = load_person_data()
    return {f"{p['vorname']} {p['nachname']}": p for p in data}


def get_person_picture(person_name):
    """
    Resolves the file path for a subject's profile picture.
    
    Converts spaces to underscores and checks against multiple common image 
    extensions. Falls back to a default placeholder image if no specific 
    file is found.
    
    Args:
        person_name (str): Full name of the subject.
        
    Returns:
        str or None: The absolute path to the resolved image file, 
                     or None as a last resort.
    """
    # Sanitize the name for the filesystem (e.g., "Max Mustermann" -> "Max_Mustermann")
    file_base = person_name.replace(" ", "_")
    
    # Supported image formats to evaluate sequentially
    extensions = [".png", ".jpg", ".jpeg"]
    
    # 1. Attempt to locate a specific profile picture
    for ext in extensions:
        picture_path = os.path.join(PICTURE_DIR, f"{file_base}{ext}")
        if os.path.exists(picture_path):
            return picture_path
            
    # 2. Fallback to the default placeholder asset
    default_image = os.path.join(PICTURE_DIR, "no_picture_male.png")
    
    if os.path.exists(default_image):
        return default_image
    else:
        # Final fallback if no assets are accessible
        return None