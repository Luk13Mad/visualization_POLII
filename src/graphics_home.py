import streamlit as st
import util


def graphics_main():
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True) #removes top right menu

    
    #st.write(util.svg_helper(),unsafe_allow_html = True)

    st.image(util.read_png("data/main_pic4.png"),width=500)
    
    st.markdown("# **Actionable dependency atlas of dysregulated transcription**")

    st.markdown('''
                    This atlas depicts actionable dependencies that arise from the dysregulation of transcription.  
Aberrant transcription is a hallmark of many diseases such as cancer, ageing or inflammation. It is now becomming druggable through small molecule inhibitors of molecular processes involved in the coordination of gene expression, including bromodomain proteins, splicing regulators and, more recently, transcriptional cyclin dependent kinases (tCDKs). 

                    ''')

    tab1,tab2,tab3,tab4 = st.tabs(["Drugging Transcription","Transcription Cycle","Manual","FAQ"])

    with tab1:
        display_drugging_transcription()

    with tab2:
        display_transcription_cycle()

    with tab3:
        display_manual()

    with tab4:
        display_FAQ()

def display_drugging_transcription():
    st.markdown('''
        ### Dysregulated gene expression is druggable.  
Gene expression dysregulation is a hallmark of most human diseases – including cancer. Transcription is tightly regulated through a concerted action of regulatory factors such as transcriptional cyclin-depending kinases (tCDKs) – many of which are druggable. Many small-molecule inhibitor targeting transcription-associated processes are now evaluated (pre)clinically, but frequently lack biomarkers for patient stratification.

### Unexpected relationships between transcription-related pathways.  
We developed a Cas13 platform for multidimensional gene perturbation by guided RNA cleavage, which enabled the discovery of gene-dosage dependencies and higher-order genetic interaction scenarios. We performed massively parallel GI screens across three cellular models, multiple time-points, and 47,727 pairwise perturbations. The resulting complex interactomes enabled the discovery of unexpected relationships between transcription-related pathway, many of which are druggable.

### Dysregulated gene expression: Fueling oncogenesis, but eliciting actionable dependencies.  
Cancers support oncogenic signaling by altering specific transcription stages – but as a side-effect elicit precise and actionable molecular dependencies. We here provide a detailed atlas of such vulnerabilities, each assigned to distinct stages of dysregulated transcription
        ''')

def display_manual():

    with open("data/manual_video_720p.mp4","rb") as video:
        st.video(video.read())
    st.markdown("The video was partly generated using Servier Medical Art, provided by Servier, licensed under a Creative Commons Attribution 3.0 unported license.")

def display_transcription_cycle():

    st.markdown('''
    Transcription regulation for most protein-coding genes ultimately converges on changes in Pol II activity, which is coordinated through a concerted action of transcriptional CDKs (tCDKs). Mimicking the cell cycle, tCDKs regulate Pol II in a series of mono-directional stages collectively known as the transcription cycle.
    ''')

    with st.expander("Video"):
        with open("data/transcription_cycle_video.mp4","rb") as video:
            st.video(video.read())

def display_FAQ():

    with st.expander("### How can I contact you for suggestions or comments?"):
        st.write('''
    Please refer to the contact information [here](/Contact_Info)
        ''')

    with st.expander("### Is all raw data used for the network graph and bargraph?"):
        st.write('''
    No, the constructs containing TTTT control have been excluded.
        ''')

    with st.expander("### Can I view the source code for this website?"):
        st.write('''
    Sure, it is available on [GitHub](https://github.com/Luk13Mad/visualization_POLII)
        ''')

    with st.expander("### What is a transcription cycle?"):
        st.write('''
    Transcription cycles and cell cycles share many characteristics: They are both organized in uni-directional stages and are both tightly controlled by cyclin dependent kinases (CDKs), just to name a few. Transcription stages are: recruitment &rarr; initiation &rarr; pausing and release &rarr; elongation &rarr; termination &rarr; recycling of components.  \n
    Transcription cycles are frequently dysregulated across human diseases. In cancer, this includes mutations of transcriptional CDKs (e.g., CDK12 or CDK7), an increase of transcription outputs (e.g., upon MYC amplification) or an overall increased dependence of tumors on transcription regulators. More are more inhibitors of transcription enter (pre)clinical trials, creating a strong impetus to understand the underlying determinants and molecular bases of therapeutic activity.
        ''')

    with st.expander("### What is a genetic interaction (GI)?"):
        st.write('''
    Phenotypes are frequently not dictated by the status of a single gene alone, but are rather the result of multiple genes interacting with each other. In the context of fitness, genetic interactions come at two different flavors:  \n
    1.	A negative GI or “1 + 1 is > 2”  \n A negative GI refers to situations in which a combination of two genetic events results in a more severe fitness effect than what would be expected given the individual phenotype of each genetic event. A synthetic lethality is the most extreme form of a negative GI. We like the expression “synthetic sickness” better – since this term also includes fitness defects that do not result in the death of a cell.  \n
    2.	A positive GI or “1 + 1 is < 2”  \n A positive GI in refers to situation in which the combined effect of two genetic events results in a fitness higher than what would be expected given each individual phenotype. We like to refer to these situation as “buffering interactions”. 
        ''')

    with st.expander("### What are LFCs?"):
        st.write('''
    LFCs are an abbreviation for “log fold changes”. We like to calculate LFCs in order to mathematically quantify fitness trends over time. If between two time-points the abundance of a crRNA is reduced by 50%, we would express this as $log2(0.5) = -1 = LFC$. Therefore: negative LFCs indicate fitness defects, whereas positive LFCs indicate a fitness increase above the baseline.  \n
    The LFC of a specific crRNA "A" (LFC A) or "B" (LFC B) is the mean LFC of all pairs of this crRNA with a non-targeting control. For each gene targeted, there are three different spacers associated with.
        ''')

    with st.expander("### How do we calculate expected polygenetic phenotypes? "):
        st.write('''
    We use an additive model. For digenic phenotypes this is straight-forward:  \n
    $LFC(A,B)_{expected} = LFC(A) + LFC(B)$  \n
    (LFC (A) = LFC of perturbation A, LFC (B) = LFC of perturbation B)  \n
    It’s trickier for interactions between three genes. Here we sum up both the individual LFCs and digenetic interactions to calculate expected LFCs. 
        ''')

    with st.expander("### What is a $\Delta$LFC?"):
        st.write('''
    $\Delta$LFCs express both the direction of a GI (positive or negative) and its extent. It is calculated according to the following formula:  \n
    $\Delta LFC =   LFC_{observed}   -   LFC_{expected}$  \n
    Let’s assume a synthetic lethality, in which $LFC(A) = -0.5$ and $LFC(B) = -0.7$. The observed $LFC(A,B) = -3$. The $LFC(A,B)_{expected}$  is  $LFC(A) + LFC(B) = -1.2$. The $\Delta LFC = -3 – (-1.2) = -1.8$. The negativity of the $\Delta$LFC indicates a negative GI – or a synthetic sickness. We define a buffering relationship to exhibit a $\Delta LFC > 0$, whereas a $\Delta LFC = 0$ reflects additivity (= no interaction). 
        ''')

    with st.expander("### How do you know $LFC_{observed}$? "):
        st.write('''
    They are based on our combinatorial CRISPR screens and reflect the LFC of targeting two genes in parallel. 
        ''')

    with st.expander("### Why do you use Cas13d and not Cas9 or Cas12?"):
        st.write('''
    We believe that Cas13d exhibits several characteristics, which in their combination are unique.  \n
    First, Cas13d targets RNA, not DNA. Therefore, it elicits knockdowns, not knockouts. Knockdowns have been shown by others to be beneficial for genetic interaction screens. We also think that they are resemble what can be expected from treating a patient with molecular drug: Partial target inhibition rather than knockout.  \n
    Second, Cas13d can mobilize crRNA from CRISPR arrays, therefore enables the super-compact encoding of multiple crRNAs – which is ideal for library production and integrity.
        ''')

    with st.expander("### Why do you recommend excluding highly essential crRNAs from my analysis?"):
        st.write('''
    If you deliver a death-punch to a cell by efficiently perturbing an essential gene, our $\Delta$LFC formula reaches its limitations. Let’s imagine a situation in which a researcher perturbs two essential genes. To reach the default (or neutral) outcome of additivity ($\Delta$ LFC = 0), the combined effect of perturbing two genes needs to match the sum of both single effects. However, perturbing two essential genes frequently fails to be additive. We like to exaggerate this by saying: “It’s hard for a cell to die twice as fast.” As a consequence, the $\Delta$LFC indicates a positive GI (=a buffering event), which we believe is misleading. We therefore recommend to exclude highly essential crRNAs.
        ''')

    with st.expander("### What are TTTT controls?"):
        st.write('''
    We engineered some crRNAs in spot 1 to contain a Polymerase III transcriptional inactivator. Our idea here was to create some super-strong buffering events, which were meant to act as positive controls in our screen. They are biologically meaningless and should therefore be excluded from most analyses. 
        ''')

    with st.expander("### Are you planning to extend this atlas? "):
        st.write('''
    Absolutely! More cell lines, more transcription regulators, more druggable targets – stay tuned!
        ''')

    with st.expander("### Are different isoforms listed?"):
        st.write('''
     No, while each guide could in theory target a specific isoform, this was not accounted for.
        ''')

    with st.expander("### Why don’t you calculate gene level interactions instead of crRNA level?"):
        st.write('''
    Cas13d elicits knockdowns, rather than knockouts. We find that many synthetic GIs are only become visible upon a modest gene dosage reduction. Averaging the effect of both strong and modest crRNAs targeting the same gene would mask such scenarios, we therefore decided to not calculate gene-level interactions.
        ''')

    with st.expander("### Why some cell lines have high positive LFC values and others not?"):
        st.write('''
    A positive LFC represents a fitness increase or enrichment of the given crRNA in the population.  For example, loss of a tumor suppressor can enable cells to divide faster. Such crRNAs thus enrich in a screen. We find fitness increases to exhibit a particularly strong context dependence. They occur more frequently seen in immortalized, un-transformed cellular models (such as hTert-RPE1). It’s challenging to make a cancer cell divide even faster! 
        ''')

