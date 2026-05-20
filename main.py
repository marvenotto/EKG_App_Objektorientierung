import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

st.title("Aktivitätsanalyse")

# 1. Daten laden
df = pd.read_csv("data/activities/activity.csv")

# Leere Zeilen löschen
df = df.dropna(subset=["PowerOriginal"])

# NEU: Da 'Duration' immer 1 ist, bauen wir uns eine echte, 
# fortlaufende Achse (Zeilen von 0 bis Ende durchzählen = Sekunden)
df["Echte_Sekunden"] = df.groupby(level=0).cumcount() + df.index

# 2. Max HR Eingabe
max_hr = st.number_input("Maximale Herzfrequenz:", value=190)

# 3. Einfache Metriken berechnen
st.write(f"Durchschnittliche Leistung: {df['PowerOriginal'].mean():.1f} W")
st.write(f"Maximale Leistung: {df['PowerOriginal'].max():.1f} W")

# 4. Herzfrequenz-Zonen einteilen
bins = [0, 0.5 * max_hr, 0.6 * max_hr, 0.7 * max_hr, 0.8 * max_hr, 0.9 * max_hr, max_hr, 300]
labels = ["Unter Z1", "Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5", "Über Z5"]
df["Zone"] = pd.cut(df["HeartRate"], bins=bins, labels=labels)

# 5. Zeit und Durchschnittsleistung pro Zone berechnen
zonen = df.groupby("Zone", observed=False).agg(
    Minuten=("PowerOriginal", lambda x: round(len(x) / 60, 2)),
    Avg_Leistung=("PowerOriginal", "mean")
).reset_index()

zonen = zonen[zonen["Zone"].isin(["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"])]

st.subheader("Zonen Auswertung")
st.dataframe(zonen)

# 6. Interaktiver Verlauf (jetzt mit der echten Zeitachse in Minuten)
st.subheader("Interaktiver Verlauf")
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Wir nehmen unsere neue Spalte 'Echte_Sekunden' und teilen sie durch 60 für Minuten
fig.add_trace(
    go.Scatter(x=df["Echte_Sekunden"] / 60, y=df["PowerOriginal"], name="Leistung (W)"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df["Echte_Sekunden"] / 60, y=df["HeartRate"], name="Puls (bpm)"),
    secondary_y=True,
)

fig.update_xaxes(title_text="Zeit (Minuten)")

st.plotly_chart(fig)