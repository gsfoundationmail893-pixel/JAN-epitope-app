import streamlit as st
import py3Dmol
import streamlit.components.v1 as components

# ===== Step 1: Epitope Prediction =====
def predict_epitope(sequence):
    # MOCK example (replace with real prediction later)
    return [
        {"sequence": sequence[10:20], "type": "B-cell", "start": 10, "end": 20},
        {"sequence": sequence[50:60], "type": "T-cell", "start": 50, "end": 60}
    ]

# ===== Step 2: Disease Association =====
def get_disease_info(sequence):
    # MOCK example (replace with UniProt API later)
    return {
        "protein_name": "Spike glycoprotein",
        "disease": "COVID-19",
        "description": "COVID-19 is caused by SARS-CoV-2, a coronavirus responsible for respiratory illness worldwide."
    }

# ===== Step 3: Structure Generation =====
def generate_structure(sequence):
    # MOCK PDB — Replace with AlphaFold/ColabFold API
    pdb_string = """
    HEADER    MOCK STRUCTURE
    ATOM      1  N   MET A   1      11.104  13.207   2.100  1.00 20.00
    ATOM      2  CA  MET A   1      12.104  14.207   3.100  1.00 20.00
    ATOM      3  C   MET A   1      13.104  15.207   2.500  1.00 20.00
    END
    """
    return pdb_string

# ===== Step 4: Viewer Function Compatible with Streamlit =====
def view_structure(pdb_string, epitopes):
    view = py3Dmol.view(width=800, height=600)
    view.addModel(pdb_string, "pdb")
    view.setStyle({"cartoon": {"color": "spectrum"}})

    # Highlight epitopes
    for epi in epitopes:
        view.addStyle({"resi": list(range(epi["start"], epi["end"] + 1))}, {"stick": {"color": "red"}})

    view.zoomTo()

    # Render as HTML for Streamlit
    html = view.render()
    components.html(html, height=600, width=800)

# ===== Streamlit App UI =====
st.title("🧬 Epitope Prediction Web App")
st.write("Paste your protein sequence below to predict epitopes, associated disease info, and view the protein structure.")

sequence = st.text_area("Paste Protein Sequence", height=200)

if st.button("Predict Epitope"):
    if not sequence:
        st.error("⚠️ Please enter a protein sequence!")
    else:
        with st.spinner("🔬 Predicting epitopes and generating structure..."):
            epitopes = predict_epitope(sequence)
            disease_info = get_disease_info(sequence)
            pdb_string = generate_structure(sequence)

        st.subheader("Predicted Epitopes")
        for epi in epitopes:
            st.markdown(f"- **Sequence:** `{epi['sequence']}`  |  **Type:** `{epi['type']}`  |  **Positions:** `{epi['start']}-{epi['end']}`")

        st.subheader("Disease Info")
        st.markdown(f"- **Protein:** {disease_info['protein_name']}")
        st.markdown(f"- **Disease:** {disease_info['disease']}")
        st.markdown(f"- **Description:** {disease_info['description']}")

        st.subheader("3D Protein Structure with Epitope Highlight")
        view_structure(pdb_string, epitopes)

