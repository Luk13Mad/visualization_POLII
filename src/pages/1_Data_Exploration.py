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
     initial_sidebar_state = "expanded",
)


#main function
def main_data():
    data_app_body()

#mainbody displaying data
#takes care of routing sidebar selections
def data_app_body():
    sidebar_options = sidebar.app_sidebar()
    match sidebar_options["cell"]:
        case "T98-G":
            match sidebar_options["TP"]:
                case "Early":
                    graphics_data.graphics_main(T98G_early)
                case "Late":
                    graphics_data.graphics_main(T98G_late)
        case "HEK 293T":
            match sidebar_options["TP"]:
                case "Early":
                    graphics_data.graphics_main(HEK_early)
                case "Late":
                    graphics_data.graphics_main(HEK_late)
        case "hTert-RPE1":
            match sidebar_options["TP"]:
                case "Early":
                    graphics_data.graphics_main(RPE1_early)
                case "Late":
                    graphics_data.graphics_main(RPE1_late)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--data", type=str, default="data/Table_data.xlsx")
    args = parser.parse_args()

    HEK_early,HEK_late,T98G_early,T98G_late,RPE1_early,RPE1_late = util.load_data(args.data)
    main_data()
