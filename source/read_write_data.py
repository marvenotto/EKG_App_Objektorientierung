import os
import json
import logging
import pandas as pd

# Hier schalten wir ein unsichtbares Warnsystem ein. 
# Wenn im Hintergrund etwas schiefgeht, schreibt das Programm das für uns in ein Fehler-Tagebuch.
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# --- Automatische Ordnersuche ---
# Egal auf welchem PC das Programm gestartet wird, es findet automatisch seinen Hauptordner.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, "..")

# Hier merken wir uns fest, in welchen Ordnern unsere Datenbank und unsere Profilbilder liegen.
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "person_db.json")
PICTURE_DIR = os.path.join(PROJECT_ROOT, "data", "pictures")

def read_my_txt(file_path):
    # Lese die EKG-Werte aus der Textdatei. (Die Zahlen sind dort mit Tabulatoren getrennt).
    df = pd.read_csv(file_path, sep="\t", header=None)

    # Wir geben den beiden Spalten einfache, verständliche Namen.
    df.columns = ["Messwerte in mV","Zeit in ms"]
    
    # Das fertige Paket mit den EKG-Daten geht zurück an die Webseite.
    return df

def load_person_data():
    """
    Diese Funktion öffnet unsere Datenbank im Hintergrund. 
    Sie passt auf, dass die App nicht abstürzt, falls die Datei fehlt oder kaputt ist.
    """
    # Gibt es die Datei überhaupt? Wenn nicht, brechen wir sofort ab.
    if not os.path.exists(DATA_PATH):
        logger.error(f"Database file not found at {DATA_PATH}")
        return []
    
    try:
        # Versuche, die Datei ganz normal zu öffnen und zu lesen.
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Ist der Inhalt auch wirklich eine vernünftige Liste?
        if not isinstance(data, list):
            logger.error(f"Invalid data format: Expected list, got {type(data).__name__}")
            return []
            
        return data
        
    except json.JSONDecodeError as e:
        # Wenn die Datei falsch formatiert ist (z.B. ein Komma fehlt), fangen wir den Fehler hier ab.
        logger.error(f"JSON parsing error in {DATA_PATH}: {e}")
        return []
    except (IOError, OSError) as e:
        # Wenn die Datei z.B. vom Computer blockiert ist.
        logger.error(f"Error reading file {DATA_PATH}: {e}")
        return []
    except Exception as e:
        # Für alle anderen, völlig unerwarteten Fehler.
        logger.error(f"Unexpected error loading person data: {e}")
        return []


def get_person_list():
    """
    Das hier baut einfach nur die Namensliste (Vorname + Nachname) für unser Dropdown-Menü auf der Webseite.
    """
    data = load_person_data()
    person_list = []
    
    # Wir schauen uns jede Person in der Datenbank einzeln an und prüfen, ob alles stimmt.
    for i, person in enumerate(data):
        try:
            # Sind die Daten im richtigen Format?
            if not isinstance(person, dict):
                logger.warning(f"Record {i}: Expected dict, got {type(person).__name__}, skipping")
                continue
                
            # Wurden Vorname und Nachname überhaupt ausgefüllt?
            if 'vorname' not in person or 'nachname' not in person:
                logger.warning(f"Record {i}: Missing 'vorname' or 'nachname' field, skipping")
                continue
            
            # Wir schneiden aus Versehen getippte Leerzeichen am Anfang und Ende weg.
            vorname = str(person['vorname']).strip()
            nachname = str(person['nachname']).strip()
            
            # Sind die Felder nach dem Abschneiden der Leerzeichen leer? Dann überspringen!
            if not vorname or not nachname:
                logger.warning(f"Record {i}: Empty name fields, skipping")
                continue
            
            # Alles super! Wir packen Vor- und Nachname zusammen in unsere fertige Liste.
            person_list.append(f"{vorname} {nachname}")
            
        except Exception as e:
            # Falls bei dieser Person irgendetwas schiefgeht, machen wir einfach mit der nächsten weiter.
            logger.warning(f"Record {i}: Error processing person data: {e}")
            continue
    
    return person_list


def get_person_dict():
    """
    Das ist unser schnelles Telefonbuch: Wir verknüpfen den ganzen Namen direkt mit allen Infos der Person.
    So findet die App später sofort das richtige Alter und Bild, wenn man einen Namen anklickt.
    """
    data = load_person_data()
    person_dict = {}
    
    for i, person in enumerate(data):
        try:
            # Wir prüfen wieder alle Namen, genau wie oben bei der Namensliste.
            if not isinstance(person, dict):
                logger.warning(f"Record {i}: Expected dict, got {type(person).__name__}, skipping")
                continue
            
            if 'vorname' not in person or 'nachname' not in person:
                logger.warning(f"Record {i}: Missing 'vorname' or 'nachname' field, skipping")
                continue
            
            vorname = str(person['vorname']).strip()
            nachname = str(person['nachname']).strip()
            
            if not vorname or not nachname:
                logger.warning(f"Record {i}: Empty name fields, skipping")
                continue
            
            # Den vollen Namen zusammenbasteln.
            full_name = f"{vorname} {nachname}"
            
            # Das System merkt sich im Hintergrund, falls es zwei Leute mit exakt dem gleichen Namen gibt.
            if full_name in person_dict:
                logger.warning(f"Duplicate person found: {full_name}, overwriting previous entry")
            
            # Wir speichern die Person unter ihrem vollen Namen in unserem "Telefonbuch" ab.
            person_dict[full_name] = person
            
        except Exception as e:
            logger.warning(f"Record {i}: Error processing person data: {e}")
            continue
    
    return person_dict


def get_person_picture(person_name):
    """
    Diese Funktion sucht im Ordner nach dem passenden Foto für die ausgewählte Person.
    Damit der Computer die Bilder findet, wandeln wir Leerzeichen in Unterstriche um (Max Mustermann -> Max_Mustermann).
    """
    try:
        # Haben wir überhaupt einen echten, vernünftigen Namen bekommen?
        if not isinstance(person_name, str) or not person_name.strip():
            logger.warning("Invalid person_name: must be a non-empty string")
            return None
        
        # Mache aus "Max Mustermann" ein "Max_Mustermann" für die Dateisuche.
        file_base = person_name.replace(" ", "_").strip()
        
        # Wir schauen nacheinander nach, ob das Bild ein .png, .jpg oder .jpeg ist.
        extensions = [".png", ".jpg", ".jpeg"]
        
        # 1. Wir suchen, ob es ein echtes Foto von der Person gibt.
        for ext in extensions:
            picture_path = os.path.join(PICTURE_DIR, f"{file_base}{ext}")
            if os.path.exists(picture_path):
                return picture_path
        
        # 2. Wenn wir kein persönliches Foto finden, laden wir unser graues Standard-Profilbild.
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
    Das ist die Funktion für unser neues Formular! 
    Sie nimmt die Eingaben, prüft ob alles Sinn macht, und speichert die neue Person für immer ab.
    """
    try:
        # --- Schritt 1: Eingaben kontrollieren ---
        # Hat der User wirklich einen Text in das Vornamen-Feld eingetippt?
        if not isinstance(vorname, str) or not vorname.strip():
            logger.error("Invalid vorname: must be a non-empty string")
            return {
                "success": False,
                "person": None,
                "error_type": "invalid_input",
                "message": "Vorname ungültig oder leer"
            }
        
        # Hat der User einen Nachnamen eingetippt?
        if not isinstance(nachname, str) or not nachname.strip():
            logger.error("Invalid nachname: must be a non-empty string")
            return {
                "success": False,
                "person": None,
                "error_type": "invalid_input",
                "message": "Nachname ungültig oder leer"
            }
        
        # Hat der User ein normales Alter (zwischen 0 und 150 Jahren) angegeben?
        if not isinstance(alter, int) or alter < 0 or alter > 150:
            logger.error("Invalid alter: must be an integer between 0 and 150")
            return {
                "success": False,
                "person": None,
                "error_type": "invalid_input",
                "message": "Alter muss zwischen 10 und 100 liegen"
            }
        
        # --- Schritt 2: Neue Person vorbereiten ---
        # Wir holen uns alle bisherigen Leute aus der Datenbank.
        data = load_person_data()
        
        # Wir suchen die höchste ID-Nummer, die wir haben, und geben der neuen Person einfach die nächste Nummer (+1).
        max_id = max([p.get('id', 0) for p in data] + [0])
        new_id = max_id + 1
        
        # Wir basteln das Daten-Paket für die neue Person zusammen.
        new_person = {
            "id": new_id,
            "vorname": vorname.strip(),
            "nachname": nachname.strip(),
            "alter": alter
        }
        
        # --- Schritt 3: Gibt es die Person schon? ---
        # Wir gehen alle Leute durch. Wenn Vor- und Nachname exakt gleich sind, meckern wir und brechen ab.
        for person in data:
            if (person['vorname'].lower() == new_person['vorname'].lower() and 
                person['nachname'].lower() == new_person['nachname'].lower()):
                logger.warning(f"Person {vorname} {nachname} already exists in database")
                return {
                    "success": False,
                    "person": None,
                    "error_type": "duplicate",
                    "message": f"⚠️ {vorname} {nachname} existiert bereits in der Datenbank!"
                }
        
        # --- Schritt 4: Speichern ---
        # Die Person ist wirklich neu! Wir hängen sie ganz hinten an unsere Namensliste an.
        data.append(new_person)
        
        # Jetzt schreiben wir die neue, längere Liste sicher zurück in die Datei auf die Festplatte.
        try:
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"Successfully added new person: {vorname} {nachname} (ID: {new_id})")
            
            # Es hat geklappt! Die Erfolgsmeldung geht zurück an die Webseite.
            return {
                "success": True,
                "person": new_person,
                "error_type": None,
                "message": f"✅ {vorname} {nachname} wurde hinzugefügt!"
            }
        
        except (IOError, OSError) as e:
            # die Datei ließ sich nicht speichern (z.B. weil sie schreibgeschützt ist).
            logger.error(f"Error writing to JSON file {DATA_PATH}: {e}")
            return {
                "success": False,
                "person": None,
                "error_type": "file_error",
                "message": "Fehler beim Speichern der Datei"
            }
            
    except Exception as e:
        # Falls irgendein ganz seltsamer Fehler passiert ist, der nicht geplant war.
        logger.error(f"Unexpected error adding person: {e}")
        return {
            "success": False,
            "person": None,
            "error_type": "unknown",
            "message": "Unerwarteter Fehler"
        }