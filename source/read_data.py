import os
import json

# 1. Dynamische Pfad-Ermittlung
# Wir ermitteln den absoluten Pfad zu diesem Skript (read_data.py im Ordner 'source')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Gehe eine Ebene höher in das Hauptverzeichnis (EKG_App_Steamlit)
PROJECT_ROOT = os.path.join(BASE_DIR, "..")

# Definieren der Pfade zu den Daten und Bildern
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "person_db.json")
PICTURE_DIR = os.path.join(PROJECT_ROOT, "data", "pictures")

def load_person_data():
    """Lädt die gesamte JSON-Datenbank."""
    if not os.path.exists(DATA_PATH):
        print(f"Fehler: Datei nicht gefunden unter {DATA_PATH}")
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_person_list():
    """Gibt eine Liste aller Namen (Vorname + Nachname) zurück."""
    data = load_person_data()
    return [f"{p['vorname']} {p['nachname']}" for p in data]

def get_person_dict():
    """Gibt ein Dictionary für schnellen Zugriff via Name zurück."""
    data = load_person_data()
    return {f"{p['vorname']} {p['nachname']}": p for p in data}

def get_person_picture(person_name):
    """
    Sucht das Bild einer Person. Ersetzt Leerzeichen durch Unterstriche 
    und prüft verschiedene Dateiendungen.
    """
    # Name für Dateisystem vorbereiten (z.B. "Max Mustermann" -> "Max_Mustermann")
    file_base = person_name.replace(" ", "_")
    
    # Liste der unterstützten Endungen (deine Bilder sind laut Screenshot .png)
    extensions = [".png", ".jpg", ".jpeg"]
    
    # 1. Versuche das spezifische Bild zu finden
    for ext in extensions:
        picture_path = os.path.join(PICTURE_DIR, f"{file_base}{ext}")
        if os.path.exists(picture_path):
            # Wir geben den Pfad relativ zurück oder absolut, hier absolut für die Sicherheit
            return picture_path
            
    default_image = os.path.join(PICTURE_DIR, "no_picture_male.png")
    
    if os.path.exists(default_image):
        return default_image
    else:
        # Letzter Ausweg, falls gar nichts da ist
        return None


# 1. Dynamische Pfad-Ermittlung
# Wir ermitteln den absoluten Pfad zu diesem Skript (read_data.py im Ordner 'source')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Gehe eine Ebene höher in das Hauptverzeichnis (EKG_App_Steamlit)
PROJECT_ROOT = os.path.join(BASE_DIR, "..")

# Definieren der Pfade zu den Daten und Bildern
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "person_db.json")
PICTURE_DIR = os.path.join(PROJECT_ROOT, "data", "pictures")

def load_person_data():
    """Lädt die gesamte JSON-Datenbank."""
    if not os.path.exists(DATA_PATH):
        print(f"Fehler: Datei nicht gefunden unter {DATA_PATH}")
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_person_list():
    """Gibt eine Liste aller Namen (Vorname + Nachname) zurück."""
    data = load_person_data()
    return [f"{p['vorname']} {p['nachname']}" for p in data]

def get_person_dict():
    """Gibt ein Dictionary für schnellen Zugriff via Name zurück."""
    data = load_person_data()
    return {f"{p['vorname']} {p['nachname']}": p for p in data}

def get_person_picture(person_name):
    """
    Sucht das Bild einer Person. Ersetzt Leerzeichen durch Unterstriche 
    und prüft verschiedene Dateiendungen.
    """
    # Name für Dateisystem vorbereiten (z.B. "Max Mustermann" -> "Max_Mustermann")
    file_base = person_name.replace(" ", "_")
    
    # Liste der unterstützten Endungen (deine Bilder sind laut Screenshot .png)
    extensions = [".png", ".jpg", ".jpeg"]
    
    # 1. Versuche das spezifische Bild zu finden
    for ext in extensions:
        picture_path = os.path.join(PICTURE_DIR, f"{file_base}{ext}")
        if os.path.exists(picture_path):
            # Wir geben den Pfad relativ zurück oder absolut, hier absolut für die Sicherheit
            return picture_path
            
    default_image = os.path.join(PICTURE_DIR, "no_picture_male.png")
    
    if os.path.exists(default_image):
        return default_image
    else:
        # Letzter Ausweg, falls gar nichts da ist
        return None




# %%

# Paket für Bearbeitung von Tabellen
import pandas as pd

# Paket
## zuvor !pip install plotly
## ggf. auch !pip install nbformat
import plotly.express as px


def read_my_csv():
    # Einlesen eines Dataframes
    ## "\t" steht für das Trennzeichen in der txt-Datei (Tabulator anstelle von Beistrich)
    ## header = None: es gibt keine Überschriften in der txt-Datei
    df = pd.read_csv("EGK_App/data/ekg_data/01_Ruhe.txt", sep="\t", header=None)

    # Setzt die Columnnames im Dataframe
    df.columns = ["Messwerte in mV","Zeit in ms"]
    
    # Gibt den geladen Dataframe zurück
    return df


# %%

def make_plot(df):

    # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
    fig = px.line(df.head(2000), x= "Zeit in ms", y="Messwerte in mV")
    return fig

#%% Test

#df = read_my_csv()
#fig = make_plot(df)

#fig.show()

# %%
