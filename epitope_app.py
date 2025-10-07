import streamlit as st
import requests
import py3Dmol
import streamlit.components.v1 as components
from Bio import SeqIO
from io import StringIO

# ------------------ PAGE CONFIG -------------------
st.set_page_config(page_title="Epitope Binding App", layout="wide")
st.title("🧬 Epitope Binding App")
st.markdown("### Predict epitopes, highlight regions, identify diseases, and visualize 3D structures")

# ------------------ INPUT -------------------
sequence = st.text_area("🔹 Paste Protein Sequence (FASTA or plain):", height=200)

# ------------------ EPITOPE PREDICTION -------------------
if st.button("🔍 Predict Epitope"):
    if not sequence:
        st.warning("Please enter a valid protein sequence.")
    else:
        # --- Clean sequence ---
        if sequence.startswith(">"):
            record = SeqIO.read(StringIO(sequence), "fasta")
            seq = str(record.seq)
        else:
            seq = sequence.replace("\n", "").strip()

        # --- Simple mock epitope prediction ---
        epitopes = [seq[i:i+9] for i in range(0, len(seq) - 9, 10)]
        st.session_state['epitopes'] = epitopes
        st.session_state['sequence'] = seq

        # ------------------ Disease Prediction -------------------
        disease = "Unknown Disease"
        if "GPGRA" in seq:
            disease = "HIV infection (gp120 epitope)"
        elif "RGD" in seq:
            disease = "Cancer metastasis (Integrin-binding motif)"
        elif "EPIY" in seq:
            disease = "Helicobacter pylori infection (CagA epitope)"
        elif "NANP" in seq:
            disease = "Malaria (Plasmodium falciparum circumsporozoite protein)"

        st.session_state['disease'] = disease

# ------------------ DISPLAY RESULTS -------------------
if 'epitopes' in st.session_state:
    seq = st.session_state['sequence']
    epitopes = st.session_state['epitopes']

    st.success(f"✅ {len(epitopes)} possible epitopes found!")
    st.write("### Predicted Epitope Regions:")
    for i, ep in enumerate(epitopes, 1):
        st.markdown(f"**Epitope {i}:** `{ep}`")

    # Highlight epitopes in red
    highlighted_seq = seq
    for ep in epitopes:
        highlighted_seq = highlighted_seq.replace(ep, f"<span style='color:red; font-weight:bold'>{ep}</span>")

    st.markdown("### Highlighted Sequence (epitopes in red):", unsafe_allow_html=True)
    st.markdown(f"<pre style='white-space: pre-wrap;'>{highlighted_seq}</pre>", unsafe_allow_html=True)

# ------------------ DISEASE RESULTS -------------------
if 'disease' in st.session_state:
    st.write("---")
    st.subheader("🧠 Disease Prediction")
    st.write(f"**Predicted Disease:** {st.session_state['disease']}")

    disease_info = {
        "HIV infection (gp120 epitope)": "HIV gp120 interacts with CD4 receptors, initiating viral entry into host cells.",
        "Cancer metastasis (Integrin-binding motif)": "The RGD motif mediates integrin binding, promoting cancer cell adhesion and metastasis.",
        "Helicobacter pylori infection (CagA epitope)": "CagA protein of H. pylori disrupts gastric epithelial integrity, leading to ulcers and gastric cancer.",
        "Malaria (Plasmodium falciparum circumsporozoite protein)": "The NANP repeat epitope is recognized by immune cells, forming the basis for malaria vaccine targets.",
        "Unknown Disease": "No known disease association for the detected epitopes."
    }

    st.info(disease_info.get(st.session_state['disease'], "No detailed info available."))

# ------------------ 3D STRUCTURE -------------------
st.write("---")
st.subheader("🧩 3D Structure Viewer")
st.write("If you know the UniProt ID for this protein, enter it below:")

uniprot_id = st.text_input("UniProt ID (optional):")

if st.button("🧬 Show 3D Structure"):
    if uniprot_id:
        url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
        r = requests.get(url)
        if r.status_code == 200:
            pdb_data = r.text
            viewer = py3Dmol.view(width=600, height=400)
            viewer.addModel(pdb_data, 'pdb')
            viewer.setStyle({'cartoon': {'color': 'spectrum'}})
            viewer.zoomTo()
            html = viewer._make_html()
            components.html(html, height=400)
        else:
            st.error("3D structure not found in AlphaFold database.")
    else:
        st.warning("Please enter a UniProt ID to load the structure.")
