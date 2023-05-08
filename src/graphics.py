import streamlit as st
import altair as alt
from PIL import Image
import numpy as np

#main graphics function
#handle layout here
def graphics_main(data):
    st.markdown("# **Imbalanced Pol II transcription cycles elicit global and stage-specific collateral liabilities**")
    st.markdown("Visualization for the supplementary data and additional graphics.  \n Based on :  \n TODO CITATION")
    st.markdown("***")
    st.markdown("# **Raw data table** :")
    display_dataframe(data)

    st.markdown("***")
    st.markdown("# **Bar graph** :  \n Constructs containing TTTT control have been excluded for this plot.")
    display_bargraph(data)

    st.markdown("***")
    st.markdown("# **Additional graphics** :")
    st.image(Image.open("data/puppies.jpg"),caption = "The description will be here, until then enjoy these puppies.")

#display dataframe
#make interaction selection
def display_dataframe(data):
    LFC_A_min = float(data.loc[:,"LFC(A)"].min())
    LFC_A_max = float(data.loc[:,"LFC(A)"].max())
    LFC_A_cutoff_min,LFC_A_cutoff_max = st.slider("Cutoff LFC A",min_value = LFC_A_min - 0.01,
                             max_value = LFC_A_max + 0.01,
                             value = (LFC_A_min,LFC_A_max),
                             step = 0.001)
    
    LFC_B_min = float(data.loc[:,"LFC(B)"].min())
    LFC_B_max = float(data.loc[:,"LFC(B)"].max())
    LFC_B_cutoff_min,LFC_B_cutoff_max = st.slider("Cutoff LFC B",min_value = LFC_B_min - 0.01,
                             max_value = LFC_B_max + 0.01,
                             value = (LFC_B_min,LFC_B_max),
                             step = 0.001)
    
    TTTT = st.checkbox('TTTT control',help = "If selected removes constructs with TTTT control.")


    unique_genes_A = ["all genes"] + list(data.loc[:,"Gene(A)"].unique())
    gene1 = st.selectbox(
        'Gene in spot A',
        unique_genes_A)

    unique_genes_B = ["all genes"] + list(data.loc[data.loc[:,"Gene(A)"] == gene1,"Gene(B)"].unique())
    gene2 = st.selectbox(
        'Gene in spot B',
        unique_genes_B)

    
    mask_cutoff_A = (data.loc[:,"LFC(A)"] >= LFC_A_cutoff_min) & (data.loc[:,"LFC(A)"] <= LFC_A_cutoff_max)
    mask_cutoff_B = (data.loc[:,"LFC(B)"] >= LFC_B_cutoff_min) & (data.loc[:,"LFC(B)"] <= LFC_B_cutoff_max)
    if TTTT:
        mask_TTTT = data.loc[:,"TTTT control"] == "no"
    else:
        mask_TTTT = True

    if gene1 == "all genes":
        mask_geneA = True
    else:
        mask_geneA = data.loc[:,"Gene(A)"] == gene1

    if gene2 == "all genes":
        mask_geneB = True
    else:
        mask_geneB = data.loc[:,"Gene(B)"] == gene2

    combined_mask = mask_cutoff_A & mask_cutoff_B & mask_TTTT & mask_geneA & mask_geneB
    st.dataframe(data.loc[combined_mask,["CrRna(A)","CrRNA(B)","Gene(A)","Gene(B)",
                                         "LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed","dLFC(A,B)"]].sort_values(["Gene(A)","Gene(B)"]).reset_index(drop=True))


#display bar chart of selected gene pair
def display_bargraph(data):
    unique_genes_A = data.loc[:,"Gene(A)"].unique()
    gene1 = st.selectbox(
        'Gene in spot A',
        unique_genes_A)

    unique_genes_B = data.loc[data.loc[:,"Gene(A)"] == gene1,"Gene(B)"].unique()
    gene2 = st.selectbox(
        'Gene in spot B',
        unique_genes_B)
    
    mask_geneA = data.loc[:,"Gene(A)"] == gene1
    mask_geneB = data.loc[:,"Gene(B)"] == gene2
    mask_TTTT = data.loc[:,"TTTT control"] == "no"
    combined_mask = mask_TTTT & mask_geneA & mask_geneB

    data = data.loc[combined_mask,["CrRna(A)","CrRNA(B)","Gene(A)","Gene(B)","LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed","dLFC(A,B)"]]

    bar = alt.Chart(data.melt(
                                id_vars = ["CrRna(A)","CrRNA(B)"],
                                value_vars = ["LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed","dLFC(A,B)"]
                            ).groupby(
                                "variable"
                            ).agg({"value" : np.mean}).reset_index()
                    ).mark_bar(color = "orange").encode(
                            x = alt.X("variable",sort = ["LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed","dLFC(A,B)"],title = None),
                            y = alt.Y("value",title = "LFC"),
                            tooltip = alt.value(None))
    
    scatter = alt.Chart(data.melt(
                                id_vars = ["CrRna(A)","CrRNA(B)"],
                                value_vars = ["LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed","dLFC(A,B)"]
                            )
                    ).mark_circle(size = 30,color = "red").encode(
                        x = alt.X("variable",sort = ["LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed","dLFC(A,B)"],title = None),
                        y = alt.Y("value",title = "LFC"),
                        tooltip = ["value","CrRna(A)","CrRNA(B)"],
                    )

    st.altair_chart(bar + scatter, use_container_width=True)
