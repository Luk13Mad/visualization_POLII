import streamlit as st


def graphics_main():
    st.markdown("# **Imbalanced Pol II transcription cycles elicit global and stage-specific collateral liabilities**")
    st.markdown("Welcome to the homepage.  \n TODO CITATION")

    tab1,tab2 = st.tabs(["Introduction","FAQ"])

    with tab1:
        display_introduction()

    with tab2:
        st.text("placeholder")


    st.markdown("***")
    st.markdown("**Impressum:**  \n Links to our host intitutions' data protection statements:  \n [DKFZ](https://www.dkfz.de/de/datenschutzerklaerung.html?m=1668607885&)")


def display_introduction():
    st.markdown('''
    ## Actionable dependency atlas of dysregulated transcription  \n
    ''')

    with open("data/introduction_video.mp4","rb") as video:
        st.video(video.read())


    st.markdown('''
    ## Dysregulated gene expression is druggable.  \n
    Gene expression dysregulation is a hallmark of most human diseases – including cancer. Transcription is tightly regulated through a concerted action of regulatory factors such as transcriptional cyclin-depending kinases (tCDKs) – many of which are druggable. Many small-molecule inhibitor targeting transcription-associated processes are now evaluated (pre)clinically, but frequently lack biomarkers for patient stratitication. 

    ## Unexpected relationships between transcription-related pathways.  \n
    We developed a Cas13 platform for multidimensional gene perturbation by guided RNA cleavage, which enabled the discovery of gene-dosage dependencies and higher-order genetic interaction scenarios. We performed massively parallel GI screens across three cellular models, multiple time-points, and 47,727 pairwise perturbations. The resulting complex interactomes enabled the discovery of unexpected relationships between transcription-related pathway, many of which are druggable. 

    ## Dysregulated gene expression: Fueling oncogenesis, but eliciting actionable dependencies.  \n
    Cancers support oncogenic signaling by altering specific transcription stages – but as a side-effect elicit precise and actionable molecular dependencies. We here provide a detailed atlas of such vulnerabilities, each assigned to distinct stages of dysregulated transcription.
    ''')