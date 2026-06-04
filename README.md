# 📄 ATS Resume Scanner

An interactive, high-fidelity **ATS (Applicant Tracking System) Resume Scanner** built with Python and Streamlit. It extracts text from a candidate's resume and a target job description, analyzes them using Natural Language Processing (NLP) techniques, calculates a comprehensive compatibility score, and displays visually stunning dashboards and charts along with actionable feedback.

---

## 🚀 Features

* **High-Accuracy PDF Parsing**: Uses `pdfplumber` to extract clean text from resumes and job descriptions.
* **Granular ATS Scoring (out of 100)**:
  * **Keyword Match (35 pts)**: Compares matching key terms.
  * **Skills Match (25 pts)**: Identifies specific technology skills matching a built-in library of top industry terms.
  * **Cosine Similarity (20 pts)**: Performs vocabulary overlap analysis using a Count Vectorizer.
  * **TF-IDF Relevance (10 pts)**: Computes weighted importance of key matching words relative to the overall document.
  * **Section Presence (10 pts)**: Scans for critical resume parts (*experience, education, skills, contact, summary, projects, certifications*).
* **Premium Interactive Dashboards**:
  * **Score Gauge**: Visual pointer showing the match percentage category (Poor, Moderate, Good, Excellent).
  * **Radar Chart**: Interactive spider chart mapping the strengths/weaknesses across all five categories.
  * **Score Breakdown Bar Chart**: Clear horizontal bar comparison of points scored vs maximum possible points.
* **Actionable Resume Optimization Tips**: Tailored list of recommendations to improve the resume (e.g., missing keywords to add, missing sections to write, and language mirroring hints).

---

## 🛠️ Tech Stack

* **Frontend & Dashboard**: [Streamlit](https://streamlit.io/)
* **NLP & Text Analysis**: `scikit-learn` (`CountVectorizer`, `TfidfVectorizer`, `cosine_similarity`)
* **PDF Parsing**: `pdfplumber`
* **Visualization**: `Matplotlib` (using headless `Agg` backend)
* **Data Processing**: `Pandas`, `NumPy`
* **Containerization**: `Docker`

---

## 📁 Repository Structure

```
├── app.py                  # Streamlit dashboard layout and frontend elements
├── scanner.py              # Core NLP processing and scoring math
├── charts.py               # Matplotlib gauge, radar, and bar chart generator
├── requirements.txt        # Python package dependencies
├── Dockerfile              # Containerization steps
└── ATS_Scanner_Colab.ipynb # Google Colab Jupyter Notebook implementation
```

---

## ⚙️ Setup and Installation

### Running Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/DeveloperKSD/Resume-ATS.git
   cd Resume-ATS
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```
   *The application will launch automatically in your default browser at `http://localhost:8501`.*

---

## 🐳 Docker Deployment

To build and run the application inside a lightweight container:

1. **Build the Docker Image**:
   ```bash
   docker build -t resume-ats .
   ```

2. **Run the Docker Container**:
   ```bash
   docker run -d -p 8501:8501 resume-ats
   ```

3. **Access the Application**:
   Open your browser and navigate to `http://localhost:8501`.
