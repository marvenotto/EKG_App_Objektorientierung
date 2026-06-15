import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Hier laden wir unsere eigenen Funktionen aus dem 'source'-Ordner
from source.read_write_data import read_my_txt, get_person_list, get_person_dict, get_person_picture, add_person

# --- FUNKTION: NEUE PERSON SPEICHERN ---
# Diese Funktion nimmt die Eingaben aus dem Formular und speichert eine komplett neue Versuchsperson
def submit_new_person():
    result = add_person(
        st.session_state.input_vorname,
        st.session_state.input_nachname,
        st.session_state.input_alter,
    )
    st.session_state.add_person_result = result

    # Wenn das Speichern geklappt hat, leeren wir die Felder wieder für die nächste Person
    if result["success"]:
        st.session_state.input_vorname = ""
        st.session_state.input_nachname = ""
        st.session_state.input_alter = 25


# Start der Webseite: Titel und Auswahlbereich anzeigen
st.write("# EKG APP")
st.write("## Versuchsperson auswählen")


# Zwischenspeicher anlegen, damit unsere Daten beim Neuladen der Seite nicht verschwinden
if 'current_user_data' not in st.session_state:
    st.session_state.current_user_data = None

# Standardwerte für unser neues Formular festlegen (leere Felder für Namen, Alter auf 25)
if 'input_vorname' not in st.session_state:
    st.session_state.input_vorname = ""
if 'input_nachname' not in st.session_state:
    st.session_state.input_nachname = ""
if 'input_alter' not in st.session_state:
    st.session_state.input_alter = 25

# Namensliste aller bekannten Personen laden und das Dropdown-Menü bauen
person_list = get_person_list()
current_user = st.selectbox(
    'Versuchsperson',
    options=person_list,
    key="sbVersuchsperson"
)

# --- BEREICH: NEUE VERSUCHSPERSON HINZUFÜGEN ---
# Hier bauen wir ein ausklappbares Formular, um direkt in der App neue Tester anzulegen
with st.expander("➕ Neue Versuchsperson hinzufügen"):
    st.write("### Neue Person eintragen")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_vorname = st.text_input("Vorname", placeholder="z.B. Max", key="input_vorname")
    
    with col2:
        new_nachname = st.text_input("Nachname", placeholder="z.B. Mustermann", key="input_nachname")
    
    with col3:
        new_alter = st.number_input("Alter", min_value=10, max_value=100, key="input_alter")
    
    col_btn, col_info = st.columns([1, 3])
    
    with col_btn:
        # Button löst unsere Speicher-Funktion von ganz oben aus
        st.button(
            "Person hinzufügen",
            key="btnAddPerson",
            on_click=submit_new_person,
        )

    with col_info:
        st.info("💡 Nach dem Hinzufügen findest du die neue Person in der Auswahl-Liste unten!")

    # Feedback für den User: Hat das Speichern geklappt oder gab es einen Fehler (z.B. Person existiert schon)?
    if "add_person_result" in st.session_state:
        result = st.session_state.add_person_result
        if result["success"]:
            st.success(result["message"])
            st.write("✅ Die neue Person wurde erstellt und steht jetzt oben in der Auswahl zur Verfügung.")
        elif result["error_type"] == "duplicate":
            st.warning(result["message"])
        else:
            st.error(result["message"])

st.divider()  # Optischer Trennstrich auf der Webseite

# --- DATEN ANZEIGEN ---
# Wenn auf 'Daten anzeigen' geklickt wird, laden wir alle Infos zur ausgewählten Person
if st.button("Daten anzeigen", key="btnDatenAnzeigen"):
    all_persons = get_person_dict()

    if current_user in all_persons:
        # Profilbild und Datensatz im Zwischenspeicher sichern
        st.session_state.current_user_data = all_persons[current_user]
        st.session_state.picture_path = get_person_picture(current_user)

    # Profilbild und Alter der Person oben auf der Webseite ausgeben
    if st.session_state.current_user_data:
        user = st.session_state.current_user_data

        st.write(f"### Daten von {current_user}")
        st.write(f"**Alter:** {user['alter']}")
        st.image(st.session_state.picture_path, width=200)

    # Die Ansicht in zwei übersichtliche Tabs aufteilen
    tab1, tab2 = st.tabs(["EKG-Data", "Power-Data"])

    # --- TAB 1: EKG-DATEN ---
    with tab1:
        st.header("EKG-Data")
        
        # Rohe EKG-Werte aus unserer Textdatei einlesen
        df = read_my_txt("data/ekg_data/01_Ruhe.txt")

        # Ein interaktives Diagramm mit Plotly erstellen und die blaue EKG-Linie einzeichnen
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(
            go.Scatter(
                x=df["Zeit in ms"],
                y=df["Messwerte in mV"],
                mode="lines",
                name="EKG",
                line=dict(color="blue"),
            ),
            row=1,
            col=1,
        )
        
        # Den perfekten Zeitausschnitt für das Diagramm berechnen (Startwert + 2,5 Sekunden)
        start_time = df["Zeit in ms"].min()
        end_time = start_time + 2500  
        
        # Das Diagramm aufhübschen: Titel, Achsen und den berechneten Zeitausschnitt anwenden
        fig.update_layout(
            title="EKG-Verlauf",
            xaxis_title="Zeit in ms",
            yaxis_title="Messwerte in mV",
            template="plotly_white",
            margin=dict(l=40, r=20, t=50, b=40),
            xaxis=dict(
                range=[start_time, end_time],
                tickformat="d"  # Erzwingt glatte Zahlen auf der X-Achse
            )
        )

        st.plotly_chart(fig, width='stretch')

    # --- TAB 2: LEISTUNGSDATEN (POWER) ---
    with tab2:
        st.header("Power-Data")
        st.title("Aktivitätsanalyse")

        # 1. Fahrrad-Trainingsdaten einlesen und Fehlerwerte (leere Zeilen) aussortieren
        df = pd.read_csv("data/activities/activity.csv")
        df = df.dropna(subset=["PowerOriginal"])       
        
        # Eine durchgehende Zeitachse in echten Sekunden generieren
        df["Echte_Sekunden"] = range(len(df))          

        # 2. Die App sucht vollautomatisch den allerhöchsten Puls aus der Datei
        max_hr = df["HeartRate"].max()

        # 3. Die wichtigsten Eckdaten der Fahrt anzeigen (Max. Puls, Max. Leistung, Durchschnitt)
        st.write(f"Maximaler Puls: {df['HeartRate'].max()} bpm")
        st.write(f"Maximale Leistung: {df['PowerOriginal'].max():.1f} W")
        st.write(f"Durchschnittliche Leistung: {df['PowerOriginal'].mean():.1f} W")

        # 4. Den Puls in 5 Trainingszonen einteilen (basierend auf 50% bis 100% des Maximalpulses)
        bins = [0.5 * max_hr, 0.6 * max_hr, 0.7 * max_hr, 0.8 * max_hr, 0.9 * max_hr, max_hr + 1]
        labels = ["🟢 Zone 1", "🔵 Zone 2", "🟡 Zone 3", "🟠 Zone 4", "🔴 Zone 5"]
        df["Zone"] = pd.cut(df["HeartRate"], bins=bins, labels=labels, right=False)

        # 5. Auswertung: Ausrechnen, wie viele Minuten und Prozent man in welcher Zone war
        gesamt_sekunden = len(df)
        zonen = df.groupby("Zone", observed=False).agg(
            Minuten=("PowerOriginal", lambda x: round(len(x) / 60, 2)),
            Prozent=("PowerOriginal", lambda x: round((len(x) / gesamt_sekunden) * 100, 1)),
            Avg_Leistung=("PowerOriginal", "mean")
        ).reset_index()

        # Leere Trainingszonen aus der Tabelle werfen und das Ergebnis ausgeben
        zonen = zonen.dropna(subset=["Zone"])
        st.subheader("Zonen Auswertung")
        st.dataframe(zonen[["Zone", "Prozent", "Minuten", "Avg_Leistung"]])

        # 6. Interaktive Diagramme für Leistung und Puls bauen
        st.subheader("Interaktiver Verlauf")

        # Drei leere Graphen erstellen: Einer für Watt, einer für Puls, einer kombiniert
        fig_Watt = make_subplots()
        fig_Herz = make_subplots(specs=[[{"secondary_y": True}]])
        fig_both = make_subplots(specs=[[{"secondary_y": True}]])

        # Linie für die Leistung (Watt) zeichnen
        fig_Watt.add_trace(
            go.Scatter(x=df["Echte_Sekunden"] / 60, y=df["PowerOriginal"], name="Leistung (W)", line_color="white"),
            secondary_y=False,
        )
        
        # Linie für den Puls (Herzfrequenz) zeichnen
        fig_Herz.add_trace(
            go.Scatter(x=df["Echte_Sekunden"] / 60, y=df["HeartRate"], name="Puls (bpm)", line_color="red"),
            secondary_y=True,
        )

        # Kombinierte Ansicht: Beide Werte übereinanderlegen für den perfekten Überblick
        fig_both.add_trace(
            go.Scatter(x=df["Echte_Sekunden"] / 60, y=df["PowerOriginal"], name="Leistung (W)", line_color="white"),
            secondary_y=False,
        )
        fig_both.add_trace(
            go.Scatter(x=df["Echte_Sekunden"] / 60, y=df["HeartRate"], name="Puls (bpm)", line_color="red"),
            secondary_y=True,
        )

        # Alle Achsen ordentlich beschriften, damit alles direkt verständlich ist
        fig_Watt.update_xaxes(title_text="Zeit (Minuten)")
        fig_Herz.update_xaxes(title_text="Zeit (Minuten)")
        fig_Watt.update_yaxes(title_text="Leistung (W)", secondary_y=False)
        fig_Herz.update_yaxes(title_text="Puls (bpm)", secondary_y=True)
        
        fig_both.update_xaxes(title_text="Zeit (Minuten)")
        fig_both.update_yaxes(title_text="Leistung (W)", secondary_y=False)
        fig_both.update_yaxes(title_text="Puls (bpm)", secondary_y=True)

        # Die drei fertigen Diagramme ganz unten auf der Webseite ausspucken
        st.plotly_chart(fig_both, width='stretch')
        st.plotly_chart(fig_Herz, width='stretch')
        st.plotly_chart(fig_Watt, width='stretch')