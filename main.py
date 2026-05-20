import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ==============================================================================
# RELEVANTER CODE FÜR DIE AKTUELLLE ABGABE (POWER-DATA)
# ==============================================================================

st.title("Aktivitäts- & Leistungsanalyse")

# 1. Daten aus der Datei laden
try:
    # Pfad angepasst an deine Ordnerstruktur (data/activities/activity.csv)
    df_activity = pd.read_csv("data/activities/activity.csv")

    # Falls eine Zeit-Spalte existiert, konvertieren wir sie zur besseren Darstellung
    if "Zeit" in df_activity.columns:
        df_activity["Zeit"] = pd.to_datetime(df_activity["Zeit"], errors="ignore")
    elif "time" in df_activity.columns:
        df_activity["Zeit"] = pd.to_datetime(df_activity["time"], errors="ignore")
    else:
        # Falls keine Zeitspalte da ist, erstellen wir einen fortlaufenden Index (Sekunden)
        df_activity["Zeit"] = df_activity.index

    # Dynamische Spalten-Erkennung (falls die CSV englische Header hat)
    p_col = "Leistung" if "Leistung" in df_activity.columns else "power"
    hr_col = "Herzfrequenz" if "Herzfrequenz" in df_activity.columns else "heart_rate"
    t_col = "Zeit"

    # 2. Max HR Eingabe über die App
    max_hr = st.number_input(
        "Maximale Herzfrequenz (max HR) eingeben:",
        min_value=100,
        max_value=250,
        value=190,
    )

    st.markdown("---")

    # 3. Mittelwert & Maximalwert der Leistung berechnen und anzeigen
    mean_power = df_activity[p_col].mean()
    max_power = df_activity[p_col].max()

    col1, col2 = st.columns(2)
    col1.metric(label="Durchschnittliche Leistung", value=f"{mean_power:.1f} W")
    col2.metric(label="Maximale Leistung", value=f"{max_power:.1f} W")

    st.markdown("---")

    # 4. Herzfrequenz-Zonen berechnen (Prozentsätze basierend auf max_hr)
    # Zone 1 (50-60%), Zone 2 (60-70%), Zone 3 (70-80%), Zone 4 (80-90%), Zone 5 (90-100%)
    bins = [0, 0.5 * max_hr, 0.6 * max_hr, 0.7 * max_hr, 0.8 * max_hr, 0.9 * max_hr, max_hr, 300]
    labels = ["Unter Z1", "Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5", "Über Z5"]
    
    df_activity["Zone"] = pd.cut(df_activity[hr_col], bins=bins, labels=labels)

    # 5. Zeit pro Zone (in Minuten) & Durchschnittsleistung pro Zone berechnen
    # Jede Zeile in der CSV wird als 1 Sekunde gezählt.
    zonen_analyse = (
        df_activity.groupby("Zone", observed=False)
        .agg(
            Sekunden=(p_col, "count"),
            Avg_Leistung=(p_col, "mean"),
        )
        .reset_index()
    )

    # Nur die echten Zonen 1 bis 5 filtern
    zonen_analyse = zonen_analyse[zonen_analyse["Zone"].isin([f"Zone {i}" for i in range(1, 6)])]
    # Sekunden in Minuten umrechnen
    zonen_analyse["Zeit (Minuten)"] = (zonen_analyse["Sekunden"] / 60).round(2)

    # Tabelle in Streamlit anzeigen
    st.subheader("Auswertung der Herzfrequenz-Zonen")
    st.dataframe(
        zonen_analyse[["Zone", "Zeit (Minuten)", "Avg_Leistung"]].rename(
            columns={"Avg_Leistung": "Ø Leistung (Watt)"}
        ),
        hide_index=True,
        use_container_width=True
    )

    # 6. Interaktiven Plotly-Plot (2 Y-Achsen + farbige Zonen im Hintergrund) erstellen
    st.subheader("Interaktiver Verlauf von Leistung & Puls")
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Kurve 1: Leistung (Linke Y-Achse)
    fig.add_trace(
        go.Scatter(x=df_activity[t_col], y=df_activity[p_col], name="Leistung (W)", line=dict(color="green")),
        secondary_y=False,
    )

    # Kurve 2: Herzfrequenz (Rechte Y-Achse)
    fig.add_trace(
        go.Scatter(x=df_activity[t_col], y=df_activity[hr_col], name="Herzfrequenz (bpm)", line=dict(color="red")),
        secondary_y=True,
    )

    # Hintergrundfarben für die Zonen definieren
    colors = {
        "Zone 1": "rgba(200, 200, 200, 0.15)",  # Grau
        "Zone 2": "rgba(0, 255, 0, 0.08)",     # Grün
        "Zone 3": "rgba(255, 255, 0, 0.08)",   # Gelb
        "Zone 4": "rgba(255, 165, 0, 0.12)",   # Orange
        "Zone 5": "rgba(255, 0, 0, 0.12)",     # Rot
    }

    zone_limits = [0.5 * max_hr, 0.6 * max_hr, 0.7 * max_hr, 0.8 * max_hr, 0.9 * max_hr, max_hr]
    zone_names = ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"]

    # Farbige Rechtecke in den Hintergrund legen
    for i in range(len(zone_names)):
        fig.add_hrect(
            y0=zone_limits[i],
            y1=zone_limits[i + 1],
            fillcolor=colors[zone_names[i]],
            annotation_text=zone_names[i],
            annotation_position="outside top left",
            secondary_y=True,
            layer="below",
            line_width=0,
        )

    # Achsenbeschriftungen und Layout optimieren
    fig.update_xaxes(title_text="Zeit / Verlauf")
    fig.update_yaxes(title_text="<b>Leistung</b> (Watt)", secondary_y=False)
    fig.update_yaxes(title_text="<b>Herzfrequenz</b> (bpm)", secondary_y=True)
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))

    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error(
        "Datei 'activity.csv' wurde nicht gefunden. Bitte prüfe, ob sie im Ordner 'data/activities/' liegt!"
    )
except Exception as e:
    st.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")