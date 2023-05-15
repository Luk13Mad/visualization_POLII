import streamlit as st
import util
import sidebar
import graphics_data
import graphics_home
from argparse import ArgumentParser


#page config
st.set_page_config(
     page_title='CRISPR screen',
     layout="wide",
     initial_sidebar_state = "collapsed",
)


#main function
def main():
    home_app_body()

def home_app_body():
    graphics_home.graphics_main()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--data", type=str, default="data/Table_data.xlsx")
    args = parser.parse_args()
    if util.check_password():
        HEK_early,HEK_late,T98G_early,T98G_late,RPE1_early,RPE1_late = util.load_data(args.data)
        main()
