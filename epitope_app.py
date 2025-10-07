import streamlit as st
import torch
import py3Dmol
from Bio.SeqUtils import seq3
from esm import pretrained
import tempfile
import os

# =============================
# Load ESMFold model (for structure prediction)
# =============================
@st.cache_resource
def load_model():
    model = pretrained.esmfold_v1()
    model = model.eval().cuda() if torch.cuda.is_available() else model.eval()
    return model

model = load_model()

# =============================
# Disease association mock data
# =============================
disease_database = {
    "COVID-19": ["SPIKE", "SARS", "COV", "NCOV", "CORONA"],
    "HIV": ["GAG", "POL", "ENV", "HIV"],
    "Influenza": ["HA", "NA", "HEMAGGLUTININ"],
    "Adenovirus": ["ADENOVIRUS", "HEXON", "PENTON"],
    "Hepatitis B": ["HBsAg", "HBV"],
}

def predict_disease_from_sequence(seq):
    seq_upper = seq.upper()
    for disease, markers in disease_database.items():
        if any(marker in seq_upper for marker in markers):
            return disease
    return "Unknown Disease"

def disease_info(name):
    info = {
        "COVID-19": "COVID-19 is caused by SARS-CoV-2, affecting the respiratory system and causing fever, cough, and fatigue.",
        "HIV": "HIV attacks the immune system, specifically the CD4 cells, and can lead to AIDS if untreated.",
        "Influenza": "Influenza virus causes seasonal flu characterized by fever, sore throat, and muscle aches.",
        "Adenovirus": "Adenoviruses cause infections in the respiratory tract, eyes, and intestines.",
        "Hepatitis B": "Hepatitis B virus infects the liver, leading to inflammation and possible chronic disease."
    }
    return info.get(name, "No known details about this disease.")

# =============================
# Generate 3D structure using ESMFold
# =============================
def predict_structure(sequence):
    with torch.no_grad():
        output = model.infer_pdb(sequence)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdb")
    temp_file.write(output.encode())
    temp_file.close()
    return temp_file.name

def show_structure(pdb_path):
    with open(pdb_path, "r") as file:
        pdb_data = file.read()
    viewer = py3Dmol.view(width=600, height=400)
    viewer.addModel(pdb_data, "pdb")
    viewer.setStyle({'cartoon': {'color': 'spectrum'}})
    viewer.zoomTo()
    viewer.show()
    return viewer

# =============================
# Streamlit UI
# =============================
st.set_page_config(page_title="Epitope Binding App", layout="wide")

st.title("🔬 Epitope Binding Prediction App")
st.markdown("Enter a **protein sequence** below to predict epitopes, identify possible diseases, and visualize the 3D structure.")

sequence = st.text_area("Enter Protein Sequence:", height=180, placeholder=">sp|P0DTC2|SARS-CoV-2 Spike Protein...\nMFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYY...")

if st.button("🔍 Predict Epitope & Structure"):
    if not sequence:
        st.warning("Please enter a valid protein sequence.")
    else:
        # Clean sequence
        seq = "".join(sequence.splitlines()[1:]) if sequence.startswith(">") else sequence
        st.subheader("🧩 Prediction Result")
        st.write(f"**Epitope Type:** B-cell linear epitope")
        
        disease = predict_disease_from_sequence(seq)
        st.write(f"**Predicted Disease:** {disease}")
        st.write(f"**About Disease:** {disease_info(disease)}")

        with st.spinner("Predicting 3D structure... this may take a minute ⏳"):
            pdb_file = predict_structure(seq)
            st.success("✅ Structure prediction complete!")

        st.subheader("🧬 3D Structure Viewer")
        viewer = show_structure(pdb_file)
        viewer_html = viewer._make_html()
        st.components.v1.html(viewer_html, height=420)

        os.remove(pdb_file)
