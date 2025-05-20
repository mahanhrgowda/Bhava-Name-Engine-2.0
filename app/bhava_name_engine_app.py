import streamlit as st
import json
import pandas as pd
from batch_name_input import process_batch_csv
from reverse_bhava_name_generator import suggest_names_for_bhava
from name_similarity import find_similar_names
from batch_similarity_clusters import generate_similarity_clusters, generate_similarity_clusters_json

st.set_page_config(page_title="Bhāva Name Engine", layout="wide")
st.title("🔮 Bhāva Name Engine")

# Load and show Bhāva dataset
st.subheader("📖 Bhāva Glossary")
with open("bhava_dataset.json", encoding="utf-8") as f:
    bhava_data = json.load(f)

df = pd.DataFrame(bhava_data)
st.dataframe(df)

# Batch CSV Input Section
st.subheader("📥 Batch CSV Name Input")
uploaded_file = st.file_uploader("Upload a CSV file with a 'Name' column", type=["csv"])

name_list = []
result_df = None
if uploaded_file:
    result_df, error = process_batch_csv(uploaded_file)
    if error:
        st.error(f"❌ Error: {error}")
    else:
        st.success("✅ Processed successfully!")
        st.dataframe(result_df)
        name_list = result_df['Name'].tolist()
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Tagged CSV", csv, "tagged_names.csv", "text/csv")

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

    # JSON Export
    cluster_json_dict = generate_similarity_clusters_json(name_list)
    json_str = json.dumps(cluster_json_dict, ensure_ascii=False, indent=2)
    st.download_button("💾 Download All Clusters (JSON)", json_str, "name_similarity_clusters.json", "application/json")
