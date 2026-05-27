import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Custom modules for reading data and plotting
from source.read_write_data import read_my_csv, get_person_list, get_person_dict, get_person_picture, add_person
# from source.read_pandas import make_plot


def submit_new_person():
    result = add_person(
        st.session_state.input_vorname,
        st.session_state.input_nachname,
        st.session_state.input_alter,
    )
    st.session_state.add_person_result = result

    if result["success"]:
        st.session_state.input_vorname = ""
        st.session_state.input_nachname = ""
        st.session_state.input_alter = 25


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

# --- NEUE VERSUCHSPERSON HINZUFÜGEN ---
with st.expander("➕ Neue Versuchsperson hinzufügen"):
    st.write("### Neue Person eintragen")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_vorname = st.text_input("Vorname", placeholder="z.B. Max", key="input_vorname")
    
    with col2:
        new_nachname = st.text_input("Nachname", placeholder="z.B. Mustermann", key="input_nachname")
    
    with col3:
        new_alter = st.number_input("Alter", min_value=10, max_value=100, value=25, key="input_alter")
    
    col_btn, col_info = st.columns([1, 3])
    
    with col_btn:
        st.button(
            "Person hinzufügen",
            key="btnAddPerson",
            on_click=submit_new_person,
        )

    with col_info:
        st.info("💡 Nach dem Hinzufügen findest du die neue Person in der Auswahl-Liste unten!")

    if "add_person_result" in st.session_state:
        result = st.session_state.add_person_result
        if result["success"]:
            st.success(result["message"])
            st.write("✅ Die neue Person wurde erstellt und steht jetzt oben in der Auswahl zur Verfügung.")
        elif result["error_type"] == "duplicate":
            st.warning(result["message"])
        else:
            st.error(result["message"])

st.divider()  # Visuelle Trennung

# --- Handle data fetching when the action button is clicked --- 
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
    # --- TAB 1: EKG Data Visualization ---
    with tab1:
        st.header("EKG-Data")
        
        # Load and plot raw EKG data
        df = read_my_csv()

        # Generate an EKG line plot using Plotly Subplots
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
        
        # Startwert ermitteln
        start_time = df["Zeit in ms"].min()
        end_time = start_time + 2500  
        
        fig.update_layout(
            title="EKG-Verlauf",
            xaxis_title="Zeit in ms",
            yaxis_title="Messwerte in mV",
            template="plotly_white",
            margin=dict(l=40, r=20, t=50, b=40),
            xaxis=dict(
                range=[start_time, end_time],
                tickformat="d"  # <-- Erzwingt die Ganzzahl-Darstellung (kein 'k' mehr!)
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    # --- TAB 2: Activity and Power Analysis ---
    with tab2:
        st.header("Power-Data")

        # Task 3: Comprehensive Activity Analysis
        st.title("Aktivitätsanalyse")

        # 1. Data Ingestion & Cleaning
        df = pd.read_csv("data/activities/activity.csv")
        df = df.dropna(subset=["PowerOriginal"])       # Drop missing power data rows
        df["Echte_Sekunden"] = range(len(df))          # Generate a continuous time sequence in seconds

        # 2. Calculate maximum heart rate directly from data (no user input)
        max_hr = df["HeartRate"].max()

        # 3. Summary Statistics
        st.write(f"Maximaler Puls: {df['HeartRate'].max()} bpm")
        st.write(f"Maximale Leistung: {df['PowerOriginal'].max():.1f} W")
        st.write(f"Durchschnittliche Leistung: {df['PowerOriginal'].mean():.1f} W")

        # 4. Heart Rate Zone Binning
        # Define thresholds (in BPM) based on the user's custom maximum heart rate
        # Zones:
        #  - Zone 1: 50-60% HFmax
        #  - Zone 2: 60-70% HFmax
        #  - Zone 3: 70-80% HFmax
        #  - Zone 4: 80-90% HFmax
        #  - Zone 5: 90-100% HFmax
        
        bins = [0.5 * max_hr, 0.6 * max_hr, 0.7 * max_hr, 0.8 * max_hr, 0.9 * max_hr, max_hr + 1]
        labels = ["🟢 Zone 1", "🔵 Zone 2", "🟡 Zone 3", "🟠 Zone 4", "🔴 Zone 5"]
        df["Zone"] = pd.cut(df["HeartRate"], bins=bins, labels=labels, right=False)

        # 5. Zone Analysis & Percentage Computation
        # Total duration of valid training data in seconds
        gesamt_sekunden = len(df)

        # Aggregate performance metrics grouped by training zones
        zonen = df.groupby("Zone", observed=False).agg(
            Minuten=("PowerOriginal", lambda x: round(len(x) / 60, 2)),
            Prozent=("PowerOriginal", lambda x: round((len(x) / gesamt_sekunden) * 100, 1)),
            Avg_Leistung=("PowerOriginal", "mean")
        ).reset_index()

        # Remove rows with NaN zones (if any)
        zonen = zonen.dropna(subset=["Zone"])

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
        st.plotly_chart(fig_both, width='stretch')
        st.plotly_chart(fig_Herz, width='stretch')
        st.plotly_chart(fig_Watt, width='stretch')