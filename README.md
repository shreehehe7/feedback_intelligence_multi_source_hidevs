# Multi-Source Feedback Intelligence System 

A robust, real-time dashboard built with Streamlit that aggregates user feedback from the **Google Play Store**, **Apple App Store**, and custom **CSV files**. The system utilizes Natural Language Processing (NLP) to analyze sentiment, detect trends, and identify critical issues automatically, allowing product teams to generate professional weekly PDF reports with a single click.

---

##  Features
- **Multi-Source Ingestion**: Live fetching from Google Play Store (`google-play-scraper`) and Apple App Store (RSS Feeds), alongside CSV uploads.
- **Sentiment Analysis**: Automatic labeling (Positive, Neutral, Negative) and compound scoring using `vaderSentiment`.
- **Trend Detection & KPI Tracking**: Interactive Plotly charts visualizing sentiment distributions and daily trends over time.
- **Issue Prioritization**: NLP-driven extraction of the most frequent keywords specifically from negative reviews to flag urgent bugs or user complaints.
- **Automated PDF Reporting**: Generates a professional weekly summary report (complete with embedded pie and line charts) using `fpdf2` and `kaleido`.

---

##  Project Demo Video

[![Watch the Demo on YouTube](https://img.shields.io/badge/YouTube-Watch_Video-red?style=for-the-badge&logo=youtube)](YOUR_YOUTUBE_LINK_HERE)

*(Insert your YouTube video link above)*

---

##  Setup & Installation Guide

### Prerequisites
- Python 3.9+
- pip (Python Package Installer)

### 1. Clone the Repository
```bash
git clone https://github.com/shreeyadav06/feedback_intelligence_multi_source_hidevs.git
cd feedback_intelligence_multi_source_hidevs
```

### 2. Create and Activate a Virtual Environment
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```
The dashboard will automatically open in your browser at `http://localhost:8501`.

---

##  API Setup Instructions
This project is designed to be plug-and-play and **does not require any paid API keys**:
- **Google Play Store**: Uses the open-source `google-play-scraper` package to bypass API limits.
- **Apple App Store**: Fetches data directly via Apple's public iTunes RSS feeds using the `requests` library.
- **NLP Engine**: Uses local `vaderSentiment`, requiring no external API calls to OpenAI or Google Cloud.

---

##  Screenshots


### 1. Main Dashboard & Data Ingestion
![Dashboard Overview](screenshots/dashboard.png)

### 2. Sentiment Trends & Visualizations
![Charts](screenshots/charts.png)

### 3. Generated PDF Report
![PDF Report](screenshots/pdf_report.png)

