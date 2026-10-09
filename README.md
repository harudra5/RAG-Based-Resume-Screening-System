# RAG-Based Resume Screening System

An intelligent recruitment application that uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from resumes, match candidates against job descriptions, and support candidate screening and ranking.

## Overview

Recruiters often spend considerable time reviewing resumes and identifying candidates who meet job requirements. This project streamlines the process by combining resume document processing, retrieval techniques, and job description matching in a single application.

## Key Features

- **Resume Document Loading:** Extract text from resume documents.
- **Text Chunking:** Split resume content into smaller chunks for efficient retrieval.
- **Embedding Generation:** Convert text chunks into vector representations.
- **Vector Store:** Store and search resume embeddings.
- **Ensemble Retrieval:** Combine retrieval methods to identify relevant candidate information.
- **Job Description Integration:** Use job requirements to retrieve and compare relevant resume content.
- **ATS Score:** Calculate candidate matching scores based on relevant skills and job requirements.
- **Candidate Ranking:** Rank candidates according to their matching scores.
- **Recruitment Assistant:** Use the RAG pipeline to answer queries based on retrieved resume information.
- **Deployment:** Provide a user interface for interacting with the application.

## RAG Pipeline

1. **Document Loading** — Load resumes and extract their text.
2. **Chunking** — Split extracted text into manageable chunks.
3. **Embedding** — Generate vector embeddings for the chunks.
4. **Vector Store** — Index and store embeddings for retrieval.
5. **Ensemble Retrieval** — Combine retrieval approaches to improve relevant information retrieval.
6. **Job Description Processing** — Use the job description to guide candidate searches.
7. **Candidate Matching** — Compare retrieved resume information with job requirements.
8. **ATS Scoring and Ranking** — Calculate matching scores and rank candidates.
9. **RAG Generation** — Pass retrieved context to an LLM to generate grounded responses.
10. **Deployment** — Make the application accessible through its user interface.

## Technology Stack

- **Programming Language:** Python
- **LLM Application Framework:** LangChain
- **Interface:** Streamlit
- **Core Concepts:** RAG, embeddings, vector search, ensemble retrieval, ATS scoring

*Add the exact embedding model, vector database, LLM provider, and deployment platform used in your implementation.*

## Use Cases

- Search resumes using job-specific requirements.
- Identify candidates with relevant skills and experience.
- Compare candidate profiles against a job description.
- Rank candidates for further review.
- Ask questions about retrieved resume information.

## Getting Started

### 1. Clone the Repository

git clone <your-repository-url>
cd <your-repository-folder>

### 2. Create a Virtual Environment

python -m venv venv

Activate it:

**Windows**

venv\Scripts\activate

**macOS/Linux**

source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Configure Environment Variables

Create a `.env` file if your application requires API keys. Add the required variables and keep the file out of version control.

### 5. Run the Application

For a Streamlit application:

streamlit run app.py

## Project Structure

RAG-Based-Resume-Screening/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
└── ...

The final folder structure may vary depending on how the RAG pipeline and supporting modules are organized.

## Important Note

ATS scores are matching estimates, not definitive measures of candidate quality. Recruiters should review the underlying resume evidence and make final decisions with appropriate human oversight.

## Future Improvements

- Improve retrieval relevance and ranking.
- Add resume-grounded explanations for candidate scores.
- Evaluate retrieval quality and answer faithfulness.
- Improve handling of different resume formats.
- Add more robust candidate filtering and comparison features.

## Author

**Harish Alakuntla**

Interested in Data Science, Machine Learning, Generative AI, AI/ML and AI-powered applications.
