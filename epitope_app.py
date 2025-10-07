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

    for epi in epitopes:
        res_range = list(range(epi["start"], epi["end"] + 1))
        view.addStyle({"resi": res_range}, {"stick": {"color": "red"}})

    view.zoomTo()
    html =
