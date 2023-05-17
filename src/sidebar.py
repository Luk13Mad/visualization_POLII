import streamlit as st
import util

#config sidebar
def data_sidebar():
    with st.sidebar:
        select_cellline = st.selectbox(
        'Which cell line would you like to look at?',
        ("HEK 293T","T98-G","hTert-RPE1")
        )

        select_timepoint = st.selectbox(
            "Which timepoint would you like to look at?",
            ("Early","Late"),
            help = "Early = D0vsD6 , Late = D0vsD16"
        )
    with st.sidebar:
        st.image(util.read_png("data/main_logo.png"))

    return {"cell" : select_cellline,"TP" : select_timepoint}