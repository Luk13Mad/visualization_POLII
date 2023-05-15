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

    tab1,tab2,tab3,tab4,tab5 = st.tabs(["Introduction","Network graph","Raw data","FAQ","Additional graphics"])
    with tab1:
        display_introduction()

    with tab2:
        st.markdown("## Network graph :  \n Constructs containing TTTT control have been excluded for this plot.  \n Node colors represent amount of constructs within dLFC threshold.")
        display_networkgraph(data)

    with tab3:
        st.markdown("## Raw data table :")
        display_dataframe_bargraph(data)

    with tab4:
        display_FAQ()

    with tab5:
        st.image(Image.open("data/puppies.jpg"),caption = "The description will be here, until then enjoy these puppies.")

    st.markdown("***")
    st.markdown("**Impressum:**  \n Links to our host intitutions' data protection statements:  \n [DKFZ](https://www.dkfz.de/de/datenschutzerklaerung.html?m=1668607885&)")

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
    agg_bardata = bardata.melt(
                                id_vars = ["CrRna(A)","CrRNA(B)"],
                                value_vars = ["dLFC(A,B)"]
                            ).groupby(
                                "variable"
                            ).agg({"value" : np.mean}).reset_index()
    agg_bardata["color"] = agg_bardata.loc[:,"value"].apply(lambda x: "sickness" if x <= -0.5 else ("buffering" if x >= 0.5 else "neutral"))

    bar_dLFC = alt.Chart(agg_bardata
                    ).mark_bar().encode(
                            x = alt.X("variable",sort = ["dLFC(A,B)"],title = None),
                            y = alt.Y("value",title = "dLFC"),
                            tooltip = alt.value(None),
                            color = alt.Color("color:N",scale = alt.Scale(
                                                                domain = ["sickness","buffering","neutral"],
                                                                range = ["#ff581a", "#00adff","sand"]),
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

    st.altair_chart(bar_dLFC + scatter_dLFC, use_container_width=True)

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
    
    LFC_selected_cutoff_min,LFC_selected_cutoff_max = st.slider("Cutoff LFC selected gene",min_value = LFC_selected_min - 0.01,
                             max_value = LFC_selected_max + 0.01,
                             value = (LFC_selected_min,LFC_selected_max),
                             step = 0.001,key = "network_slider_selected",
                             help = "LFC range of crRNAs for selected gene. We recommend to exclude highly essential crRNAs from the analysis. ")
    

    LFC_other_min = float(np.nanmin((data.loc[mask_geneA,"LFC(B)"].min(),data.loc[mask_geneB,"LFC(A)"].min())))
    LFC_other_max = float(np.nanmax((data.loc[mask_geneA,"LFC(B)"].max(),data.loc[mask_geneB,"LFC(A)"].max())))
    LFC_other_cutoff_min,LFC_other_cutoff_max = st.slider("Cutoff LFC paired gene",min_value = LFC_other_min - 0.01,
                             max_value = LFC_other_max + 0.01,
                             value = (LFC_other_min,LFC_other_max),
                             step = 0.001,key = "network_slider_other",
                             help = "LFC range of crRNAs for paired gene. We recommend to exclude highly essential crRNAs from the analysis. ")
    
    dLFC_min = float(data.loc[mask_gene,"dLFC(A,B)"].min())
    dLFC_max = float(data.loc[mask_gene,"dLFC(A,B)"].max())
    dLFC_cutoff_min,dLFC_cutoff_max = st.slider("Cutoff dLFC",min_value = dLFC_min - 0.01,
                             max_value = dLFC_max + 0.01,
                             value = (dLFC_min,dLFC_max),
                             step = 0.001,
                             key = "network_slider_dLFC",
                             help = "negative dLFCs = synthetic sickness, positive dLFCs = buffering") 
    
    
    mask_TTTT = data.loc[:,"TTTT control"] == "no"
    mask_cutoff_selected = (data.loc[mask_geneA,"LFC(A)"] >= LFC_selected_cutoff_min) & (data.loc[mask_geneA,"LFC(A)"] <= LFC_selected_cutoff_max) | (data.loc[mask_geneB,"LFC(B)"] >= LFC_selected_cutoff_min) & (data.loc[mask_geneB,"LFC(B)"] <= LFC_selected_cutoff_max)
    mask_cutoff_other = (data.loc[mask_geneA,"LFC(B)"] >= LFC_other_cutoff_min) & (data.loc[mask_geneA,"LFC(B)"] <= LFC_other_cutoff_max) | (data.loc[mask_geneB,"LFC(A)"] >= LFC_other_cutoff_min) & (data.loc[mask_geneB,"LFC(A)"] <= LFC_other_cutoff_max)
    mask_cutoff_dLFC = (data.loc[:,"dLFC(A,B)"] >= dLFC_cutoff_min) & (data.loc[:,"dLFC(A,B)"] <= dLFC_cutoff_max)
    combined_mask = mask_TTTT & mask_cutoff_selected & mask_cutoff_other & mask_cutoff_dLFC & mask_gene

    data = data.loc[combined_mask,["Gene(A)","Gene(B)","dLFC(A,B)"]]
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

    network = nxa.draw_networkx(G=G,pos=pos,node_tooltip = ['name'],
                                node_label = "name",node_color="distance",
                                font_color = "black",font_size = 18)
    

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

def display_FAQ():
    st.write('''
    ## What is a transcription cycle?
    Transcription cycles and cell cycles share many characteristics: They are both organized in uni-directional stages and are both tightly controlled by cyclin dependent kinases (CDKs), just to name a few. Transcription stages are: recruitment &rarr; initiation &rarr; pausing and release &rarr; elongation &rarr; termination &rarr; recycling of components.  \n
    Transcription cycles are frequently dysregulated across human diseases. In cancer, this includes mutations of transcriptional CDKs (e.g., CDK12 or CDK7), an increase of transcription outputs (e.g., upon MYC amplification) or an overall increased dependence of tumors on transcription regulators. More are more inhibitors of transcription enter (pre)clinical trials, creating a strong impetus to understand the underlying determinants and molecular bases of therapeutic activity.

    ## What is a genetic interaction (GI)?
    Phenotypes are frequently not dictated by the status of a single gene alone, but are rather the result of multiple genes interacting with each other. In the context of fitness, genetic interactions come at two different flavors:  \n
    1.	A negative GI or “1 + 1 is > 2”  \n A negative GI refers to situations in which a combination of two genetic events results in a more severe fitness effect than what would be expected given the individual phenotype of each genetic event. A synthetic lethality is the most extreme form of a negative GI. We like the expression “synthetic sickness” better – since this term also includes fitness defects that do not result in the death of a cell.  \n
    2.	A positive GI or “1 + 1 is < 2”  \n A positive GI in refers to situation in which the combined effect of two genetic events results in a fitness higher than what would be expected given each individual phenotype. We like to refer to these situation as “buffering interactions”. 

    ## What are LFCs?
    LFCs are an abbreviation for “log fold changes”. We like to calculate LFCs in order to mathematically quantify fitness trends over time. If between two time-points the abundance of a crRNA is reduced by 50%, we would express this as $log2(0.5) = -1 = LFC$. Therefore: negative LFCs indicate fitness defects, whereas positive LFCs indicate a fitness increase above the baseline.  \n
    The LFC of a specific crRNA "A" (LFC A) or "B" (LFC B) is the mean LFC of all pairs of this crRNA with a non-targeting control. For each gene targeted, there are three different spacers associated with.

    ## How do we calculate expected polygenetic phenotypes? 
    We use an additive model. For digenic phenotypes this is straight-forward:  \n
    $LFC(A,B)_{expected} = LFC(A) + LFC(B)$  \n
    (LFC (A) = LFC of perturbation A, LFC (B) = LFC of perturbation B)  \n
    It’s trickier for interactions between three genes. Here we sum up both the individual LFCs and digenetic interactions to calculate expected LFCs. 

    ## What is a $\Delta$LFC?
    $\Delta$LFCs express both the direction of a GI (positive or negative) and its extent. It is calculated according to the following formula:  \n
    $\Delta LFC =   LFC_{observed}   -   LFC_{expected}$  \n
    Let’s assume a synthetic lethality, in which $LFCA = -0.5$ and $LFCB = -0.7$. The observed $LFC(A,B) = -3$. The $LFC(A,B)_{expected}$  is  $LFC(A) + LFC(B) = -1.2$. The $\Delta LFC = -3 – (-1.2) = -1.8$. The negativity of the $\Delta$LFC indicates a negative GI – or a synthetic sickness. We define a buffering relationship to exhibit a $\Delta LFC > 0$, whereas a $\Delta LFC = 0$ reflects additivity (= no interaction). 


    ## How do you know $LFC_{observed}$? 
    They are based on our combinatorial CRISPR screens and reflect the LFC of targeting two genes in parallel. 

    ## Why do you use Cas13d and not Cas9 or Cas12?
    We believe that Cas13d exhibits several characteristics, which in their combination are unique.  \n
    First, Cas13d targets RNA, not DNA. Therefore, it elicits knockdowns, not knockouts. Knockdowns have been shown by others to be beneficial for genetic interaction screens. We also think that they are resemble what can be expected from treating a patient with molecular drug: Partial target inhibition rather than knockout.  \n
    Second, Cas13d can mobilize crRNA from CRISPR arrays, therefore enables the super-compact encoding of multiple crRNAs – which is ideal for library production and integrity.

    ## Why do you recommend excluding highly essential crRNAs from my analysis?
    If you deliver a death-punch to a cell by efficiently perturbing an essential gene, our $\Delta$LFC formula reaches its limitations. Let’s imagine a situation in which a researcher perturbs two essential genes. To reach the default (or neutral) outcome of additivity ($\Delta$ LFC = 0), the combined effect of perturbing two genes needs to match the sum of both single effects. However, perturbing two essential genes frequently fails to be additive. We like to exaggerate this by saying: “It’s hard for a cell to die twice as fast.” As a consequence, the $\Delta$LFC indicates a positive GI (=a buffering event), which we believe is misleading. We therefore recommend to exclude highly essential crRNAs.

    ## What are TTTT controls?
    We engineered some crRNAs in spot 1 to contain a Polymerase III transcriptional inactivator. Our idea here was to create some super-strong buffering events, which were meant to act as positive controls in our screen. They are biologically meaningless and should therefore be excluded from most analyses. 

    ## Are you planning to extent this atlas? 
    Absolutely! More cell lines, more transcription regulators, more druggable targets – stay tuned!

    ## Are different isoforms listed?
    No, while each guide could in theory target a specific isoform, this was not accounted for. 

    ## Why don’t you calculate gene level interactions instead of crRNA level?
    Cas13d elicits knockdowns, rather than knockouts. We find that many synthetic GIs are only become visible upon a modest gene dosage reduction. Averaging the effect of both strong and modest crRNAs targeting the same gene would mask such scenarios, we therefore decided to not calculate gene-level interactions. 

    ## Why some cell lines have high positive LFC values and others not?
    A positive LFC represents a fitness increase or enrichment of the given crRNA in the population.  For example, loss of a tumor suppressor can enable cells to divide faster. Such crRNAs thus enrich in a screen. We find fitness increases to exhibit a particularly strong context dependence. They occur more frequently seen in immortalized, un-transformed cellular models (such as hTert-RPE1). It’s challenging to make a cancer cell divide even faster! 

    ''')