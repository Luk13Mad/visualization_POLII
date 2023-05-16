import pandas as pd
import streamlit as st
import os
import base64

#function loading data
@st.cache_data
def load_data(path):
    if not os.path.isfile(path):
        raise ValueError("Could not find file. Try giving absolute path.")
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
        if st.session_state["password"].lower() == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password (senior authors last name)", type="password", on_change=password_entered, key="password"
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
    
def aggregate_df_to_edgelist(df : pd.DataFrame,maingene = str,source = "Gene(A)", target = "Gene(B)", edge_attr = "dLFC(A,B)",aggfun = len):
    edgedict = {}
    for _,row in df.iterrows():
        if row[source] == maingene:
            if row[target] in edgedict:
                edgedict[row[target]].append(row[edge_attr])
            else:
                edgedict.update({row[target]:[row[edge_attr]]})
        elif row[target] == maingene:
            if row[source] in edgedict:
                edgedict[row[source]].append(row[edge_attr])
            else:
                edgedict.update({row[source]:[row[edge_attr]]})
        else:
            raise ValueError
        
    edgelist = []
    for k in edgedict.keys():
        edgelist.append((maingene,k,aggfun(edgedict[k])))

    return edgelist



#code to allow image with link from https://discuss.streamlit.io/t/href-on-image/9693/4
@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache_data
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
                <img width="200" height="200" src="data:image/{img_format};base64,{bin_str}" />
        </a>'''
    return html_code