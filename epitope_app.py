import streamlit as st
import requests
import py3Dmol
import streamlit.components.v1 as components

# ===== Step 1: Epitope Prediction =====
def predict_epitopes(sequence):
    # MOCK prediction — replace with real API later
    return [
        {"sequence": sequence[10:20], "type": "B-cell", "start": 10, "end": 20},
        {"sequence": sequence[50:60], "type": "T-cell", "start": 50, "end": 60}
    ]

# ===== Step 2: Disease Association =====
def get_disease_info(protein_id="P12345"):
    try:
        url = f"https://rest.uniprot.org/uniprotkb/{protein_id}.json"
        response = requests.get(url)
        data = response.json()
        diseases = data.get("diseases", [])
        if diseases:
            return [{"disease": d["name"], "description": d.get("description", "No description")} for d in diseases]
        else:
            return [{"disease": "Unknown", "description": "No disease information found."}]
    except:
        return [{"disease": "Error", "description": "Could not fetch disease information."}]

# ===== Step 3: Structure Generation =====
def fetch_3d_structure(sequence):
    # MOCK PDB — replace with AlphaFold/ColabFold API later
    pdb_string = """
HEADER    MOCK STRUCTURE
ATOM      1  N   MET A   1      11.104  13.207   2.100  1.00 20.00
ATOM      2  CA  MET A   1      12.104  14.207   3.100  1.00 20.00
ATOM      3  C   MET A   1      13.104  15.207   2.500  1.00 20.00
ATOM      4  O   MET A   1      14.104  16.207   2.900  1.00 20.00
END
"""
    return pdb_string

# ===== Step 4: Viewer Function for Streamlit =====
def view_structure(pdb_string, epitopes):
    view = py3Dmol.view(width=800, height=600)
    view.addModel(pdb_string, "pdb")
    view.setStyle({"cartoon": {"color": "spectrum"}})

    for epi in epitopes:
        view.addStyle({"resi": list(range(epi["start"], epi["end"] + 1))}, {"stick": {"color": "red"}})

    view.zoomTo()
    html = view._make_html()
    components.html(html, height=600, width=800)

# ===== Streamlit UI =====
st.title("🧬 Epitope Prediction and Protein Structure Viewer")
st.write("Enter a protein sequence to predict epitopes, view associated diseases, and explore the 3D structure.")

sequence = st.text_area("Paste Protein Sequence", height=200)

if st.button("Predict Epitope"):
    if not sequence:
        st.error("⚠️ Please enter a protein sequence!")
    else:
        with st.spinner("🔬 Predicting epitopes and generating structure..."):
            epitopes = predict_epitopes(sequence)
            disease_info = get_disease_info()
            pdb_string = fetch_3d_structure(sequence)

        st.subheader("Predicted Epitopes")
        for epi in epitopes:
            st.write(f"**Sequence:** {epi['sequence']} | **Type:** {epi['type']} | **Positions:** {epi['start']}-{epi['end']}")

        st.subheader("Disease Info")
        for disease in disease_info:
            st.write(f"**Disease:** {disease['disease']} | **Description:** {disease['description']}")

        st.subheader("3D Protein Structure with Epitope Highlight")
        view_structure(pdb_string, epitopes)

