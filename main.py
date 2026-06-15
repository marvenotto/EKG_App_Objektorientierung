import streamlit as st
from source.person import Person
from source.ekgdata import Ekgdata

st.title("EKG & Aktivitäts-Analyse App")

# 1. Daten laden
all_persons_data = Person.load_person_data()

if all_persons_data:
    
    # Holt die echten deutschen Schlüssel aus der JSON für das Dropdown-Menü
    person_names = [f"{p.get('nachname', 'Unbekannt')}, {p.get('vorname', 'Unbekannt')}" for p in all_persons_data]
    selected_name = st.selectbox("Wähle eine Testperson aus:", person_names)
    
    # Finde die ID der ausgewählten Person heraus
    selected_index = person_names.index(selected_name)
    selected_person_id = all_persons_data[selected_index].get('id')
    
    # 2. Objektorientierung: Wir erstellen ein Person-Objekt
    current_person = Person.load_by_id(selected_person_id)
    
    if current_person:
        st.subheader(f"Daten von {current_person.firstname} {current_person.lastname}")
        
        bild = current_person.get_image()
        if bild:
            st.image(bild, width=150)
            
        st.write(f"**Alter:** {current_person.calc_age()} Jahre")
        st.write(f"**Max. Herzfrequenz:** {current_person.calc_max_heart_rate()} bpm")
        
        # 3. EKG Daten verarbeiten
        if current_person.ekg_tests:
            st.write("### EKG Tests")
            
            for ekg_info in current_person.ekg_tests:
                ekg_test = Ekgdata.load_by_id(ekg_info)
                ekg_test.find_peaks()
                hr = ekg_test.estimate_hr()
                
                st.write(f"**Datum des Tests:** {ekg_test.date}")
                st.write(f"**Geschätzte Herzfrequenz:** {hr} bpm")
                
                fig = ekg_test.plot_time_series()
                if fig:
                    st.plotly_chart(fig)
        else:
            st.info("Keine EKG-Daten für diese Person gefunden.")
else:
    st.error("Konnte keine Personen-Datenbank finden.")