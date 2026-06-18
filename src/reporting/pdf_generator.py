from fpdf import FPDF
import pandas as pd
import os
from datetime import datetime

class ReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Weekly Feedback Intelligence Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(df, trends, top_issues, filters=None, pie_chart_path=None, line_chart_path=None):
    """
    Generates a PDF report summarizing the feedback intelligence and returns bytes.
    """
    pdf = ReportPDF()
    pdf.add_page()
    
    # Filters Section
    if filters:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Filters Applied', 0, 1)
        pdf.set_font('Arial', '', 10)
        for key, value in filters.items():
            pdf.cell(0, 6, f'{key}: {value}', 0, 1)
        pdf.ln(5)
    
    # Overview Section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '1. Overview', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    if df is not None and not df.empty:
        total_reviews = len(df)
        avg_sentiment = df['sentiment_score'].mean() if 'sentiment_score' in df.columns else 0
        positive_count = len(df[df['sentiment_label'] == 'Positive']) if 'sentiment_label' in df.columns else 0
        negative_count = len(df[df['sentiment_label'] == 'Negative']) if 'sentiment_label' in df.columns else 0
        
        pdf.cell(0, 8, f'Total Reviews Analyzed: {total_reviews}', 0, 1)
        pdf.cell(0, 8, f'Average Sentiment Score: {avg_sentiment:.2f} (Scale: -1 to 1)', 0, 1)
        pdf.cell(0, 8, f'Positive Reviews: {positive_count}', 0, 1)
        pdf.cell(0, 8, f'Negative Reviews: {negative_count}', 0, 1)
    else:
        pdf.cell(0, 8, 'No data available.', 0, 1)
        
    pdf.ln(5)
    
    # Top Issues Section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '2. Top Critical Issues (Negative Keywords)', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    if top_issues:
        for word, count in top_issues:
            # Clean up word for latin-1 encoding to prevent FPDF crash on emojis
            safe_word = str(word).encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(0, 8, f'- {safe_word}: mentioned {count} times', 0, 1)
    else:
        pdf.cell(0, 8, 'No critical issues identified.', 0, 1)
        
    pdf.ln(5)
    
    # Visualizations Section
    if pie_chart_path or line_chart_path:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, '3. Visualizations', 0, 1)
        pdf.ln(5)
        
        if pie_chart_path:
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 10, 'Sentiment Distribution', 0, 1)
            pdf.image(pie_chart_path, x=15, w=160)
            pdf.ln(10)
            
        if line_chart_path:
            if pdf.get_y() > 150:
                pdf.add_page()
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 10, 'Sentiment Trend Over Time', 0, 1)
            pdf.image(line_chart_path, x=15, w=160)

    # Return the PDF as bytes
    return pdf.output()
