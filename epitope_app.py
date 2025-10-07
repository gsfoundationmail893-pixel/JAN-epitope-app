import streamlit as st
import requests
import json
import stmol
from Bio import SeqIO
from io import StringIO

# Function to predict epitopes (mock implementation)
def predict_epitopes(sequence):
    # Replace with actual epitope prediction logic
    return [
        {"sequence": sequence[10:20], "type": "B-cell", "start": 10, "end": 20},
        {"sequence": sequence[50:60], "type": "T-cell", "start": 50, "end": 60}
    ]

# Function to fetch disease information from UniProt
def get_disease_info(protein_id):
    url = f"https://rest.uniprot.org/uniprotkb/{protein_id}.json"
    response = requests.get(url)
    data = response.json()
    diseases = data.get('diseases', [])
    disease_info = [{"disease": disease['name'], "description": disease.get('description', 'No description available')} for disease in diseases]
    return disease_info

# Function to fetch 3D structure using AlphaFold or similar service
def fetch_3d_structure(sequence):
    # Replace with actual structure fetching logic
    # For demonstration, we'll use a mock PDB string
    pdb_string = """
    HEADER    MOCK STRUCTURE
    ATOM      1  N   MET A   1      11.104  13.207   2.100  1.00 20.00
    ATOM      2  CA  MET A   1      12.104  14.207   3.100  1.00 20.00
    ATOM      3  C   MET A   1      13.104  15.207   2.500  1.00 20.00
    ATOM      4  O   MET A   1      14.104  16.207   2.900  1.00 20.00
    END
    """
    return pdb_string

# Function to render 3D structure using Stmol
def render_3d_structure(pdb_string, epitopes):
    viewer = stmol.view(width=800, height=600)
    viewer.add_model(pdb_string, "pdb")
    viewer.set_style({"cartoon": {"color": "spectrum"}})

    # Highlight epitopes
    for epi in epitopes:
        viewer.add_style({"resi": list(range(epi["start"], epi["end"] + 1))}, {"stick": {"color": "red"}})

    viewer.zoom_to()
    viewer.show()

# Streamlit UI
st.title("🧬 Epitope Prediction and Protein Structure Viewer")
st.write("Enter a protein sequence to predict epitopes, view associated diseases, and explore the 3D structure.")

sequence_input = st.text_area("Protein Sequence", height=200)

if st.button("Analyze"):
    if sequence_input:
        with st.spinner("Processing..."):
            # Predict epitopes
            epitopes = predict_epitopes(sequence_input)

            # Fetch disease information (mock protein ID used here)
            disease_info = get_disease_info("P12345")

            # Fetch 3D structure
            pdb_string = fetch_3d_structure(sequence_input)

        # Display results
        st.subheader("Predicted Epitopes")
        for epi in epitopes:
            st.write(f"**Sequence:** {epi['sequence']} | **Type:** {epi['type']} | **Position:** {epi['start']}-{epi['end']}")

        st.subheader("Associated Diseases")
        for disease in disease_info:
            st.write(f"**Disease:** {disease['disease']} | **Description:** {disease['description']}")

        st.subheader("3D Protein Structure")
        render_3d_structure(pdb_string, epitopes)
    else:
        st.error("Please enter a protein sequence.")
