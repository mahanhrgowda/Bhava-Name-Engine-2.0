import streamlit as st
import json
import pandas as pd
from batch_name_input import process_batch_csv
from reverse_bhava_name_generator import suggest_names_for_bhava
from name_similarity import find_similar_names
from batch_similarity_clusters import generate_similarity_clusters, generate_similarity_clusters_json
from phoneme_logger import get_bhava_vector_with_log, get_dominant_bhava
from utils import format_name

st.set_page_config(page_title="Bhāva Name Engine", layout="wide")
st.title("🔮 Bhāva Name Engine")

# Load and show Bhāva dataset
st.subheader("📖 Bhāva Glossary")
with open("data/bhava_dataset.json", encoding="utf-8") as f:
    bhava_data = json.load(f)

df = pd.DataFrame(bhava_data)
st.dataframe(df)

# Batch CSV Input Section
st.subheader("📥 Batch CSV Name Input")
uploaded_file = st.file_uploader("Upload a CSV file with a 'Name' column", type=["csv"])

name_list = []
log_df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'Name' not in df.columns:
        st.error("❌ CSV must contain a 'Name' column.")
    else:
        df['Name'] = df['Name'].apply(format_name)
        logs = []
        vectors = []
        dominants = []
        for name in df['Name']:
            vector, log = get_bhava_vector_with_log(name)
            vectors.append(vector)
            dominants.append(get_dominant_bhava(vector))
            logs.append(", ".join([f"{p}→{b}" for p, b in log]))
        df['Bhāva Vector'] = vectors
        df['Dominant Bhāva'] = dominants
        df['Phoneme→Bhāva Log'] = logs
        name_list = df['Name'].tolist()

        st.success("✅ Processed with phoneme logs!")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📄 Download Tagged Names with Logs", csv, "tagged_names_with_logs.csv", "text/csv")

# Reverse Bhāva to Name Generator
st.subheader("🔁 Suggest Names by Bhāva")
selected_bhava = st.selectbox("Select a Bhāva", df['bhava'])
if selected_bhava:
    suggestions = suggest_names_for_bhava(selected_bhava)
    st.markdown("### 💡 Suggested Names:")
    st.write(", ".join(suggestions))

# Name Similarity Tool
st.subheader("🧬 Find Emotionally Similar Names")
input_name = st.text_input("Enter a name to compare:")
if input_name and name_list:
    similar_names = find_similar_names(input_name, name_list)
    st.markdown(f"### 🔍 Top Matches for `{input_name}`:")
    sim_df = pd.DataFrame(similar_names, columns=["Name", "Similarity Score"])
    st.dataframe(sim_df)

    export_csv = sim_df.to_csv(index=False).encode("utf-8")
    st.download_button("📄 Download Similar Name Matches", export_csv, f"{input_name}_similar_names.csv", "text/csv")
elif input_name and not name_list:
    st.info("📥 Upload a CSV with names first to enable similarity matching.")

# Batch Clustering
st.subheader("📊 Batch Name Clustering (Top Matches for All)")
if name_list:
    cluster_df = generate_similarity_clusters(name_list)
    st.dataframe(cluster_df)
    export_all_csv = cluster_df.to_csv(index=False).encode("utf-8")
    st.download_button("📄 Download All Name Clusters (CSV)", export_all_csv, "name_similarity_clusters.csv", "text/csv")

    cluster_json_dict = generate_similarity_clusters_json(name_list)
    json_str = json.dumps(cluster_json_dict, ensure_ascii=False, indent=2)
    st.download_button("💾 Download All Clusters (JSON)", json_str, "name_similarity_clusters.json", "application/json")

# Single Name Bhāva Analysis
st.subheader("🔍 Single Name Bhāva Analysis")
single_name = st.text_input("Enter a name for detailed analysis:")
if single_name:
    formatted_name = format_name(single_name)
    vector, log = get_bhava_vector_with_log(formatted_name)
    dominant = get_dominant_bhava(vector)

    st.markdown(f"### 🧠 Bhāva Vector for `{formatted_name}`:")
    st.json({bhava: score for bhava, score in zip(df['bhava'], vector)})

    st.markdown(f"### 🏆 Dominant Bhāva: **{dominant}** {df[df['bhava'] == dominant]['rasa_emoji'].values[0]}")

    if log:
        st.markdown("### 🪷 Phoneme → Bhāva Matches:")
        for phoneme, bhava in log:
            emoji = df[df['bhava'] == bhava]['rasa_emoji'].values[0]
            st.markdown(f"- `{phoneme}` → **{bhava}** {emoji}")
    else:
        st.info("No phonemes matched from the Maheshwara map.")

import streamlit.components.v1 as components

# Single Name Bhāva Analysis with Copy Button
st.subheader("🔍 Single Name Bhāva Analysis")
single_name = st.text_input("Enter a name for detailed analysis:")
if single_name:
    formatted_name = format_name(single_name)
    vector, log = get_bhava_vector_with_log(formatted_name)
    dominant = get_dominant_bhava(vector)

    bhava_dict = {bhava: score for bhava, score in zip(df['bhava'], vector)}
    emoji = df[df['bhava'] == dominant]['rasa_emoji'].values[0]

    summary = f"Name: {formatted_name}\n"
    summary += f"Dominant Bhāva: {dominant} {emoji}\n"
    summary += "Phoneme → Bhāva Log:\n"
    for phoneme, bhava in log:
        rasa_emoji = df[df['bhava'] == bhava]['rasa_emoji'].values[0]
        summary += f"  - {phoneme} → {bhava} {rasa_emoji}\n"

    st.markdown(f"### 🧠 Bhāva Vector for `{formatted_name}`:")
    st.json(bhava_dict)

    st.markdown(f"### 🏆 Dominant Bhāva: **{dominant}** {emoji}")

    st.markdown("### 🪷 Phoneme → Bhāva Matches:")
    for phoneme, bhava in log:
        rasa_emoji = df[df['bhava'] == bhava]['rasa_emoji'].values[0]
        st.markdown(f"- `{phoneme}` → **{bhava}** {rasa_emoji}")

    st.markdown("### 📥 Copy Bhāva Summary to Clipboard:")
    components.html(f'''
        <textarea id="bhavaSummary" rows="10" cols="60">{summary}</textarea><br>
        <button onclick="navigator.clipboard.writeText(document.getElementById('bhavaSummary').value)">📋 Copy to Clipboard</button>
    ''', height=250)
