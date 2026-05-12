import streamlit as st




# Eine Überschrift der ersten Ebene
st.write("# EKG APP")

# Eine Überschrift der zweiten Ebene
st.write("## Versuchsperson auswählen")



# Eine Auswahlbox
current_user = st.selectbox(
    'Versuchsperson',
    options = ["Cedi Tyson", "Otto Otto", "Max"], key="sbVersuchsperson")

# Ein Button
if st.button("Daten anzeigen", key="btnDatenAnzeigen"):
    st.write("Daten von " + current_user)