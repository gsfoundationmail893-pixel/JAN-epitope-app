import streamlit as st
import requests
import py3Dmol
import streamlit.components.v1 as components

# ===== Step 1: Epitope Prediction (Mock logic) =====
def predict_epitopes(sequence):
    if len(sequence) < 60:
        return []
    return [
        {"sequence": sequence[10:20], "type": "B-cell", "start": 10, "end": 20},
        {"sequence": sequence[50:60], "type": "T-cell", "start": 50, "end": 60}
    ]

# ===== Step 2: Fetch REAL Disease Information from UniProt =====
def get_disease_info(uniprot_id):
    try:
        url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
        response = requests.get(url)
        if response.status_code != 200:
            return [{"disease": "Not Found", "description": "No disease data available."}]
        data = response.json()

        # Extract disease-related comments
        disease_list = []
        for item in data.get("comments", []):
            if item.get("commentType") == "DISEASE":
                disease_name = item["disease"]["diseaseId"]
                description = item["disease"].get("description", "No description available.")
                disease_list.append({"disease": disease_name, "description": description})

        if not disease_list:
            disease_list.append({"disease": "Unknown", "description": "No disease information found."})
        return disease_list
    except Exception as e:
        return [{"disease": "Error", "description": f"Could not fetch disease info: {e}"}]

# ===== Step 3: Fetch REAL 3D Structure from AlphaFold =====
def fetch_3d_structure(uniprot_id):
    try:
        url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception:
        return None

# ===== Step 4: 3D Viewer Function =====
def view_structure(pdb_string, epitopes):
    view = py3Dmol.view(width=800, height=600)
    view.addModel(pdb_string, "pdb")
    view.setStyle({"cartoon": {"color": "spectrum"}})

    # Highlight predicted epitopes in red
    for epi in epitopes:
        res_range = list(range(epi["start"], epi["end"] + 1))
        view.addStyle({"resi": res_range}, {"stick": {"color": "red"}})

    view.zoomTo()
    html = view._make_html()  # ✅ Corrected syntax line
    components.html(html, height=600, width=800)

# ===== Streamlit Interface =====
st.title("🧬 Epitope Prediction & Protein Structure Viewer")
st.write("Enter a UniProt ID and/or a protein sequence to predict epitopes, view real disease data, and explore the AlphaFold 3D structure.")

uniprot_id = st.text_input("Enter UniProt ID (e.g., P51587 for BRCA2_HUMAN):")
sequence = st.text_area("Paste Protein Sequence (optional):", height=200)

if st.button("🔍 Predict Epitope"):
    if not uniprot_id and not sequence:
        st.error("⚠️ Please enter either a UniProt ID or a protein sequence.")
    else:
        with st.spinner("Processing..."):
            # Fetch protein sequence from UniProt if not pasted
            if not sequence and uniprot_id:
                fasta_url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
                fasta_response = requests.get(fasta_url)
                if fasta_response.status_code == 200:
                    fasta_text = fasta_response.text
                    sequence = "".join(fasta_text.split("\n")[1:])
                else:
                    st.warning("Could not fetch sequence from UniProt.")

            # Predict epitopes
            epitopes = predict_epitopes(sequence) if sequence else []

            # Get disease info
            disease_info = get_disease_info(uniprot_id) if uniprot_id else []

            # Fetch structure
            pdb_string = fetch_3d_structure(uniprot_id) if uniprot_id else None

        # --- Display Predicted Epitopes ---
        st.subheader("🧩 Predicted Epitopes")
        if epitopes:
            for epi in epitopes:
                st.write(f"**Sequence:** {epi['sequence']} | **Type:** {epi['type']} | **Positions:** {epi['start']}-{epi['end']}")
        else:
            st.info("No epitopes predicted (sequence too short or missing).")

        # --- Display Disease Info ---
        st.subheader("🧫 Associated Diseases")
        if disease_info:
            for d in disease_info:
                st.markdown(f"**Disease:** {d['disease']}  \n🩸 *{d['description']}*")
        else:
            st.info("No disease information found for this protein.")

        # --- Display Structure ---
        st.subheader("🧠 3D Protein Structure (from AlphaFold)")
        if pdb_string:
            view_structure(pdb_string, epitopes)
        else:
            st.warning("No 3D structure found in AlphaFold for this UniProt ID.")
