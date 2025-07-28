# summarizer.py

from typing import List, Dict
from collections import defaultdict
import re

# Basic keyword-based summarizer using sentence scoring

def summarize_sections(ranked_sections: List[Dict], all_sections: List[Dict]) -> List[Dict]:
    """
    Summarize top-ranked sections using simple keyword and sentence scoring.

    Args:
        ranked_sections: List of top relevant sections from ranker
        all_sections: All original extracted sections

    Returns:
        List of dicts with document, page, and refined_text summary
    """
    summaries = []
    section_map = defaultdict(str)

    # Build a lookup for full text
    for sec in all_sections:
        key = (sec["document"], sec["page"])
        section_map[key] = sec["text"]

    for sec in ranked_sections:
        key = (sec["document"], sec["page"])
        full_text = section_map.get(key, "")

        # Basic summarization: pick top 2-3 scored sentences
        summary = extract_summary(full_text)

        summaries.append({
            "document": sec["document"],
            "page": sec["page"],
            "refined_text": summary
        })

    return summaries


def extract_summary(text: str, max_sentences: int = 3) -> str:
    """Returns a short summary from the input text using naive scoring."""
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    keywords = ["GNN", "neural", "drug", "discovery", "method", "dataset", "performance"]
    sentence_scores = []

    for sent in sentences:
        score = sum(sent.lower().count(k.lower()) for k in keywords)
        sentence_scores.append((score, sent))

    # Sort by score, take top N
    top_sentences = [s for _, s in sorted(sentence_scores, reverse=True)[:max_sentences]]
    return " ".join(top_sentences)