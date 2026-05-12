import streamlit as st
#import pandas as pd
#import numpy as np

from read_data import get_person_list, get_person_age, get_person_picture


# Eine Überschrift der ersten Ebene
st.write("# EKG APP")

# Eine Überschrift der zweiten Ebene
st.write("## Versuchsperson auswählen")



# Eine Auswahlbox
current_user = st.selectbox(
    'Versuchsperson',
    options = get_person_list(), key="sbVersuchsperson")

# Ein Button
if st.button("Daten anzeigen", key="btnDatenAnzeigen"):
    st.write("Daten von " + current_user)
    st.write("Alter: " + str(get_person_age(current_user)))

    # Bildpfad von der Funktion holen
    found_path = get_person_picture(current_user)

    # Logik für den Session State oder direkt für die Anzeige:
    if found_path:
        st.session_state.picture_path = found_path
    else:
        # Fallback, wenn kein Bild existiert
        st.session_state.picture_path = 'data/pictures/no_picture_male.jpg'

    # Anzeigen des Bildes
    st.image(st.session_state.picture_path, width=200)