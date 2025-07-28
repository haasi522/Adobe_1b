# Adobe_1B – Persona-Driven Document Intelligence (Dockerized)

## Project Overview

### Mission

The goal of this challenge is to build an intelligent system that **extracts and prioritizes relevant sections** from a collection of PDF documents, tailored to a **user persona** and their **job-to-be-done**. Rather than treating all content equally, the system should determine **what matters most to whom and for what purpose**.

This system forms the foundation for personalized document understanding, targeted summarization, and intelligent information retrieval based on the user's role and intent.

###  Objective

Given a set of PDFs, a persona description, and a job-to-be-done, the system must:

- Parse each PDF document into sections
- Understand the persona's context and goal using semantic embeddings
- Rank document sections based on relevance
- Return a structured output with:
  - Metadata
  - Top relevant sections with importance scores
  - Refined sub-section summaries

---

## Approach

The pipeline integrates both **semantic understanding** and **lightweight ranking logic** to prioritize the most relevant content.

### 1. PDF Text Extraction
Uses PyMuPDF (`fitz`) to extract:
- Page-wise text
- Sectional content with document name and page number

### 2. Semantic Embedding with Sentence Transformers
Embeds:
- Persona description
- Job-to-be-done
- Document sections

Uses a compact transformer model to run efficiently on CPU within the allowed model size.

### 3. Similarity-Based Ranking
- Cosine similarity is computed between job+persona and document sections
- Top-K most relevant sections are selected
- Each section is assigned an `importance_rank`

### 4. JSON Output Generation
- Includes metadata (persona, job, timestamp)
- Lists most relevant sections from the documents
- Includes concise sub-section summaries

---

## Libraries and Tools Used

- **PyMuPDF (fitz)** – For PDF reading and page-wise text extraction  
- **Sentence-Transformers** – For generating semantic embeddings  
- **Torch** – Lightweight model inference on CPU  
- **NumPy** – Numerical processing  
- **scikit-learn** – Cosine similarity scoring and ranking  
- **Docker** – For offline, reproducible deployment  

---

## Files and Project Structure

This repository contains the following core components:

- `main.py`  
  Runs the complete pipeline — text extraction, embedding, ranking, and output generation.

- `src/extract_text.py`  
  Extracts and formats page-wise text from input PDFs.

- `src/persona_analyzer.py`  
  Loads the transformer model, embeds persona/job and document sections.

- `src/section_ranker.py`  
  Computes similarity scores and ranks relevant sections.

- `src/output_generator.py`  
  Generates structured output in the required JSON format.

- `input/`  
  Contains:
  - `documents/`: PDF files  
  - `persona.txt`: Description of the user persona  
  - `job.txt`: Job-to-be-done description  

- `output/challenge1b_output.json`  
  Final output with extracted sections and metadata.

- `models/`  
  Pre-downloaded sentence-transformer model used for offline execution.

- `requirements.txt`  
  Lists Python dependencies.

- `Dockerfile`  
  Defines the Docker environment for reproducible execution.





## Output Format

The system produces a structured JSON (`challenge1b_output.json`) with:

- **Metadata**: Input documents, persona, job description, timestamp  
- **Extracted Sections**: Document name, page number, section title, importance rank  
- **Subsection Analysis**: Refined text extracted from the relevant section  

Example snippet:
```json
{
  "metadata": {
    "input_documents": ["chemistry_1.pdf", "chemistry_2.pdf"],
    "persona": "Undergraduate Chemistry Student",
    "job_to_be_done": "Identify key concepts and mechanisms in reaction kinetics",
    "timestamp": "2025-07-28T22:00:00"
  },
  "extracted_sections": [
    {
      "document": "chemistry_1.pdf",
      "page_number": 6,
      "section_title": "Reaction Rates and Mechanisms",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "chemistry_1.pdf",
      "page_number": 6,
      "refined_text": "Reaction rates increase with concentration and temperature..."
    }
  ]
}
