import streamlit as st
import py3Dmol
import random

# =============================
# Disease association database
# =============================
disease_database = {
    "COVID-19": ["SPIKE", "SARS", "COV", "NCOV", "CORONA"],
    "HIV": ["GAG", "POL", "ENV", "HIV"],
    "Influenza": ["HA", "NA", "HEMAGGLUTININ", "FLU"],
    "Adenovirus": ["ADENOVIRUS", "HEXON", "PENTON", "E1A"],
    "Hepatitis B": ["HBV", "HBSAG", "HBCAG"],
    "Ebola": ["EBOV", "VP40", "GP", "EBOLA"]
}

# =============================
# Disease information + side effects
# =============================
disease_info = {
    "COVID-19": {
        "definition": "COVID-19 is caused by SARS-CoV-2, affecting the respiratory system.",
        "side_effects": "Fever, cough, fatigue, and breathing difficulty."
    },
    "HIV": {
        "definition": "HIV attacks immune CD4 T cells, weakening immunity and leading to AIDS if untreated.",
        "side_effects": "Fatigue, weight loss, frequent infections."
    },
    "Influenza": {
        "definition": "Influenza virus causes seasonal flu with fever, sore throat, and body aches.",
        "side_effects": "Headache, muscle pain, and chills."
    },
    "Adenovirus": {
        "definition": "Adenoviruses cause infections of the respiratory tract and eyes.",
        "side_effects": "Sore throat, pink eye, diarrhea, and fever."
    },
    "Hepatitis B": {
        "definition": "Hepatitis B infects the liver, causing acute or chronic inflammation.",
        "side_effects": "Jaundice, abdominal pain, fatigue, dark urine."
    },
    "Ebola": {
        "definition": "Ebola virus causes severe hemorrhagic fever with high fatality.",
        "side_effects": "Bleeding, fever, vomiting, and dehydration."
    }
}

# =============================
# Predict disease from sequence
# =============================
def predict_disease_from_sequence(seq):
    seq_upper = seq.upper()
    matched_diseases = []
    for disease, markers in disease_database.items():
        if any(marker in seq_upper for marker in markers):
            matched_diseases.append(disease)
    return matched_diseases if matched_diseases else ["Unknown Disease"]

# =============================
# Epitope prediction (mock model)
# =============================
def predict_epitopes(seq):
    if len(seq) < 15:
        return [(1, len(seq))]
    positions = []
    for _ in range(random.randint(1, 3)):
        start = random.randint(1, len(seq) - 10)
        end = start + random.randint(5, 12)
        positions.append((start, min(end, len(seq))))
    return positions

# =============================
# Highlight predicted epitopes
# =============================
def highlight_epitopes(seq, epitopes):
    highlighted_seq = ""
    last_end = 0
    for start, end in sorted(epitopes):
        highlighted_seq += seq[last_end:start-1]
        highlighted_seq += f"<span style='background-color:yellow; color:black; font-weight:bold;'>{seq[start-1:end]}</span>"
        last_end = end
    highlighted_seq += seq[last_end:]
    return highlighted_seq

# =============================
# Fetch and show real 3D structure from PDB
# =============================
def show_real_structure(pdb_id):
    """
    Fetch and display a real 3D protein structure using its PDB ID.
    """
    viewer = py3Dmol.view(query=f"pdb:{pdb_id}", width=600, height=400)
    viewer.setStyle({'cartoon': {'color': 'spectrum'}})
    viewer.zoomTo()
    return viewer

# =============================
# Streamlit UI
# =============================
st.set_page_config(page_title="Epitope Binding App", layout="wide")

st.title("🧬 Epitope Binding Prediction App")
st.markdown("""
Welcome to the **Epitope Binding Prediction App**!  
This tool allows you to:
- 🧩 Identify potential epitope regions from a protein sequence  
- 🧠 Predict related diseases  
- 💡 Highlight key epitopes within the sequence  
- 📖 Learn about each disease and its side effects  
- 🔬 Visualize the actual 3D structure using PDB ID
""")

# Input boxes
sequence_input = st.text_area(
    "Enter Protein Sequence (FASTA or plain):",
    height=180,
    placeholder=">sp|P0DTC2|SARS-CoV-2 Spike Protein...\nMFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYY..."
)

pdb_id = st.text_input("Enter PDB ID to view real 3D structure (e.g., 1I22):")

if st.button("🔍 Predict Epitope and Disease"):
    if not sequence_input.strip():
        st.warning("⚠️ Please enter a valid protein sequence.")
    else:
        seq_lines = sequence_input.strip().splitlines()
        seq = "".join(line.strip() for line in seq_lines if not line.startswith(">"))
        seq = seq.upper()

        epitopes = predict_epitopes(seq)
        diseases = predict_disease_from_sequence(seq)

        # Highlighted sequence
        st.subheader("🧬 Highlighted Epitope Sequence")
        st.markdown(highlight_epitopes(seq, epitopes), unsafe_allow_html=True)

        # Epitope list
        st.subheader("🧩 Predicted Epitope Regions")
        for start, end in epitopes:
            st.write(f"• Positions {start}–{end} → `{seq[start-1:end]}`")

        # Disease prediction
        st.subheader("🧠 Disease Prediction")
        st.write(f"**Possible Diseases:** {', '.join(diseases)}")

        for disease in diseases:
            if disease in disease_info:
                st.info(f"**{disease}:** {disease_info[disease]['definition']}")
                st.write(f"**Common Side Effects:** {disease_info[disease]['side_effects']}")
            else:
                st.warning(f"No detailed information available for {disease}.")

        # Epitope-disease link
        if diseases[0] != "Unknown Disease":
            st.subheader("🧩 Epitope–Disease Relationship")
            for i, (start, end) in enumerate(epitopes, 1):
                st.write(f"Epitope {i} ({start}-{end}) may be associated with {', '.join(diseases)}.")

        # 3D Viewer (real structure)
        if pdb_id:
            st.subheader("🔬 3D Structure Viewer")
            st.caption(f"Showing real structure for **PDB ID: {pdb_id.upper()}**")
            viewer = show_real_structure(pdb_id)
            st.components.v1.html(viewer._make_html(), height=420)
        else:
            st.info("Enter a PDB ID above to visualize its real 3D structure.")
