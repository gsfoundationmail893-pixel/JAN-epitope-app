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
# Mock 3D structure viewer (fixed blank issue)
# =============================
def show_mock_structure(seq):
    viewer = py3Dmol.view(width=600, height=400)
    pdb_data = """
ATOM      1  N   MET A   1      11.104  13.207  10.215  1.00  0.00           N
ATOM      2  CA  MET A   1      12.560  13.387  10.415  1.00  0.00           C
ATOM      3  C   MET A   1      13.004  14.849  10.215  1.00  0.00           C
ATOM      4  O   MET A   1      12.460  15.757  10.815  1.00  0.00           O
END
"""
    viewer.addModel(pdb_data, "pdb")
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
- 🔬 Visualize a 3D mock protein structure
""")

sequence_input = st.text_area(
    "Enter Protein Sequence (FASTA or plain):",
    height=180,
    placeholder=">sp|P0DTC2|SARS-CoV-2 Spike Protein...\nMFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYY..."
)

if st.button("🔍 Predict Epitope and Disease"):
    if not sequence_input.strip():
        st.warning("⚠️ Please enter a valid protein sequence.")
    else:
        seq_lines = sequence_input.strip().splitlines()
        seq = "".join(line.strip() for line in seq_lines if not line.startswith(">"))
        seq = seq.upper()

        epitopes = predict_epitopes(seq)
        diseases = predict_disease_from_sequence(seq)

        # Highlight sequence
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

        # 3D Viewer
        st.subheader("🔬 3D Structure Viewer")
        st.caption("Simulated 3D representation for understanding epitope binding.")
        viewer = show_mock_structure(seq)
        st.components.v1.html(viewer._make_html(), height=420
