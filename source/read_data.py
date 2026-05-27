import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

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
    Loads and parses the entire JSON user database with error handling.
    
    Returns:
        list: A list of dictionaries containing person records, 
              or an empty list if the file is missing or invalid.
    """
    if not os.path.exists(DATA_PATH):
        logger.error(f"Database file not found at {DATA_PATH}")
        return []
    
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Validate that data is a list
        if not isinstance(data, list):
            logger.error(f"Invalid data format: Expected list, got {type(data).__name__}")
            return []
            
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error in {DATA_PATH}: {e}")
        return []
    except (IOError, OSError) as e:
        logger.error(f"Error reading file {DATA_PATH}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error loading person data: {e}")
        return []


def get_person_list():
    """
    Generates a list of full names for UI selection components with validation.
    
    Returns:
        list: Formatted strings of "Firstname Lastname" for all valid records.
    """
    data = load_person_data()
    person_list = []
    
    # enumerate() provides both index (i) and element for clear error messages
    for i, person in enumerate(data):
        try:
            # Validate required fields
            if not isinstance(person, dict):
                logger.warning(f"Record {i}: Expected dict, got {type(person).__name__}, skipping")
                continue
                
            if 'vorname' not in person or 'nachname' not in person:
                logger.warning(f"Record {i}: Missing 'vorname' or 'nachname' field, skipping")
                continue
            
            # Ensure fields are strings
            vorname = str(person['vorname']).strip()
            nachname = str(person['nachname']).strip()
            
            if not vorname or not nachname:
                logger.warning(f"Record {i}: Empty name fields, skipping")
                continue
            
            person_list.append(f"{vorname} {nachname}")
            
        except Exception as e:
            logger.warning(f"Record {i}: Error processing person data: {e}")
            continue
    
    return person_list


def get_person_dict():
    """
    Creates a lookup dictionary indexed by full name with validation.
    
    Returns:
        dict: A mapping of "Firstname Lastname" to their respective profile data
              (only includes valid records).
    """
    data = load_person_data()
    person_dict = {}
    
    for i, person in enumerate(data):
        try:
            # Validate that person is a dictionary
            if not isinstance(person, dict):
                logger.warning(f"Record {i}: Expected dict, got {type(person).__name__}, skipping")
                continue
            
            # Validate required fields exist
            if 'vorname' not in person or 'nachname' not in person:
                logger.warning(f"Record {i}: Missing 'vorname' or 'nachname' field, skipping")
                continue
            
            # Convert to strings and strip whitespace
            vorname = str(person['vorname']).strip()
            nachname = str(person['nachname']).strip()
            
            if not vorname or not nachname:
                logger.warning(f"Record {i}: Empty name fields, skipping")
                continue
            
            full_name = f"{vorname} {nachname}"
            
            # Warn about duplicate names
            if full_name in person_dict:
                logger.warning(f"Duplicate person found: {full_name}, overwriting previous entry")
            
            person_dict[full_name] = person
            
        except Exception as e:
            logger.warning(f"Record {i}: Error processing person data: {e}")
            continue
    
    return person_dict


def get_person_picture(person_name):
    """
    Resolves the file path for a subject's profile picture with error handling.
    
    Converts spaces to underscores and checks against multiple common image 
    extensions. Falls back to a default placeholder image if no specific 
    file is found.
    
    Args:
        person_name (str): Full name of the subject.
        
    Returns:
        str or None: The absolute path to the resolved image file, 
                     or None if no valid image is found.
    """
    try:
        # Validate input
        if not isinstance(person_name, str) or not person_name.strip():
            logger.warning("Invalid person_name: must be a non-empty string")
            return None
        
        # Sanitize the name for the filesystem (e.g., "Max Mustermann" -> "Max_Mustermann")
        file_base = person_name.replace(" ", "_").strip()
        
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
            logger.warning(f"No default placeholder image found at {default_image}")
            return None
            
    except Exception as e:
        logger.error(f"Error resolving picture for {person_name}: {e}")
        return None


def add_person(vorname, nachname, alter):
    """
    Adds a new person to the database and saves to JSON file.
    
    Args:
        vorname (str): First name of the person.
        nachname (str): Last name of the person.
        alter (int): Age of the person.
        
    Returns:
        dict: The newly created person record, or None if addition failed.
    """
    try:
        # Validate inputs
        if not isinstance(vorname, str) or not vorname.strip():
            logger.error("Invalid vorname: must be a non-empty string")
            return None
        
        if not isinstance(nachname, str) or not nachname.strip():
            logger.error("Invalid nachname: must be a non-empty string")
            return None
        
        if not isinstance(alter, int) or alter < 0 or alter > 150:
            logger.error("Invalid alter: must be an integer between 0 and 150")
            return None
        
        # Load current data
        data = load_person_data()
        
        # Find the highest current ID
        max_id = max([p.get('id', 0) for p in data] + [0])
        new_id = max_id + 1
        
        # Create new person record
        new_person = {
            "id": new_id,
            "vorname": vorname.strip(),
            "nachname": nachname.strip(),
            "alter": alter
        }
        
        # Check for duplicates
        for person in data:
            if (person['vorname'].lower() == new_person['vorname'].lower() and 
                person['nachname'].lower() == new_person['nachname'].lower()):
                logger.warning(f"Person {vorname} {nachname} already exists in database")
                return None
        
        # Add new person to list
        data.append(new_person)
        
        # Save to JSON file
        try:
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"Successfully added new person: {vorname} {nachname} (ID: {new_id})")
            return new_person
        
        except (IOError, OSError) as e:
            logger.error(f"Error writing to JSON file {DATA_PATH}: {e}")
            return None
            
    except Exception as e:
        logger.error(f"Unexpected error adding person: {e}")
        return None