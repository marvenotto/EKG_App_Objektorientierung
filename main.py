import streamlit as st
from source.read_data import get_person_list, get_person_dict, get_person_picture

from source.read_pandas import read_my_csv
from source.read_pandas import make_plot

st.write("# EKG APP")
st.write("## Versuchsperson auswählen")

# Initialisiere Session State Variablen
if 'current_user_data' not in st.session_state:
    st.session_state.current_user_data = None

person_list = get_person_list()

current_user = st.selectbox(
    'Versuchsperson',
    options=person_list,
    key="sbVersuchsperson"
)

if st.button("Daten anzeigen", key="btnDatenAnzeigen"):

    all_persons = get_person_dict()

    if current_user in all_persons:
        st.session_state.current_user_data = all_persons[current_user]
        st.session_state.picture_path = get_person_picture(current_user)

# Anzeige
if st.session_state.current_user_data:

    user = st.session_state.current_user_data

    st.write(f"### Daten von {current_user}")
    st.write(f"**Alter:** {user['alter']}")

    st.image(st.session_state.picture_path, width=200)

# Tabs
tab1, tab2 = st.tabs(["EKG-Data", "Power-Data"])

with tab1:

    st.header("EKG-Data")

    df = read_my_csv()
    fig = make_plot(df)

    st.plotly_chart(fig)

with tab2:

    st.header("Power-Data")