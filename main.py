import streamlit as st
from source.read_data import get_person_list, get_person_dict, get_person_picture
from source.read_data import get_person_list, get_person_dict, get_person_picture



st.write("# EKG APP")
st.write("## Versuchsperson auswählen")

# Initialisiere Session State Variablen
if 'current_user_data' not in st.session_state:
    st.session_state.current_user_data = None

person_list = get_person_list()
current_user = st.selectbox('Versuchsperson', options=person_list, key="sbVersuchsperson")

if st.button("Daten anzeigen", key="btnDatenAnzeigen"):
    # Daten einmalig beim Klick laden und im State speichern
    all_persons = get_person_dict()
    if current_user in all_persons:
        st.session_state.current_user_data = all_persons[current_user]
        st.session_state.picture_path = get_person_picture(current_user)
        print(get_person_picture(current_user)) # Debug-Ausgabe

# Anzeige (bleibt bestehen, solange etwas im State ist)
if st.session_state.current_user_data:
    user = st.session_state.current_user_data
    st.write(f"### Daten von {current_user}")
    st.write(f"**Alter:** {user['alter']}")
    st.image(st.session_state.picture_path, width=200)



st.write("# EKG APP")
st.write("## Versuchsperson auswählen")

# Initialisiere Session State Variablen
if 'current_user_data' not in st.session_state:
    st.session_state.current_user_data = None

person_list = get_person_list()
current_user = st.selectbox('Versuchsperson', options=person_list, key="sbVersuchsperson")

if st.button("Daten anzeigen", key="btnDatenAnzeigen"):
    # Daten einmalig beim Klick laden und im State speichern
    all_persons = get_person_dict()
    if current_user in all_persons:
        st.session_state.current_user_data = all_persons[current_user]
        st.session_state.picture_path = get_person_picture(current_user)
        print(get_person_picture(current_user)) # Debug-Ausgabe

# Anzeige (bleibt bestehen, solange etwas im State ist)
if st.session_state.current_user_data:
    user = st.session_state.current_user_data
    st.write(f"### Daten von {current_user}")
    st.write(f"**Alter:** {user['alter']}")
    st.image(st.session_state.picture_path, width=200)