import pandas as pd
import streamlit as st
import os

#function loading data
@st.cache_data
def load_data(path):
    if not os.path.isfile(path):
        raise ValueError("Could not find file. Try giving absolute path.")
    if not path.endswith(".xlsx"):
        raise ValueError("Must be excel file, ending with .xlsx")
    df_dict = pd.read_excel(path,sheet_name = None)
    HEK_early = df_dict["HEK_early"]
    HEK_late = df_dict["HEK_late"]
    T98G_early = df_dict["T98G_early"]
    T98G_late = df_dict["T98G_late"]
    RPE1_early = df_dict["RPE1_early"]
    RPE1_late = df_dict["RPE1_late"]
    del df_dict
    return HEK_early,HEK_late,T98G_early,T98G_late,RPE1_early,RPE1_late

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True