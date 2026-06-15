import json
import datetime
from PIL import Image
import os

class Person:
    def __init__(self, person_dict):
        self.id = person_dict.get("id")
        self.firstname = person_dict.get("vorname", "Unbekannt")
        self.lastname = person_dict.get("nachname", "Unbekannt")
        self.age = person_dict.get("alter", 25)
        
        current_year = datetime.datetime.now().year
        self.date_of_birth = current_year - self.age
        
        self.gender = "Male"  
        self.picture_path = f"data/pictures/{self.lastname.lower()}.jpg"
        
        # HIER IST DIE MAGIE: Wir weisen den IDs dynamisch eure 5 Dateien zu
        file_map = {
            1: "data/ekg_data/01_Ruhe.txt",
            2: "data/ekg_data/02_Ruhe.txt",
            3: "data/ekg_data/03_Ruhe.txt",
            4: "data/ekg_data/04_Belastung.txt",
            5: "data/ekg_data/05_Belastung.txt"
        }
        # Falls jemand z.B. ID 6 hat, bekommt er als Ersatz einfach Datei 1
        test_file = file_map.get(self.id, "data/ekg_data/01_Ruhe.txt")
        
        self.ekg_tests = [
            {
                "id": self.id,
                "date": "15.06.2026",
                "result_link": test_file
            }
        ]

    @staticmethod
    def load_person_data():
        try:
            with open("data/person_db.json", "r", encoding="utf-8") as file:
                person_data = json.load(file)
            return person_data
        except FileNotFoundError:
            return []

    @classmethod
    def load_by_id(cls, person_id):
        data = cls.load_person_data()
        for p in data:
            if p.get("id") == person_id:
                return cls(p)
        return None

    def calc_age(self):
        return self.age

    def calc_max_heart_rate(self):
        age = self.calc_age()
        if self.gender.lower() == "male":
            return int(223 - (0.9 * age))
        else:
            return int(226 - (1.0 * age))

    def get_full_name(self):
        return f"{self.lastname}, {self.firstname}"

    def get_image(self):
        if os.path.exists(self.picture_path):
            try:
                return Image.open(self.picture_path)
            except:
                return None
        return None