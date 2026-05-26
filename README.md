# 📊 EKG & Aktivitäts-Analyse App

Eine interaktive **Streamlit-Anwendung** zur Analyse und Visualisierung von Fitness- und EKG-Daten. Die App berechnet detaillierte Leistungsstatistiken, teilt Aktivitäten in 5 Belastungszonen ein und präsentiert die Daten mit interaktiven Plotly-Diagrammen.

---

## ✨ Features

- 👤 **Versuchspersonenverwaltung** – Wähle aus mehreren Testpersonen aus
- 📈 **EKG-Datenanalyse** – Visualisierung von Herzfrequenzdaten über die Zeit
- 💪 **Leistungsdatenanalyse** – Detaillierte Leistungsstatistiken und -zonen
- 🎯 **Dynamische Belastungszonen** – 5 Herzfrequenzzonen basierend auf maximaler Herzfrequenz
- 📊 **Interaktive Visualisierung** – Plotly-Diagramme zum Erforschen der Daten
- 🖼️ **Personenfotos** – Anzeige von Profilbildern
- 📱 **Responsive Design** – Optimiert für verschiedene Bildschirmgrößen

---

## 🚀 Schnellstart

### Voraussetzungen
- Python 3.13 oder höher
- **PDM** – [Installation](https://pdm-project.org/latest/#installation)

### Installation & Ausführung

1. **Repository klonen und in das Verzeichnis wechseln:**
   ```bash
   git clone <repository-url>
   cd EKG_App_Steamlit
   ```

2. **Abhängigkeiten mit PDM installieren:**
   ```bash
   pdm install
   ```

3. **App starten:**
   ```bash
   pdm run streamlit run main.py
   ```

4. **Browser öffnen:**
   ```
   Local URL: http://localhost:8501
   Network URL: http://10.55.15.193:8501
   ```

> **💡 Tipp:** VSCode kann beim ersten Start der App kurz langsam sein – einfach ein paar Sekunden Geduld haben fals nichts passiert, einfach stoppen mit ^c und erneut pdm run streamlit run main.py ausführen! 

---

## 📁 Projektstruktur

```
EKG_App_Steamlit/
├── main.py                 # Hauptanwendung
├── pyproject.toml          # PDM Projektdatei
├── README.md               # Diese Datei
├── data/
│   ├── person_db.json      # Personendatensätze
│   ├── activities/
│   │   └── activity.csv    # Aktivitätsdaten
│   ├── ekg_data/
│   │   ├── 01_Ruhe.txt     # EKG Ruhemessungen
│   │   ├── 02_Ruhe.txt
│   │   ├── 03_Ruhe.txt
│   │   ├── 04_Belastung.txt # EKG Belastungsmessungen
│   │   ├── 05_Belastung.txt
│   │   └── ReadMe.txt
│   └── pictures/           # Profilbilder der Versuchspersonen
└── source/
    ├── read_data.py        # Datenlese-Funktionen
    ├── read_pandas.py      # Pandas und Plotly Funktionen
    └── my_first_pandas.py  # Zusätzliche Pandas-Tools
```

---

## 📋 Anforderungen

| Paket | Version | Zweck |
|-------|---------|-------|
| `streamlit` | ≥1.57.0 | Web-Framework für die UI |
| `pandas` | ≥3.0.3 | Datenverwaltung und -analyse |
| `numpy` | ≥2.4.4 | Numerische Berechnungen |
| `plotly-express` | ≥0.4.1 | Interaktive Datenvisualisierung |

---

## 💻 Verwendung

### Daten anzeigen
1. Wähle eine **Versuchsperson** aus dem Dropdown-Menü
2. Klicke auf **"Daten anzeigen"**
3. Die Personeninformationen und das Foto werden angezeigt

### Reiter
- **EKG-Data** – Visualisierung der Herzfrequenzmessungen
- **Power-Data** – Leistungsstatistiken und Belastungszonen

---

## 🏋️ Die 5 Belastungszonen erklärt

Die App teilt die Herzfrequenz automatisch in **5 Trainings- und Belastungszonen** ein. Diese Zonen basieren auf der **maximalen Herzfrequenz (HFmax)** der ausgewählten Person.

| Zone | Name | Herzfrequenz | Trainingseffekt | Beschreibung |
|------|------|-------------|-----------------|--------------|
| **1** | 🟢 Erholung | 50–60% HFmax | Regeneration & Ausdauer | Niedriger Puls, leichte Aktivität, ideal zum Warmlaufen oder Erholen |
| **2** | 🔵 Aerob | 60–70% HFmax | Fettverbrennung & Grundlagen | Komfortables Training, länger durchzuhalten, Basis-Ausdauertraining |
| **3** | 🟡 Anaerobe Schwelle | 70–80% HFmax | Ausdauer-Verbesserung | Anstrengendes Training, höhere Intensität, Grenzbereich |
| **4** | 🟠 VO₂-Max | 80–90% HFmax | Maximale Fitness | Intensives Training, Verbesserung der Leistung, kurzzeitig |
| **5** | 🔴 Sprintzone | 90–100% HFmax | Maximale Leistung | Maximale Intensität, nur kurz möglich, Sprinttraining |

### 📍 Wo finde ich die Zonen in der App?

- Gehe zum Reiter **"Power-Data"**
- Das Diagramm zeigt die **zeitliche Verteilung** der Herzfrequenz auf alle 5 Zonen
- Farbcodierung (wie oben) macht die Intensität auf einen Blick sichtbar
- **Statistiken** zeigen, wie viel Zeit in jeder Zone verbracht wurde

### 💡 Beispiel-Interpretation

Wenn du eine **Ruhe-Messung** öffnest:
- 🟢 Hauptsächlich in Zone 1–2 (normale Ruheherzfrequenz)

Bei einer **Belastungs-Messung**:
- 🟡🟠🔴 Verteilung über mehrere Zonen, mit Spitzen in Zone 4–5 (intensives Training)

---

## 🔧 Konfiguration & Entwicklung

### Neue Abhängigkeiten hinzufügen
```bash
pdm add <paket-name>
```

### Abhängigkeiten aktualisieren
```bash
pdm update
```

### Entwicklungsmodus
```bash
pdm run streamlit run main.py --logger.level=debug
```

---

## 📄 Lizenz

Dieses Projekt steht unter der **MIT-Lizenz**. Siehe [LICENSE](LICENSE) für weitere Informationen.

---

## 👨‍💻 Autor

**Cedric Rissi**  
📧 [cedric.rissi2003@gmail.com](mailto:cedric.rissi2003@gmail.com)

---

## 🐛 Feedback & Support

Hast du Fragen oder Probleme? Erstelle gerne ein Issue im Repository oder kontaktiere den Autor direkt.
