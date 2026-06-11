# ── Base image ────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ── Set working directory inside container ────────────────────────────────────
WORKDIR /app

# ── Install system dependencies (pdfplumber/poppler engine layer) ─────────────
RUN apt-get update && apt-get install -y \
    libpoppler-cpp-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# ── Copy requirements first (Layer Caching optimization) ──────────────────────
COPY requirements.txt .

# ── Install Python dependencies ───────────────────────────────────────────────
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy absolute working project contents into container root ────────────────
COPY . /app

# ── Expose Streamlit's target networking socket port ─────────────────────────
EXPOSE 8501

# ── Streamlit container runtime environment parameters ────────────────────────
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501

# ── Launch Application Engine ──────────────────────────────────────────────────
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]