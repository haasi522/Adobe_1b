# main.py
print("🚀 Starting main.py execution...")


import os
import json
from datetime import datetime
from pdf_reader import extract_text_sections
from relevance_ranker import rank_sections
from summarizer import summarize_sections

def main():
    input_dir = "input"
    output_dir = "output"

    # Validate input folder
    if not os.path.exists(input_dir):
        print("❌ input/ folder not found.")
        return

    # Load persona and job
    try:
        with open(os.path.join(input_dir, "persona.txt")) as f:
            persona = f.read().strip()
        print("✅ Loaded persona:", persona)

        with open(os.path.join(input_dir, "job.txt")) as f:
            job = f.read().strip()
        print("✅ Loaded job-to-be-done:", job)

    except Exception as e:
        print("❌ Failed to read persona or job:", str(e))
        return

    # Check PDFs
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]
    if not pdf_files:
        print("❌ No PDF files found in input/.")
        return
    print("📄 Found PDF files:", pdf_files)

    # Extract text from each PDF
    all_sections = []
    for pdf in pdf_files:
        pdf_path = os.path.join(input_dir, pdf)
        print(f"🔍 Extracting sections from {pdf}...")
        extracted = extract_text_sections(pdf_path)
        print(f"   → {len(extracted)} sections found.")
        all_sections.extend(extracted)

    if not all_sections:
        print("❌ No sections extracted from PDFs.")
        return

    print(f"✅ Total sections extracted: {len(all_sections)}")

    # Rank relevant sections
    ranked_sections = rank_sections(persona, job, all_sections, top_k=5)
    print(f"🏆 Top {len(ranked_sections)} relevant sections ranked.")

    # Summarize those sections
    summaries = summarize_sections(ranked_sections, all_sections)
    print(f"📝 {len(summaries)} summaries generated.")

    # Final output JSON
    output_json = {
        "metadata": {
            "input_documents": pdf_files,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [
            {
                "document": sec["document"],
                "page": sec["page"],
                "section_title": sec["section_title"],
                "importance_rank": sec["importance_rank"]
            }
            for sec in ranked_sections
        ],
        "subsection_analysis": summaries
    }

    # Save to output folder
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "challenge1b_output.json")
    with open(output_path, "w") as f:
        json.dump(output_json, f, indent=2)

    print("✅ Output saved to:", output_path)
    print(json.dumps(output_json, indent=2))


if __name__ == "__main__":
    main()
