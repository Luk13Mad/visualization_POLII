import streamlit as st
import util
from argparse import ArgumentParser
import graphics_info

def main_info():
    graphics_info.graphics_main()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--data", type=str, default="data/Table_data.xlsx")
    args = parser.parse_args()

    if util.check_password():
        HEK_early,HEK_late,T98G_early,T98G_late,RPE1_early,RPE1_late = util.load_data(args.data)
        main_info()