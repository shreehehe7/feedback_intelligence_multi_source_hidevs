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

https://youtu.be/O_1cpURWKdk


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

### 1. Main Dashboard
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/7ea81ccf-521f-48ea-8cff-b79fe566f31f" />

### 2. Sentiment Trends & Visualizations
<img width="1919" height="906" alt="Image" src="https://github.com/user-attachments/assets/b1383349-7077-422b-bf04-ff2f75de70fc" />

### 3. User Reviews Fetched
<img width="1909" height="907" alt="Image" src="https://github.com/user-attachments/assets/152fe218-d300-40c9-8766-71f0eeb6e4fb" />

