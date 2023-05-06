import streamlit as st
import util
import sidebar
import graphics
from argparse import ArgumentParser


#page config
st.set_page_config(
     page_title='CRISPR screen',
     layout="wide",
     initial_sidebar_state="expanded",
)


#main function
def main():
    sidebar_options = sidebar.app_sidebar()
    app_body(sidebar_options)

    return None

#mainbody displaying data
#takes care of routing sidebar selections
def app_body(sidebar_options):
    match sidebar_options["cell"]:
        case "T98G":
            match sidebar_options["TP"]:
                case "Early":
                    graphics.graphics_main(T98G_early)
                case "Late":
                    graphics.graphics_main(T98G_late)
        case "HEK":
            match sidebar_options["TP"]:
                case "Early":
                    graphics.graphics_main(HEK_early)
                case "Late":
                    graphics.graphics_main(HEK_late)
        case "RPE1":
            match sidebar_options["TP"]:
                case "Early":
                    graphics.graphics_main(RPE1_early)
                case "Late":
                    graphics.graphics_main(RPE1_late)

    return None


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--data", type=str, default=None)
    args = parser.parse_args()
    HEK_early,HEK_late,T98G_early,T98G_late,RPE1_early,RPE1_late = util.load_data(args.data)
    main()