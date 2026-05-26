import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Custom modules for reading data and plotting
from source.read_data import get_person_list, get_person_dict, get_person_picture
from source.read_pandas import read_my_csv, make_plot

# App title and initial user selection UI
st.write("# EKG APP")
st.write("## Versuchsperson auswählen")

# Initialize session state variables to persist user data across reruns
if 'current_user_data' not in st.session_state:
    st.session_state.current_user_data = None

# Fetch the list of available subjects and display the selection dropdown
person_list = get_person_list()
current_user = st.selectbox(
    'Versuchsperson',
    options=person_list,
    key="sbVersuchsperson"
)

# Handle data fetching when the action button is clicked
if st.button("Daten anzeigen", key="btnDatenAnzeigen"):
    all_persons = get_person_dict()

    if current_user in all_persons:
        # Save selected user data and picture path to session state
        st.session_state.current_user_data = all_persons[current_user]
        st.session_state.picture_path = get_person_picture(current_user)

# Display selected subject's profile information
if st.session_state.current_user_data:
    user = st.session_state.current_user_data

    st.write(f"### Daten von {current_user}")
    st.write(f"**Alter:** {user['alter']}")
    st.image(st.session_state.picture_path, width=200)

# Set up organized views using layout tabs
tab1, tab2 = st.tabs(["EKG-Data", "Power-Data"])

# --- TAB 1: EKG Data Visualization ---
with tab1:
    st.header("EKG-Data")
    
    # Load and plot raw EKG data
    df = read_my_csv()
    fig = make_plot(df)
    st.plotly_chart(fig)

# --- TAB 2: Activity and Power Analysis ---
with tab2:
    st.header("Power-Data")

    # Task 3: Comprehensive Activity Analysis
    st.title("Aktivitätsanalyse")

    # 1. Data Ingestion & Cleaning
    df = pd.read_csv("data/activities/activity.csv")
    df = df.dropna(subset=["PowerOriginal"])       # Drop missing power data rows
    df["Echte_Sekunden"] = range(len(df))          # Generate a continuous time sequence in seconds

    # 2. User input for performance metrics calculation
    max_hr = st.number_input("Maximale Herzfrequenz:", value=190)

    # 3. Summary Statistics
    st.write(f"Durchschnittliche Leistung: {df['PowerOriginal'].mean():.1f} W")
    st.write(f"Maximale Leistung: {df['PowerOriginal'].max():.1f} W")

    # 4. Heart Rate Zone Binning
    # Define thresholds and labels based on the user's custom maximum heart rate
    bins = [0, 0.5 * max_hr, 0.6 * max_hr, 0.7 * max_hr, 0.8 * max_hr, 0.9 * max_hr, max_hr, 300]
    labels = ["Unter Z1", "Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5", "Über Z5"]
    df["Zone"] = pd.cut(df["HeartRate"], bins=bins, labels=labels)

    # 5. Zone Analysis & Percentage Computation
    # Total duration of valid training data in seconds
    gesamt_sekunden = len(df)

    # Aggregate performance metrics grouped by training zones
    zonen = df.groupby("Zone", observed=False).agg(
        Minuten=("PowerOriginal", lambda x: round(len(x) / 60, 2)),
        Prozent=("PowerOriginal", lambda x: round((len(x) / gesamt_sekunden) * 100, 1)),
        Avg_Leistung=("PowerOriginal", "mean")
    ).reset_index()

    # Filter out edge cases to focus on standard training zones (1 to 5)
    zonen = zonen[zonen["Zone"].isin(["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"])]

    st.subheader("Zonen Auswertung")
    # Render the structured summary dataframe
    st.dataframe(zonen[["Zone", "Prozent", "Minuten", "Avg_Leistung"]])

    # 6. Interactive Visualizations & Charts
    st.subheader("Interaktiver Verlauf")

    # Instantiate separate figure objects for isolated and overlay analytics
    fig_Watt = make_subplots()
    fig_Herz = make_subplots(specs=[[{"secondary_y": True}]])
    fig_both = make_subplots(specs=[[{"secondary_y": True}]])

    # Trace 1: Power output timeline (Minutes vs. Watts)
    fig_Watt.add_trace(
        go.Scatter(x=df["Echte_Sekunden"] / 60, y=df["PowerOriginal"], name="Leistung (W)", line_color="white"),
        secondary_y=False,
    )
    
    # Trace 2: Heart rate timeline (Minutes vs. BPM)
    fig_Herz.add_trace(
        go.Scatter(x=df["Echte_Sekunden"] / 60, y=df["HeartRate"], name="Puls (bpm)", line_color="red"),
        secondary_y=True,
    )

    # Combined View: Superimpose Power and Heart Rate for easy overview comparison
    fig_both.add_trace(
        go.Scatter(x=df["Echte_Sekunden"] / 60, y=df["PowerOriginal"], name="Leistung (W)", line_color="white"),
        secondary_y=False,
    )
    fig_both.add_trace(
        go.Scatter(x=df["Echte_Sekunden"] / 60, y=df["HeartRate"], name="Puls (bpm)", line_color="red"),
        secondary_y=True,
    )

    # Update global axes titles and properties for clarity
    fig_Watt.update_xaxes(title_text="Zeit (Minuten)")
    fig_Herz.update_xaxes(title_text="Zeit (Minuten)")
    fig_Watt.update_yaxes(title_text="Leistung (W)", secondary_y=False)
    fig_Herz.update_yaxes(title_text="Puls (bpm)", secondary_y=True)
    
    fig_both.update_xaxes(title_text="Zeit (Minuten)")
    fig_both.update_yaxes(title_text="Leistung (W)", secondary_y=False)
    fig_both.update_yaxes(title_text="Puls (bpm)", secondary_y=True)

    # Render dynamic Plotly plots inside Streamlit layout blocks
    st.plotly_chart(fig_both, use_container_width=True)
    st.plotly_chart(fig_Herz, use_container_width=True)
    st.plotly_chart(fig_Watt, use_container_width=True)