import json

# Opening JSON file
file = open("data/person_db.json")



def load_person_data(file):
    """A Function that knows where the person database is and returns a dictionary with the persons"""
    with open("data/person_db.json") as file:
        person_data = json.load(file)
    return person_data


def get_person_list():
    person_data = load_person_data(file)
    return [f"{person['vorname']} {person['nachname']}" for person in person_data]

def get_person_age(person_name):
    person_data = load_person_data(file)
    for person in person_data:
        if f"{person['vorname']} {person['nachname']}" == person_name:
            return person['alter']
    return None

print(get_person_list())
print(get_person_age("Cedi Tyson"))