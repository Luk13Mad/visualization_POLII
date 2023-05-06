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
    df_dict = pd.read_excel(path,sheet_name = None) #"data/Table_S3_Screening_results_AC_03_05_2023.xlsx"
    HEK_early = df_dict["HEK_early"]
    HEK_late = df_dict["HEK_late"]
    T98G_early = df_dict["T98G_early"]
    T98G_late = df_dict["T98G_late"]
    RPE1_early = df_dict["RPE1_early"]
    RPE1_late = df_dict["RPE1_late"]
    del df_dict
    return HEK_early,HEK_late,T98G_early,T98G_late,RPE1_early,RPE1_late