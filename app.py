import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64
import os

from src.ingestion.play_store import fetch_play_store_reviews
from src.ingestion.app_store import fetch_app_store_reviews
from src.ingestion.csv_import import parse_csv_reviews
from src.processing.sentiment import analyze_sentiment
from src.processing.analyzer import get_trend_summary, identify_critical_issues, prioritize_feedback
from src.reporting.pdf_generator import generate_pdf_report

st.set_page_config(page_title="Feedback Intelligence", page_icon="📊", layout="wide")

st.title("Multi-Source Feedback Intelligence System")

# Initialize session state for data
if 'feedback_data' not in st.session_state:
    st.session_state.feedback_data = pd.DataFrame()

# --- Sidebar Controls ---
st.sidebar.header("Data Sources")

# Google Play
with st.sidebar.expander("Google Play Store"):
    play_app_id = st.text_input("App ID (Play Store)", value="com.whatsapp")
    if st.button("Fetch Play Store"):
        with st.spinner("Fetching Google Play reviews..."):
            df_play = fetch_play_store_reviews(play_app_id, count=100)
            if not df_play.empty:
                df_play = analyze_sentiment(df_play)
                st.session_state.feedback_data = pd.concat([st.session_state.feedback_data, df_play]).drop_duplicates(subset=['id'])
                st.success(f"Fetched {len(df_play)} reviews!")
            else:
                st.error("Failed to fetch reviews or none found.")

# App Store
with st.sidebar.expander("Apple App Store"):
    ios_app_id = st.text_input("App ID (App Store)", value="310633997")
    if st.button("Fetch App Store"):
        with st.spinner("Fetching App Store reviews..."):
            df_ios = fetch_app_store_reviews(ios_app_id, count=100)
            if not df_ios.empty:
                df_ios = analyze_sentiment(df_ios)
                st.session_state.feedback_data = pd.concat([st.session_state.feedback_data, df_ios]).drop_duplicates(subset=['id'])
                st.success(f"Fetched {len(df_ios)} reviews!")
            else:
                st.error("Failed to fetch reviews or none found.")

# CSV Upload
with st.sidebar.expander("Upload CSV"):
    uploaded_file = st.file_uploader("Choose a CSV file")
    if uploaded_file is not None:
        if st.button("Process CSV"):
            with st.spinner("Processing CSV..."):
                df_csv = parse_csv_reviews(uploaded_file.getvalue())
                if not df_csv.empty:
                    df_csv = analyze_sentiment(df_csv)
                    st.session_state.feedback_data = pd.concat([st.session_state.feedback_data, df_csv]).drop_duplicates(subset=['id'])
                    st.success(f"Processed {len(df_csv)} reviews!")
                else:
                    st.error("Failed to parse CSV.")

if st.sidebar.button("Clear All Data"):
    st.session_state.feedback_data = pd.DataFrame()
    st.rerun()

# --- Main Dashboard ---
if st.session_state.feedback_data.empty:
    st.info("No data available. Please fetch or upload reviews from the sidebar.")
else:
    df = st.session_state.feedback_data.copy()
    
    # Filters
    st.subheader("Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sources = df['source'].unique().tolist()
        selected_sources = st.multiselect("Source", options=sources, default=sources)
        
    with col2:
        sentiments = df['sentiment_label'].unique().tolist()
        selected_sentiments = st.multiselect("Sentiment", options=sentiments, default=sentiments)
        
    with col3:
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], utc=True).dt.tz_localize(None)
            min_date = df['date'].min().date()
            max_date = df['date'].max().date()
            date_range = st.date_input("Date Range", [min_date, max_date])
        else:
            date_range = []

    # Apply filters
    filtered_df = df[df['source'].isin(selected_sources) & df['sentiment_label'].isin(selected_sentiments)]
    if len(date_range) == 2:
        start_date, end_date = date_range
        # Convert date column to date for comparison
        date_series = pd.to_datetime(filtered_df['date']).dt.date
        filtered_df = filtered_df[(date_series >= start_date) & (date_series <= end_date)]
        
    st.markdown("---")
    
    # KPIs
    st.subheader("Overview")
    kpi1, kpi2, kpi3 = st.columns(3)
    
    kpi1.metric("Total Reviews", len(filtered_df))
    avg_score = filtered_df['sentiment_score'].mean() if not filtered_df.empty else 0
    kpi2.metric("Average Sentiment", f"{avg_score:.2f}")
    
    if not filtered_df.empty:
        top_source = filtered_df['source'].value_counts().index[0]
        kpi3.metric("Top Source", top_source)
    else:
        kpi3.metric("Top Source", "N/A")
        
    st.markdown("---")
    
    # Charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Sentiment Distribution")
        if not filtered_df.empty:
            sentiment_counts = filtered_df['sentiment_label'].value_counts().reset_index()
            sentiment_counts.columns = ['Sentiment', 'Count']
            fig_pie = px.pie(sentiment_counts, values='Count', names='Sentiment', color='Sentiment',
                             color_discrete_map={'Positive':'#00CC96', 'Neutral':'#636EFA', 'Negative':'#EF553B'})
            st.plotly_chart(fig_pie, use_container_width=True)
            # Save for PDF
            os.makedirs("data", exist_ok=True)
            fig_pie.write_image("data/pie.png", width=500, height=350)
            
    with chart_col2:
        st.subheader("Sentiment Trend Over Time")
        if not filtered_df.empty and 'date' in filtered_df.columns:
            trend_df = get_trend_summary(filtered_df)
            if not trend_df.empty:
                fig_line = px.line(trend_df, x='date_only', y='sentiment_score', title='Average Daily Sentiment Score', markers=True)
                st.plotly_chart(fig_line, use_container_width=True)
                # Save for PDF
                os.makedirs("data", exist_ok=True)
                fig_line.write_image("data/line.png", width=700, height=350)
                
    st.markdown("---")
    
    # Critical Issues
    st.subheader("Critical Issues")
    top_issues = identify_critical_issues(filtered_df, top_n=10)
    
    if top_issues:
        st.write("Most frequent terms in negative reviews:")
        issue_df = pd.DataFrame(top_issues, columns=['Keyword', 'Frequency'])
        st.dataframe(issue_df, hide_index=True)
    else:
        st.info("No critical issues found in the current selection.")
        
    st.markdown("---")
    
    # Prioritized Feedback
    st.subheader("Recent & Prioritized Feedback")
    priority_df = prioritize_feedback(filtered_df)
    st.dataframe(priority_df[['date', 'source', 'rating', 'sentiment_label', 'sentiment_score', 'review_text']], hide_index=True, use_container_width=True)
    
    # Reporting
    st.markdown("---")
    st.subheader("Reporting")
    
    filters = {
        "Sources": ", ".join(selected_sources) if selected_sources else "All",
        "Sentiments": ", ".join(selected_sentiments) if selected_sentiments else "All",
        "Date Range": f"{start_date} to {end_date}" if len(date_range) == 2 else "All Time"
    }

    pie_chart_path = "data/pie.png" if not filtered_df.empty and os.path.exists("data/pie.png") else None
    line_chart_path = "data/line.png" if not filtered_df.empty and os.path.exists("data/line.png") else None
    
    pdf_bytes = generate_pdf_report(filtered_df, get_trend_summary(filtered_df), top_issues, filters=filters, pie_chart_path=pie_chart_path, line_chart_path=line_chart_path)
    
    # Use HTML base64 approach to force browser download and guarantee filename
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="feedback_report.pdf" style="display: inline-block; padding: 0.5em 1em; color: white; background-color: #FF4B4B; border-radius: 4px; text-decoration: none; font-weight: bold;">Download PDF Report</a>'
    st.markdown(href, unsafe_allow_html=True)
