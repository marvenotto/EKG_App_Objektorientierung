import streamlit as st
#import pandas as pd
#import numpy as np

from read_data import get_person_list, get_person_age


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