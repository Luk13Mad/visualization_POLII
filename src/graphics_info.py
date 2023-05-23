import streamlit as st

def graphics_main():
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)#removes top right menu

    st.markdown("## **Contact Information**")

    st.markdown('''
    **Braun Lab**:  \n
PI: Christian Braun  \n
Max-Eder Research Group  \n
Department of Pediatrics, Dr. von Hauner Children’s Hospital  \n
University Hospital, LMU Munich  \n
Lindwurmstraße 4, 80337 Munich, Germany  \n
Tel.: ++49-89-4400-54729  \n
[Braun lab website](https://www.ccrc-hauner.de/braun-lab/48534a730dc8e62f)  \n
   
Website and interactive graphics by Lukas Madenach.
''')


    st.markdown("***")
    st.markdown("**Impressum:**  \n Links to our host intitutions' data protection statements:  \n [Klinikum LMU](https://www.lmu-klinikum.de/datenschutzerklarung/47827f3d01345fe0) | [Helmholtz München](https://www.helmholtz-munich.de/datenschutz) | [DKFZ](https://www.dkfz.de/de/datenschutzerklaerung.html?m=1668607885&)")
