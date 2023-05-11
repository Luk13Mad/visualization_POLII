import streamlit as st

#config sidebar
def app_sidebar():
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

    return {"cell" : select_cellline,"TP" : select_timepoint}