import streamlit as st
import altair as alt
from PIL import Image
import numpy as np
import networkx as nx
import nx_altair as nxa
import util

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
    st.markdown("# **Network graph** :  \n Constructs containing TTTT control have been excluded for this plot.  \n Edges represent amount of constructs within dLFC threshold.")
    display_networkgraph(data)

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

    dLFC_min = float(data.loc[:,"dLFC(A,B)"].min())
    dLFC_max = float(data.loc[:,"dLFC(A,B)"].max())
    dLFC_cutoff_min,dLFC_cutoff_max = st.slider("Cutoff dLFC",min_value = dLFC_min - 0.01,
                             max_value = dLFC_max + 0.01,
                             value = (dLFC_min,dLFC_max),
                             step = 0.001) 
    
    TTTT = st.checkbox('TTTT control',help = "If selected removes constructs with TTTT control.")


    unique_genes_A = ["all genes"] + list(data.loc[:,"Gene(A)"].sort_values().unique())
    gene1 = st.selectbox(
        'Gene in spot A',
        unique_genes_A)

    unique_genes_B = ["all genes"] + list(data.loc[data.loc[:,"Gene(A)"] == gene1,"Gene(B)"].sort_values().unique())
    gene2 = st.selectbox(
        'Gene in spot B',
        unique_genes_B)

    
    mask_cutoff_A = (data.loc[:,"LFC(A)"] >= LFC_A_cutoff_min) & (data.loc[:,"LFC(A)"] <= LFC_A_cutoff_max)
    mask_cutoff_B = (data.loc[:,"LFC(B)"] >= LFC_B_cutoff_min) & (data.loc[:,"LFC(B)"] <= LFC_B_cutoff_max)
    mask_cutoff_dLFC = (data.loc[:,"dLFC(A,B)"] >= dLFC_cutoff_min) & (data.loc[:,"dLFC(A,B)"] <= dLFC_cutoff_max)
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

    combined_mask = mask_cutoff_A & mask_cutoff_B & mask_TTTT & mask_geneA & mask_geneB & mask_cutoff_dLFC
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


def display_networkgraph(data):
    unique_genes = np.unique(data.loc[:,["Gene(A)","Gene(B)"]].values.ravel())
    gene = st.selectbox(
        'Gene to display interactions for',
        unique_genes)
    
    LFC_A_min = float(data.loc[:,"LFC(A)"].min())
    LFC_A_max = float(data.loc[:,"LFC(A)"].max())
    LFC_A_cutoff_min,LFC_A_cutoff_max = st.slider("Cutoff LFC A",min_value = LFC_A_min - 0.01,
                             max_value = LFC_A_max + 0.01,
                             value = (LFC_A_min,LFC_A_max),
                             step = 0.001,key = "network_slider_A")
    
    LFC_B_min = float(data.loc[:,"LFC(B)"].min())
    LFC_B_max = float(data.loc[:,"LFC(B)"].max())
    LFC_B_cutoff_min,LFC_B_cutoff_max = st.slider("Cutoff LFC B",min_value = LFC_B_min - 0.01,
                             max_value = LFC_B_max + 0.01,
                             value = (LFC_B_min,LFC_B_max),
                             step = 0.001,key = "network_slider_B")
    dLFC_min = float(data.loc[:,"dLFC(A,B)"].min())
    dLFC_max = float(data.loc[:,"dLFC(A,B)"].max())
    dLFC_cutoff_min,dLFC_cutoff_max = st.slider("Cutoff dLFC",min_value = dLFC_min - 0.01,
                             max_value = dLFC_max + 0.01,
                             value = (dLFC_min,dLFC_max),
                             step = 0.001,
                             key = "network_slider_dLFC") 
    
    mask_geneA = data.loc[:,"Gene(A)"] == gene
    mask_geneB = data.loc[:,"Gene(B)"] == gene
    mask_TTTT = data.loc[:,"TTTT control"] == "no"
    mask_cutoff_A = (data.loc[:,"LFC(A)"] >= LFC_A_cutoff_min) & (data.loc[:,"LFC(A)"] <= LFC_A_cutoff_max)
    mask_cutoff_B = (data.loc[:,"LFC(B)"] >= LFC_B_cutoff_min) & (data.loc[:,"LFC(B)"] <= LFC_B_cutoff_max)
    mask_cutoff_dLFC = (data.loc[:,"dLFC(A,B)"] >= dLFC_cutoff_min) & (data.loc[:,"dLFC(A,B)"] <= dLFC_cutoff_max)
    combined_mask = mask_TTTT & mask_cutoff_A & mask_cutoff_B & mask_cutoff_dLFC & (mask_geneA | mask_geneB)

    data = data.loc[combined_mask,["Gene(A)","Gene(B)","dLFC(A,B)"]]
    edgelist = util.aggregate_df_to_edgelist(df = data, maingene = gene)

    # Generate a random graph
    G = nx.Graph()
    if len(edgelist) == 0:
        G.add_weighted_edges_from([(gene,gene,0)])
    else:
        G.add_weighted_edges_from(edgelist)


    pos = nx.spring_layout(G)
    node_labels = {n: n for n in G.nodes()}
    nx.set_node_attributes(G,node_labels,"name")

    network = nxa.draw_networkx(G=G,pos=pos,node_tooltip = ['name'],node_label = "name")#,node_color="distance"

    st.markdown(f"Number of nodes: n = {G.number_of_nodes()}")
    st.altair_chart(network, use_container_width=True)

