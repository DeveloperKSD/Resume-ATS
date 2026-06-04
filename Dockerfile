# ── Base image ────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ── Set working directory inside container ────────────────────────────────────
WORKDIR /app

# ── Install system dependencies (pdfplumber needs these) ─────────────────────
RUN apt-get update && apt-get install -y \
    libpoppler-cpp-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# ── Copy requirements first (layer caching — faster rebuilds) ─────────────────
COPY requirements.txt .

# ── Install Python dependencies ───────────────────────────────────────────────
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy project files ────────────────────────────────────────────────────────
COPY scanner.py .
COPY charts.py  .
COPY app.py     .

# ── Expose Streamlit's default port ───────────────────────────────────────────
EXPOSE 8501

# ── Streamlit config: disable browser auto-open (needed in containers) ────────
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501

# ── Run the app ───────────────────────────────────────────────────────────────
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
