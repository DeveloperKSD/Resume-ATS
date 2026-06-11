<div align="center">

[![Core Language](https://img.shields.io/badge/RUN_ENGINE-PYTHON_3.11-00FF00?style=for-the-badge&logo=python&logoColor=00FF00&labelColor=000&color=00FF00)](https://www.python.org/)
[![Container Sandbox](https://img.shields.io/badge/SANDBOX-DOCKER_CONTAINER-00FFFF?style=for-the-badge&logo=docker&logoColor=00FFFF&labelColor=000&color=00FFFF)](https://www.docker.com/)
[![UI Module Engine](https://img.shields.io/badge/INTERFACE-STREAMLIT_SHELL-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=FF4B4B&labelColor=000&color=FF4B4B)](https://streamlit.io/)

</div>

# ATS Resume Scanner – Simple Overview

## What is this?
This is a **Streamlit web app** that lets you upload your resume (PDF) and a job description (PDF or text). It then gives you a clear, easy‑to‑read score showing how well your resume matches the job posting, or as a recruiter lets u compsre it to ur job description.
It also reviews standalone resume for job seeker.

## Main Features
- **PDF text extraction** – pulls plain text from both files using **pdfplumber**.
- **Keyword matching** – compares words in the job description with those in your resume.
- **Skill detection** – automatically finds technical skills from a large built‑in skill library.
- **Section detection** – checks if common resume sections (experience, education, projects, etc.) are present.
- **Readability & numbers** – measures how readable the resume is and whether it contains quantifiable metrics.
- **Visual dashboards** – bar chart, radar chart and gauge chart (made with **matplotlib**) show the breakdown of scores.
- **Improvement tips** – suggestions on missing keywords, skills or sections to improve your resume.
- **Retro Windows 95 UI mode** – fun UI that mimics an old Windows 95 desktop.

## How does it work?
1. Upload a **resume PDF** and a **job description PDF**.
2. The app extracts the raw text from each file.
3. Text is pre‑processed (lower‑casing, punctuation removal, stop‑word filter).
4. Several analyses are run:
   - Keyword overlap (35 pts) ✅
   - Skill overlap (25 pts) ✅
   - Cosine similarity (20 pts) ✅
   - TF‑IDF relevance (10 pts) ✅
   - Section presence (10 pts) ✅
5. Scores are summed to a total out of 100 and displayed with graphics.
6. A short report and actionable improvement tips are shown.

## Tech Stack
| Component | Library / Tool | Purpose |
|-----------|----------------|---------|
| Web UI | **Streamlit** | Interactive front‑end |
| PDF parsing | **pdfplumber** | Extract text from PDFs |
| NLP / similarity | **scikit‑learn** (`CountVectorizer`, `TfidfVectorizer`, `cosine_similarity`) | Keyword & vector analysis |
| Data handling | **pandas**, **numpy** | Build tables, maths |
| Charts | **matplotlib** | Bar, radar, gauge, donut charts |
| Containerisation | **Docker** | Run the app anywhere |
| Optional extras | **python‑docx** | Future DOCX support |

## Getting Started (Universal)
### 1. Clone the repository
```bash
# From GitHub
git clone https://github.com/DeveloperKSD/Resume-ATS.git
cd Resume-ATS
```
### 2. Using Docker (recommended for any platform)
```bash
# Build the Docker image
docker build -t ats-resume .

# Run the container
docker run -p 8501:8501 ats-resume
```
Open your browser at `http://localhost:8501`.

### 3. Running locally (Python environment)
```bash

can skip first two steps and skip to installing dependencies
# Create a virtual environment (optional)
python -m venv .venv
# Activate (Windows PowerShell) (optional)
.venv\Scripts\Activate.ps1
# Install dependencies
pip install -r requirements.txt
# Launch the app
streamlit run app.py
or
python -m streamlit run app.py
```
The app will be available at `http://localhost:8501`.

## Usage Tips
- Use PDFs that contain selectable text (not scanned images).
- The more relevant keywords/skills you actually have in the resume, the higher the score.
- Review the *Improvement Tips* section for concrete actions.

## Contributing
Feel free to fork, open issues, or submit pull requests. The code is modular – you can extend the skill list, add new visualisations, or plug in a different NLP model.

---
*Built with love for job‑seekers and recruiters alike.*
