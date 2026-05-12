import os
import json

DATA_PATH = "data/person_db.json"
PICTURE_DIR = "data/pictures/"

def load_person_data():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_person_list():
    data = load_person_data()
    return [f"{p['vorname']} {p['nachname']}" for p in data]

def get_person_dict():
    """Gibt ein Dictionary zurück für schnelleren Zugriff via Name."""
    data = load_person_data()
    return {f"{p['vorname']} {p['nachname']}": p for p in data}

def get_person_picture(person_name):
    file_name = person_name.replace(" ", "_")
    picture_path = os.path.join(PICTURE_DIR, f"{file_name}.jpg")
    
    if os.path.exists(picture_path):
        return picture_path
    return os.path.join(PICTURE_DIR, "no_picture_male.jpg")