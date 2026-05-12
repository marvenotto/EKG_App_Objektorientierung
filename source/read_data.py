import os
import json

# Opening JSON file
path_person_data = open("data/person_db.json")
path_pictures = "data/pictures/"



def load_person_data(file):
    """A Function that knows where the person database is and returns a dictionary with the persons"""
    with open("data/person_db.json") as file:
        person_data = json.load(file)
    return person_data



def get_person_list():
    person_data = load_person_data(path_person_data)
    return [f"{person['vorname']} {person['nachname']}" for person in person_data]



def get_person_age(person_name):
    person_data = load_person_data(path_person_data)
    for person in person_data:
        if f"{person['vorname']} {person['nachname']}" == person_name:
            return person['alter']
    return None



def get_person_picture(person_name):
    # Den Namen für den Dateipfad vorbereiten (z.B. Cedric_Rissi.jpg)
    file_name = person_name.replace(" ", "_")
    picture_path = f"data/pictures/{file_name}.jpg"
    
    # Prüfen, ob die Datei existiert
    if os.path.exists(picture_path):
        return picture_path
    else:
        return None
    

print(get_person_list())
print(get_person_age("Cedric Rissi"))
print(get_person_picture("Cedric_Rissi"))