import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

st.title("Aktivitätsanalyse")

# 1. Daten laden und säubern
df = pd.read_csv("data/activities/activity.csv")
df = df.dropna(subset=["PowerOriginal"])
df["Echte_Sekunden"] = range(len(df))

# 2. Max HR Eingabe
max_hr = st.number_input("Maximale Herzfrequenz:", value=190)

# 3. Metriken
st.write(f"Durchschnittliche Leistung: {df['PowerOriginal'].mean():.1f} W")
st.write(f"Maximale Leistung: {df['PowerOriginal'].max():.1f} W")

# 4. Herzfrequenz-Zonen einteilen
bins = [0, 0.5 * max_hr, 0.6 * max_hr, 0.7 * max_hr, 0.8 * max_hr, 0.9 * max_hr, max_hr, 300]
labels = ["Unter Z1", "Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5", "Über Z5"]
df["Zone"] = pd.cut(df["HeartRate"], bins=bins, labels=labels)

# 5. Zonen-Auswertung inklusive Prozent-Berechnung
# len(df) gibt uns die Gesamtzahl aller gültigen Sekunden im Training
gesamt_sekunden = len(df)

zonen = df.groupby("Zone", observed=False).agg(
    Minuten=("PowerOriginal", lambda x: round(len(x) / 60, 2)),
    Prozent=("PowerOriginal", lambda x: round((len(x) / gesamt_sekunden) * 100, 1)),
    Avg_Leistung=("PowerOriginal", "mean")
).reset_index()

# Filter auf die Kernzonen
zonen = zonen[zonen["Zone"].isin(["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"])]

st.subheader("Zonen Auswertung")
# Anzeige der Tabelle mit der neuen Prozent-Spalte
st.dataframe(zonen[["Zone", "Prozent", "Minuten", "Avg_Leistung"]])

# 6. Interaktiver Verlauf
st.subheader("Interaktiver Verlauf")
#fig = make_subplots(specs=[[{"secondary_y": True}]])

fig_Watt = make_subplots()
fig_Herz = make_subplots(specs=[[{"secondary_y": True}]])
fig_both = make_subplots(specs=[[{"secondary_y": True}]])


fig_Watt.add_trace(
    go.Scatter(x=df["Echte_Sekunden"] / 60, y=df["PowerOriginal"], name="Leistung (W)", line_color="white"),
    secondary_y=False,
)
fig_Herz.add_trace(
    go.Scatter(x=df["Echte_Sekunden"] / 60, y=df["HeartRate"], name="Puls (bpm)", line_color="red"),
    secondary_y=True,
)

#Beide in einem für die Übersicht
fig_both.add_trace(
    go.Scatter(x=df["Echte_Sekunden"] / 60, y=df["PowerOriginal"], name="Leistung (W)", line_color="white"),
    secondary_y=False,
)
fig_both.add_trace(
    go.Scatter(x=df["Echte_Sekunden"] / 60, y=df["HeartRate"], name="Puls (bpm)", line_color="red"),
    secondary_y=True,
)



fig_Watt.update_xaxes(title_text="Zeit (Minuten)")
fig_Herz.update_xaxes(title_text="Zeit (Minuten)")
fig_Watt.update_yaxes(title_text="Leistung (W)", secondary_y=False)
fig_Herz.update_yaxes(title_text="Puls (bpm)", secondary_y=True)
fig_both.update_xaxes(title_text="Zeit (Minuten)")
fig_both.update_yaxes(title_text="Leistung (W)", secondary_y=False)


st.plotly_chart(fig_both, use_container_width=True)
st.plotly_chart(fig_Herz, use_container_width=True)
st.plotly_chart(fig_Watt, use_container_width=True)