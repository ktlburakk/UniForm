from sentence_transformers import SentenceTransformer, util
import torch
import streamlit as st

@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def get_semantic_mapping(unique_values, threshold=0.75):
    if not unique_values:
        return {}

    model = load_model()
    # Vectorize the values
    embeddings = model.encode(unique_values, convert_to_tensor=True)
    # Compute cosine similarity matrix
    cosine_scores = util.cos_sim(embeddings, embeddings)
    
    mapping = {}
    processed = set()

    for i in range(len(unique_values)):
        if unique_values[i] in processed:
            continue
        
        similar_indices = torch.where(cosine_scores[i] > threshold)[0].tolist()
        group_items = [unique_values[idx] for idx in similar_indices]
        
        # Choose the shortest and clearest representation as the canonical value
        canonical_value = min(group_items, key=len) 
        
        for idx in similar_indices:
            val = unique_values[idx]
            mapping[val] = canonical_value
            processed.add(val)
            
    return mapping

def clean_and_standardize(series, threshold=0.75):
    
    series = series.fillna("Unspecified").astype(str).str.strip().str.title()
    
    raw_values = series.unique().tolist()
    
    mapping_dict = get_semantic_mapping(raw_values, threshold)
    
    # Apply the mapping to standardize the series
    standardized_series = series.map(mapping_dict)
    
    return standardized_series