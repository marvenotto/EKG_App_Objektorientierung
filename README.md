# EKG & Aktivitaets-Analyse App

Diese Streamlit-Anwendung dient der interaktiven Analyse und Visualisierung von EKG-Daten. Das Projekt wurde vollstaendig objektorientiert umgesetzt. Personen- und EKG-Daten werden in eigenen Python-Klassen (Person und Ekgdata) strukturiert verwaltet, um eine automatische Peak-Erkennung durchzufuehren und die Herzfrequenz zu berechnen.

## Projekt starten (PDM)

Dieses Projekt nutzt PDM zur Verwaltung der Abhaengigkeiten und der virtuellen Umgebung. Um die App lokal auf deinem System auszufuehren, muessen folgende Schritte im Terminal durchgefuehrt werden:

1. Virtuelle Umgebung einrichten und benoetigte Pakete installieren:
   ```bash
   pdm install

## Die Streamlit-App starten:
   pdm run streamlit run main.py