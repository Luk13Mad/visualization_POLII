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

    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Introduction","Raw data","Network graph","FAQ","Additional graphics"])
    with tab1:
        display_introduction()

    with tab2:
        st.markdown("## Raw data table :")
        display_dataframe_bargraph(data)

    with tab3:
        st.markdown("## Network graph :  \n Constructs containing TTTT control have been excluded for this plot.  \n Node colors represent amount of constructs within dLFC threshold.")
        display_networkgraph(data)

    with tab4:
        st.markdown("## FAQ")
        st.markdown("FAQ will be here.")

    with tab5:
        st.image(Image.open("data/puppies.jpg"),caption = "The description will be here, until then enjoy these puppies.")

    st.markdown("***")
    st.markdown("**Impressum:**  \n Links to our host intitutions' data protection statements:  \n [DKFZ](https://www.dkfz.de/de/datenschutzerklaerung.html?m=1668607885&)")

#display dataframe
#make interaction selection
def display_dataframe_bargraph(data):
    LFC_A_min = float(data.loc[:,"LFC(A)"].min())
    LFC_A_max = float(data.loc[:,"LFC(A)"].max())
    LFC_A_cutoff_min,LFC_A_cutoff_max = st.slider("Cutoff LFC A",min_value = LFC_A_min - 0.01,
                             max_value = LFC_A_max + 0.01,
                             value = (LFC_A_min,LFC_A_max),
                             step = 0.001,
                             help = "LFC range of crRNAs in Spot A. We recommend to exclude highly essential crRNAs from the analysis. ")
    
    LFC_B_min = float(data.loc[:,"LFC(B)"].min())
    LFC_B_max = float(data.loc[:,"LFC(B)"].max())
    LFC_B_cutoff_min,LFC_B_cutoff_max = st.slider("Cutoff LFC B",min_value = LFC_B_min - 0.01,
                             max_value = LFC_B_max + 0.01,
                             value = (LFC_B_min,LFC_B_max),
                             step = 0.001,
                             help = "LFC range of crRNAs in Spot B. We recommend to exclude highly essential crRNAs from the analysis.") 

    dLFC_min = float(data.loc[:,"dLFC(A,B)"].min())
    dLFC_max = float(data.loc[:,"dLFC(A,B)"].max())
    dLFC_cutoff_min,dLFC_cutoff_max = st.slider("Cutoff dLFC",min_value = dLFC_min - 0.01,
                             max_value = dLFC_max + 0.01,
                             value = (dLFC_min,dLFC_max),
                             step = 0.001,
                             help = "negative dLFCs = synthetic sickness, positive dLFCs = buffering") 
    
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
    
    st.markdown("# **Bar graph** :  \n Constructs containing TTTT control have been excluded for this plot.")

    if gene1 != "all genes" and gene2 != "all genes":
        bardata = data.loc[combined_mask,["CrRna(A)","CrRNA(B)","Gene(A)","Gene(B)","LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed","dLFC(A,B)"]]
        display_big_bargraph(bardata)
        display_dLFC_bargraph(bardata)
    else:
        st.markdown("**For performance reasons no bargraph will be plotted if for either spot \"all genes\" are selected.**")



        

def display_big_bargraph(bardata):
    bar = alt.Chart(bardata.melt(
                                id_vars = ["CrRna(A)","CrRNA(B)"],
                                value_vars = ["LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed"]
                            ).groupby(
                                "variable"
                            ).agg({"value" : np.mean}).reset_index()
                    ).mark_bar().encode(
                            x = alt.X("variable",sort = ["LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed"],title = None),
                            y = alt.Y("value",title = "LFC"),
                            tooltip = alt.value(None),
                            color = alt.Color("variable",
                                              scale = alt.Scale(domain=["LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed"],
                                                                range=['blue', 'grey','green','red'])))
    
    scatter = alt.Chart(bardata.melt(
                                id_vars = ["CrRna(A)","CrRNA(B)"],
                                value_vars = ["LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed"]
                            )
                    ).mark_circle(size = 30,color = "black").encode(
                        x = alt.X("variable",sort = ["LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed"],title = None),
                        y = alt.Y("value",title = "LFC"),
                        tooltip = ["value","CrRna(A)","CrRNA(B)"],
                    )

    st.altair_chart(bar + scatter, use_container_width=True)


def display_dLFC_bargraph(bardata):
    #for color transform just add column to bardata

    agg_bardata = bardata.melt(
                                id_vars = ["CrRna(A)","CrRNA(B)"],
                                value_vars = ["dLFC(A,B)"]
                            ).groupby(
                                "variable"
                            ).agg({"value" : np.mean}).reset_index()
    agg_bardata["color"] = agg_bardata.loc[:,"value"].apply(lambda x: "red" if x <= -0.5 else ("blue" if x >= 0.5 else "grey"))

    bar_dLFC = alt.Chart(agg_bardata
                    ).mark_bar().encode(
                            x = alt.X("variable",sort = ["dLFC(A,B)"],title = None),
                            y = alt.Y("value",title = "LFC"),
                            tooltip = alt.value(None),
                            color = alt.Color("color:N",scale = None))
    
    scatter_dLFC = alt.Chart(bardata.melt(
                                id_vars = ["CrRna(A)","CrRNA(B)"],
                                value_vars = ["dLFC(A,B)"]
                            )
                    ).mark_circle(size = 30,color = "black").encode(
                        x = alt.X("variable",sort = ["dLFC(A,B)"],title = None),
                        y = alt.Y("value",title = "LFC"),
                        tooltip = ["value","CrRna(A)","CrRNA(B)"],
                    )

    st.altair_chart(bar_dLFC + scatter_dLFC, use_container_width=True)

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
        
    springload_dict = dict()
    for (s,t,v) in G.edges(data = True):
        springload_dict.update({(s,t):{"springload":(1/v["weight"])}})
    nx.set_edge_attributes(G,springload_dict)


    pos = nx.spring_layout(G,weight = "springload")
    node_labels = {n: n for n in G.nodes()}
    nx.set_node_attributes(G,node_labels,"name")

    node_distance = {gene:0}
    for (s,t,v) in G.edges(data=True):
        if s == gene:
            node_distance.update({t:v["weight"]})
        else:
            node_distance.update({s:v["weight"]})
    nx.set_node_attributes(G,node_distance,"distance")

    network = nxa.draw_networkx(G=G,pos=pos,node_tooltip = ['name'],node_label = "name",node_color="distance",font_color = "black",font_size = 18)
    

    st.markdown(f"Number of nodes: n = {G.number_of_nodes()}")
    st.altair_chart(network, use_container_width=True)

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