import streamlit as st
from Bio import SeqIO
import requests
import py3Dmol

# Step 3 function
def predict_epitope(sequence):
    return [
        {"sequence": sequence[10:20], "type": "B-cell", "start": 10, "end": 20}
    ]

# Step 4 function
def get_disease_info(sequence):
    return {
        "protein_name": "Spike glycoprotein",
        "disease": "COVID-19",
        "description": "COVID-19 is caused by SARS-CoV-2..."
    }

# Step 5 function
def generate_structure(sequence):
    return """
    HEADER    MOCK STRUCTURE
    ATOM      1  N   MET A   1      11.104  13.207   2.100  1.00 20.00
    END
    """

# Step 6 function
def view_structure(pdb_string, epitopes):
    view = py3Dmol.view(width=800, height=600)
    view.addModel(pdb_string, "pdb")
    view.setStyle({"cartoon": {"color": "spectrum"}})
    for epi in epitopes:
        view.addStyle({"resi": list(range(epi["start"], epi["end"] + 1))}, {"stick": {"color": "red"}})
    view.zoomTo()
    return view

# Streamlit UI
st.title("🧬 Epitope Prediction Web App")
sequence = st.text_area("Paste Protein Sequence", height=200)

if st.button("Predict Epitope"):
    if not sequence:
        st.error("Please enter a protein sequence!")
    else:
        with st.spinner("Predicting..."):
            epitopes = predict_epitope(sequence)
            disease_info = get_disease_info(sequence)
            pdb_string = generate_structure(sequence)

        st.subheader("Predicted Epitopes")
        for epi in epitopes:
            st.write(f"Sequence: `{epi['sequence']}`, Type: `{epi['type']}`, Positions: `{epi['start']}-{epi['end']}`")

        st.subheader("Disease Info")
        st.write(f"Protein: {disease_info['protein_name']}")
        st.write(f"Disease: {disease_info['disease']}")
        st.write(f"Description: {disease_info['description']}")

        st.subheader("3D Protein Structure with Epitope Highlight")
        view = view_structure(pdb_string, epitopes)
        view.show()
