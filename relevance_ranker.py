from sentence_transformers import SentenceTransformer, util
from typing import List, Dict
import torch
import os

# Load the local model
model_path = "./all-MiniLM-L6-v2"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model path '{model_path}' not found.")

model = SentenceTransformer(model_path)

def rank_sections(persona: str, job_to_be_done: str, sections: List[Dict], top_k: int = 5) -> List[Dict]:
    query = f"{persona} needs to: {job_to_be_done}"
    query_embedding = model.encode(query, convert_to_tensor=True)

    scored_sections = []
    for section in sections:
        text = section.get("text", "")
        if not text.strip():
            continue
        section_embedding = model.encode(text, convert_to_tensor=True)
        similarity_score = util.pytorch_cos_sim(query_embedding, section_embedding).item()
        scored_sections.append({
            "document": section.get("document", "unknown.pdf"),
            "page": section.get("page", -1),
            "section_title": section.get("section_title", "Untitled"),
            "text": text,
            "score": round(similarity_score, 4)
        })

    scored_sections.sort(key=lambda x: x["score"], reverse=True)

    for idx, sec in enumerate(scored_sections[:top_k]):
        sec["importance_rank"] = idx + 1

    return scored_sections[:top_k]
