import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import networkx as nx
import util

#main graphics function
#handle layout here
def graphics_main(data):
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)#removes top right menu

    tab1,tab2 = st.tabs(["Network graph","Raw data"])
    
    with tab1:
        display_networkgraph(data)

    with tab2:
        display_dataframe_bargraph(data)

#display dataframe
#make interaction selection
def display_dataframe_bargraph(data):
    unique_genes_A = ["all genes"] + list(data.loc[:,"Gene(A)"].sort_values().unique())
    gene1 = st.selectbox(
        'Gene in spot A',
        unique_genes_A)

    unique_genes_B = ["all genes"] + list(data.loc[:,"Gene(B)"].sort_values().unique())
    gene2 = st.selectbox(
        'Gene in spot B',
        unique_genes_B)
    

    LFC_A_min = float(data.loc[:,"LFC(A)"].min())
    LFC_A_max = float(data.loc[:,"LFC(A)"].max())
    LFC_A_cutoff_min,LFC_A_cutoff_max = st.slider("Cutoff LFC A",min_value = LFC_A_min - 0.01,
                             max_value = LFC_A_max + 0.01,
                             value = (LFC_A_min,LFC_A_max),
                             step = 0.001,
                             help = "LFC range of crRNAs in Spot A. We recommend to exclude highly essential crRNAs (large negative values) from the analysis. ")
    
    LFC_B_min = float(data.loc[:,"LFC(B)"].min())
    LFC_B_max = float(data.loc[:,"LFC(B)"].max())
    LFC_B_cutoff_min,LFC_B_cutoff_max = st.slider("Cutoff LFC B",min_value = LFC_B_min - 0.01,
                             max_value = LFC_B_max + 0.01,
                             value = (LFC_B_min,LFC_B_max),
                             step = 0.001,
                             help = "LFC range of crRNAs in Spot B. We recommend to exclude highly essential crRNAs (large negative values) from the analysis.") 

    dLFC_min = float(data.loc[:,"dLFC(A,B)"].min())
    dLFC_max = float(data.loc[:,"dLFC(A,B)"].max())
    dLFC_cutoff_min,dLFC_cutoff_max = st.slider("Cutoff dLFC",min_value = dLFC_min - 0.01,
                             max_value = dLFC_max + 0.01,
                             value = (dLFC_min,dLFC_max),
                             step = 0.001,
                             key = "dLFC1",
                             help = "negative dLFCs = synthetic sickness, positive dLFCs = buffering") 
    
    TTTT = st.checkbox('TTTT control',help = "If selected removes constructs with TTTT control.")

    
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
    if data.loc[combined_mask,:].empty:
        st.markdown("**Not all genes appear in all combinations, pick a different combination.**")
    else:
        st.dataframe(data.loc[combined_mask,["CrRna(A)","CrRNA(B)","Gene(A)","Gene(B)",
                                         "LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed","dLFC(A,B)"]].sort_values(["Gene(A)","Gene(B)"]).reset_index(drop=True))
    
    st.markdown("# **Bar graph** :")

    if gene1 != "all genes" and gene2 != "all genes":
        bardata = data.loc[combined_mask,["CrRna(A)","CrRNA(B)","Gene(A)","Gene(B)","LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed","dLFC(A,B)"]]
        display_big_bargraph(bardata)
        display_dLFC_bargraph(bardata)
    else:
        st.markdown("**For performance reasons no bargraph will be plotted if for either spot all genes are selected.**")
        

def display_big_bargraph(bardata):
    bar = alt.Chart(bardata.melt(
                                id_vars = ["CrRna(A)","CrRNA(B)"],
                                value_vars = ["LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed"]
                            ).groupby(
                                "variable"
                            ).agg({"value" : np.mean}).reset_index()
                    ).mark_bar(size=40).encode(
                            x = alt.X("variable",sort = ["LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed"],title = None,axis=alt.Axis(labelAngle=0)),
                            y = alt.Y("value",title = "LFC"),
                            tooltip = alt.value(None),
                            color = alt.Color("variable",
                                              scale = alt.Scale(domain=["LFC(A)","LFC(B)","LFC(A,B)_expected","LFC(A,B)_observed"],
                                                                range=['blue', 'grey','green','red']),
                                             title = "LFC(.)"))
    
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
    agg_bardata = bardata.melt(id_vars = ["CrRna(A)","CrRNA(B)"],
                                value_vars = ["dLFC(A,B)"]).groupby("variable").agg({"value" : np.mean}).reset_index()
    agg_bardata["color"] = agg_bardata.loc[:,"value"].apply(lambda x: "sickness" if x <= -0.5 else ("buffering" if x >= 0.5 else "neutral"))

    bar_dLFC = alt.Chart(agg_bardata).mark_bar(size=40).encode(
                            x = alt.X("variable",title = None,axis=alt.Axis(labelAngle=0)),
                            y = alt.Y("value",title = "dLFC"),
                            tooltip = alt.value(None),
                            color = alt.Color("color:N",scale = alt.Scale(
                                                                domain = ["sickness","buffering","neutral"],
                                                                range = ["#ff581a", "#00adff","#ffd78f"]),
                                                title = "Effect"))
    
    scatter_dLFC = alt.Chart(bardata.melt(
                                id_vars = ["CrRna(A)","CrRNA(B)"],
                                value_vars = ["dLFC(A,B)"]
                            )
                    ).mark_circle(size = 30,color = "black").encode(
                        x = alt.X("variable",sort = ["dLFC(A,B)"],title = None),
                        y = alt.Y("value",title = "dLFC"),
                        tooltip = ["value","CrRna(A)","CrRNA(B)"],
                    )

    st.altair_chart(bar_dLFC  + scatter_dLFC, use_container_width=True)

def display_networkgraph(data):
    unique_genes = np.unique(data.loc[:,["Gene(A)","Gene(B)"]].values.ravel())
    gene = st.selectbox(
        'Gene to display interactions for',
        unique_genes)
    
    mask_geneA = data.loc[:,"Gene(A)"] == gene
    mask_geneB = data.loc[:,"Gene(B)"] == gene
    mask_gene = (mask_geneA | mask_geneB)

    LFC_selected_min = float(np.nanmin((data.loc[mask_geneA,"LFC(A)"].min(),data.loc[mask_geneB,"LFC(B)"].min())))
    LFC_selected_max = float(np.nanmax((data.loc[mask_geneA,"LFC(A)"].max(),data.loc[mask_geneB,"LFC(B)"].max())))
    
    LFC_selected_cutoff_min,LFC_selected_cutoff_max = st.slider("LFC range of single guides targeting the gene above",min_value = LFC_selected_min - 0.01,
                             max_value = LFC_selected_max + 0.01,
                             value = (LFC_selected_min,LFC_selected_max),
                             step = 0.001,key = "network_slider_selected",
                             help = "LFC range of crRNAs for selected gene. We recommend to exclude highly essential crRNAs (large negative values) from the analysis. ")
    
    st.write("#")

    LFC_other_min = float(np.nanmin((data.loc[mask_geneA,"LFC(B)"].min(),data.loc[mask_geneB,"LFC(A)"].min())))
    LFC_other_max = float(np.nanmax((data.loc[mask_geneA,"LFC(B)"].max(),data.loc[mask_geneB,"LFC(A)"].max())))
    LFC_other_cutoff_min,LFC_other_cutoff_max = st.slider("LFC range of single guides targeting the second gene",min_value = LFC_other_min - 0.01,
                             max_value = LFC_other_max + 0.01,
                             value = (LFC_other_min,LFC_other_max),
                             step = 0.001,key = "network_slider_other",
                             help = "LFC range of crRNAs for paired gene. We recommend to exclude highly essential crRNAs (large negative values) from the analysis. ")
    
    dLFC_min = float(data.loc[mask_gene,"dLFC(A,B)"].min())
    dLFC_max = float(data.loc[mask_gene,"dLFC(A,B)"].max())
    dLFC_cutoff_min,dLFC_cutoff_max = st.slider("Cutoff dLFC (more negative &rarr; stronger synthetic sickness)",min_value = dLFC_min - 0.01,
                             max_value = dLFC_max + 0.01,
                             value = (dLFC_min,dLFC_max),
                             step = 0.001,
                             key = "network_slider_dLFC",
                             help = "negative dLFCs = synthetic sickness, positive dLFCs = buffering") 
    
    mask_TTTT = data.loc[:,"TTTT control"] == "no"
    combined_mask = mask_TTTT & mask_gene
    data = data.loc[combined_mask,["Gene(A)","Gene(B)","LFC(A)","LFC(B)","dLFC(A,B)"]] #filter only for the relevant pairs

    #filter only for selected gene
    mask_cutoff_selected = ((data.loc[:,"LFC(A)"] >= LFC_selected_cutoff_min) & (data.loc[:,"LFC(A)"] <= LFC_selected_cutoff_max) & (data.loc[:,"Gene(A)"] == gene)) | ((data.loc[:,"LFC(B)"] >= LFC_selected_cutoff_min) & (data.loc[:,"LFC(B)"] <= LFC_selected_cutoff_max) & (data.loc[:,"Gene(B)"] == gene))
    data = data.loc[mask_cutoff_selected,["Gene(A)","Gene(B)","LFC(A)","LFC(B)","dLFC(A,B)"]]

    mask_cutoff_other = ((data.loc[:,"LFC(B)"] >= LFC_other_cutoff_min) & (data.loc[:,"LFC(B)"] <= LFC_other_cutoff_max) & (data.loc[:,"Gene(A)"] == gene)) | ((data.loc[:,"LFC(A)"] >= LFC_other_cutoff_min) & (data.loc[:,"LFC(A)"] <= LFC_other_cutoff_max) & (data.loc[:,"Gene(B)"] == gene))
    data = data.loc[mask_cutoff_other,["Gene(A)","Gene(B)","LFC(A)","LFC(B)","dLFC(A,B)"]]

    mask_cutoff_dLFC = (data.loc[:,"dLFC(A,B)"] >= dLFC_cutoff_min) & (data.loc[:,"dLFC(A,B)"] <= dLFC_cutoff_max)
    data = data.loc[mask_cutoff_dLFC,["Gene(A)","Gene(B)","LFC(A)","LFC(B)","dLFC(A,B)"]]
    
    edgelist = util.aggregate_df_to_edgelist(df = data, maingene = gene)

    # Generate graph
    G = nx.Graph()
    if len(edgelist) == 0:
        G.add_weighted_edges_from([(gene,gene,0)])
    else:
        G.add_weighted_edges_from(edgelist)
        
    springload_dict = dict()
    for (s,t,v) in G.edges(data = True):
        try:
            springload_dict.update({(s,t):{"springload":(1/v["weight"])}})
        except:
            springload_dict.update({(s,t):{"springload":0}})
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

    st.markdown(f"Number of nodes: n = {G.number_of_nodes()}")
    draw_network(graph = G,position = pos,central_gene = gene)

def draw_network(graph,position,central_gene):
    '''custom draw network function'''
    edges = draw_edges(position,central_gene)
    nodes = draw_nodes(graph,position)
    labels = draw_labels(position)

    network_graph = edges + nodes +labels
    st.altair_chart(network_graph, use_container_width=True)

def draw_labels(position):
    '''draw gene names over nodes'''
    x,y,label = [],[],[]
    for k,v in position.items():
        x.append(v[0])
        y.append(v[1])
        label.append(k)

    data = pd.DataFrame({"x":x,"y":y,"label":label})

    label_chart = alt.Chart(data).mark_text(fontStyle = "bold").encode(
        x=alt.X('x', axis=alt.Axis(title='', grid=False, labels=False, ticks=False)),
        y=alt.Y('y', axis=alt.Axis(title='', grid=False, labels=False, ticks=False)),
        text = "label",
        tooltip = ["label"])

    return label_chart

def draw_nodes(graph,position):
    '''draw nodes with color'''
    node_dict = graph.nodes()
    x,y,amount = [],[],[]
    for k,v in position.items():
        x.append(v[0])
        y.append(v[1])
        amount.append(node_dict[k]["distance"])

    data = pd.DataFrame({"x":x,"y":y,"amount":amount})

    node_chart = alt.Chart(data).mark_point().encode(
        x=alt.X('x', axis=alt.Axis(title='', grid=False, labels=False, ticks=False)),
        y=alt.Y('y', axis=alt.Axis(title='', grid=False, labels=False, ticks=False)),
        color = alt.Color("amount:O",scale = alt.Scale(domain = [x for x in range(0,data.amount.max()+1,1)],
                                                   scheme = "category10",type = "identity"),
                                                   title = "# supporting crRNA pairs"),
        size = alt.value(300),
        fill = alt.Color("amount:O",scale = alt.Scale(domain = [x for x in range(0,data.amount.max()+1,1)],
                                                   scheme = "category10",type = "identity"),
                                                   title = "# supporting crRNA pairs"),
        opacity = alt.value(1),
        tooltip = alt.value(None))

    return node_chart

def draw_edges(position,central_gene):
    '''draw edges in background of network graph'''

    x,y,x2,y2 = [],[],[],[]
    for k,v in position.items():
        if k != central_gene:
            x.append(position[central_gene][0])
            y.append(position[central_gene][1])
            x2.append(v[0])
            y2.append(v[1])
    data = pd.DataFrame({"x":x,"y":y,"x2":x2,"y2":y2})

    edge_chart = alt.Chart(data).mark_rule().encode(
        x=alt.X('x', axis=alt.Axis(title='', grid=False, labels=False, ticks=False)),
        y=alt.Y('y', axis=alt.Axis(title='', grid=False, labels=False, ticks=False)),
        x2 = "x2",
        y2 = "y2",
        color = alt.value("grey"),
        tooltip = alt.value(None))
    
    return edge_chart