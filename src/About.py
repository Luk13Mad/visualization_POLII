import streamlit as st
import util
import graphics_home
from argparse import ArgumentParser


#page config
st.set_page_config(
     page_title='CRISPR screen',
     layout="wide",
     initial_sidebar_state = "expanded",
)


#main function
def main_homepage():
    home_app_body()

def home_app_body():
    with st.sidebar:
        st.image(util.read_png("data/main_logo.png"))
    graphics_home.graphics_main()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--data", type=str, default="data/Table_data.xlsx")
    args = parser.parse_args()
    if util.check_password():
        HEK_early,HEK_late,T98G_early,T98G_late,RPE1_early,RPE1_late = util.load_data(args.data)
        main_homepage()
