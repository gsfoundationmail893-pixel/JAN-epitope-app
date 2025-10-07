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
    "Hepatitis B": ["HBV", "HBsAg", "HBcAg"],
    "Ebola": ["EBOV", "VP40", "GP", "EBOLA"]
}

# =============================
# Disease information
# =============================
disease_info = {
    "COVID-19": "COVID-19 is caused by the SARS-CoV-2 virus, which affects the respiratory system and can cause fever, cough, and fatigue.",
    "HIV": "HIV attacks immune cells (CD4 T cells), weakening the immune system and leading to AIDS if untreated.",
    "Influenza": "Influenza virus causes seasonal flu with fever, sore throat, and muscle aches.",
    "Adenovirus": "Adenoviruses cause respiratory tract infections, conjunctivitis, and gastroenteritis.",
    "Hepatitis B": "Hepatitis B virus infects liver cells, causing acute and chronic liver disease.",
    "Ebola": "Ebola virus causes severe hemorrhagic fever with high mortality rates."
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
# Show 3D structure (mock visualization)
# =============================
def show_mock_structure(seq):
    viewer = py3Dmol.view(width=600, height=400)
    viewer.addModel("N" * (len(seq) // 10 + 1), "pdb")
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
- 📖 Learn about each disease  
- 🔬 Visualize a 3D mock structure
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

        st.subheader("🧩 Epitope Prediction Result")
        st.write("**Predicted Epitope Regions (approximate):**")
        for start, end in epitopes:
            st.write(f"• Positions {start}–{end} : `{seq[start-1:end]}`")

        st.subheader("🧠 Disease Prediction")
        st.write(f"**Possible Diseases:** {', '.join(diseases)}")

        for disease in diseases:
            if disease in disease_info:
                st.info(f"**{disease}:** {disease_info[disease]}")
            else:
                st.warning(f"No detailed information available for {disease}.")

        st.subheader("🧩 3D Structure Viewer")
        st.caption("This is a simulated 3D representation for visual understanding.")
        viewer = show_mock_structure(seq)
        st.components.v1.html(viewer._make_html(), height=420)
