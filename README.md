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
    "input_documents": [
      "cardio_risk_prediction.pdf",
      "deep_learning_medical_diagnosis.pdf",
      "research paper 1.pdf"
    ],
    "persona": "PhD Researcher in Medical Machine Learning",
    "job_to_be_done": "Write a literature review on the use of machine learning and deep learning techniques in cardiovascular disease diagnosis and prediction, including model comparisons and clinical applications.",
    "processing_timestamp": "2025-07-28T22:41:36.591115"
  },
  "extracted_sections": [
    {
      "document": "cardio_risk_prediction.pdf",
      "page": 1,
      "section_title": "Title: Machine Learning Applications in Cardiovascular Risk Prediction",
      "importance_rank": 1
    },
    {
      "document": "deep_learning_medical_diagnosis.pdf",
      "page": 1,
      "section_title": "Title: Deep Learning for Medical Diagnosis: Challenges and Opportunities",
      "importance_rank": 2
    },
    {
      "document": "research paper 1.pdf",
      "page": 4,
      "section_title": "The findings confirm that:",
      "importance_rank": 3
    },
    {
      "document": "research paper 1.pdf",
      "page": 1,
      "section_title": "\u201cHeart Failure Prediction with Machine Learning: A Comparative",
      "importance_rank": 4
    },
    {
      "document": "research paper 1.pdf",
      "page": 2,
      "section_title": "Limited attention to",
      "importance_rank": 5
    }
  ],
  "subsection_analysis": [
    {
      "document": "cardio_risk_prediction.pdf",
      "page": 1,
      "refined_text": "Title: Machine Learning Applications in Cardiovascular Risk Prediction Abstract: This paper presents a study on the application of various machine learning algorithms in predicting card Conclusion: Gradient boosting outperformed other models with an AUC of 0.91. Future work will include deep learni"
    },
    {
      "document": "deep_learning_medical_diagnosis.pdf",
      "page": 1,
      "refined_text": "Title: Deep Learning for Medical Diagnosis: Challenges and Opportunities Abstract: We explore how deep learning is transforming medical diagnosis with a focus on chronic conditions like Conclusion: While deep learning shows great promise in automating diagnosis, issues with interpretability, data bias"
    },
    {
      "document": "research paper 1.pdf",
      "page": 4,
      "refined_text": "\uf0b7  The combination of Z-score normalization and SMOTE provided the most significant performance improvements across models. \uf0b7  Ensemble learning methods (Random Forest, Gradient Boosting, Extra Trees) are superior in handling complex patterns and producing robust results. The findings confirm that: \uf0b7  Data preprocessing significantly impacts model performance."
    },
    {
      "document": "research paper 1.pdf",
      "page": 1,
      "refined_text": "The study specifically aims to address two major concerns in clinical datasets: class imbalance and feature scaling , which can significantly affect model performance. \uf0b7  Use of small, balanced datasets that do not represent real-world scenarios. The key contributions include: \uf0b7  Comparison of 18 ML algorithms on a heart failure dataset."
    },
    {
      "document": "research paper 1.pdf",
      "page": 2,
      "refined_text": "Dataset The study uses the Cleveland Heart Disease dataset from the UCI Machine Learning Repository. A key characteristic of the dataset is its class imbalance \u2014 a common issue in medical datasets \u2014 where fewer patients are labeled as having heart disease. \uf0b7  Limited attention to scaling techniques , despite their influence on algorithm performance."
    }
  ]
}
