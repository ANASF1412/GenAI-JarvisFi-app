"""
Advanced PDF Report Generator for Financial Analysis
Creates comprehensive, professional financial reports
"""

from fpdf import FPDF
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd
from typing import Dict, List, Optional
import base64
import io
import logging

class FinancialReportGenerator:
    """
    Generate comprehensive PDF reports for financial analysis
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def generate_comprehensive_report(self, 
                                    user_profile: Dict, 
                                    budget_analysis: Dict, 
                                    transactions_df: pd.DataFrame) -> bytes:
        """
        Generate a comprehensive financial report as PDF
        """
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        self._add_header(pdf, user_profile)
        
        # Executive Summary
        self._add_executive_summary(pdf, budget_analysis)
        
        # Detailed Analysis
        self._add_detailed_analysis(pdf, budget_analysis)
        
        # Recommendations
        self._add_recommendations(pdf, budget_analysis, user_profile)
        
        # Charts and Graphs
        self._add_charts_section(pdf, budget_analysis, transactions_df)
        
        # Footer
        self._add_footer(pdf)
        
        return pdf.output(dest='S').encode('latin1')
    
    def _add_header(self, pdf: FPDF, user_profile: Dict):
        """Add professional header to the report"""
        # Logo space (can be customized)
        pdf.set_font("Arial", size=24, style='B')
        pdf.set_text_color(0, 51, 102)  # Professional blue
        pdf.cell(0, 15, "Personal Finance Analysis Report", ln=True, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(100, 100, 100)  # Gray
        pdf.cell(0, 8, f"Generated on {datetime.now().strftime('%B %d, %Y')}", ln=True, align='C')
        
        # User Information
        pdf.ln(10)
        pdf.set_font("Arial", size=14, style='B')
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, "Client Information", ln=True)
        
        pdf.set_font("Arial", size=11)
        pdf.cell(0, 6, f"Name: {user_profile.get('name', 'User')}", ln=True)
        pdf.cell(0, 6, f"Profile Type: {user_profile.get('demographic', 'Professional').title()}", ln=True)
        pdf.cell(0, 6, f"Monthly Income: ₹{user_profile.get('monthly_income', 0):,}", ln=True)
        pdf.ln(5)
    
    def _add_executive_summary(self, pdf: FPDF, budget_analysis: Dict):
        """Add executive summary section"""
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(0, 8, "Executive Summary", ln=True)
        pdf.set_font("Arial", size=11)
        
        summary = budget_analysis.get('summary', {})
        health = budget_analysis.get('budget_health', {})
        
        # Key metrics in a structured format
        pdf.cell(0, 6, f"• Total Income: ₹{summary.get('total_income', 0):,.2f}", ln=True)
        pdf.cell(0, 6, f"• Total Expenses: ₹{summary.get('total_spent', 0):,.2f}", ln=True)
        pdf.cell(0, 6, f"• Net Savings: ₹{summary.get('net_savings', 0):,.2f}", ln=True)
        pdf.cell(0, 6, f"• Savings Rate: {summary.get('savings_rate', 0):.1f}%", ln=True)
        pdf.cell(0, 6, f"• Financial Health Score: {health.get('score', 0)}/100 ({health.get('status', 'N/A')})", ln=True)
        pdf.ln(5)
    
    def _add_detailed_analysis(self, pdf: FPDF, budget_analysis: Dict):
        """Add detailed financial analysis"""
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(0, 8, "Detailed Analysis", ln=True)
        
        # Category Breakdown
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(0, 6, "Spending by Category:", ln=True)
        pdf.set_font("Arial", size=10)
        
        categories = budget_analysis.get('category_breakdown', {}).get('by_category', {})
        for category, amount in list(categories.items())[:8]:  # Top 8 categories
            percentage = (amount / budget_analysis.get('summary', {}).get('total_spent', 1)) * 100
            pdf.cell(0, 5, f"  • {category.title()}: ₹{amount:,.0f} ({percentage:.1f}%)", ln=True)
        
        pdf.ln(3)
        
        # Trends Analysis
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(0, 6, "Spending Trends:", ln=True)
        pdf.set_font("Arial", size=10)
        
        trends = budget_analysis.get('trends', {})
        pdf.cell(0, 5, f"  • Trend Direction: {trends.get('trend_direction', 'Stable').title()}", ln=True)
        pdf.cell(0, 5, f"  • Change: {trends.get('trend_percentage', 0):+.1f}%", ln=True)
        pdf.ln(5)
    
    def _add_recommendations(self, pdf: FPDF, budget_analysis: Dict, user_profile: Dict):
        """Add personalized recommendations"""
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(0, 8, "Personalized Recommendations", ln=True)
        pdf.set_font("Arial", size=11)
        
        recommendations = budget_analysis.get('recommendations', [])
        for i, rec in enumerate(recommendations[:6], 1):  # Top 6 recommendations
            # Handle text wrapping for long recommendations
            words = rec.split(' ')
            line = ""
            for word in words:
                if len(line + word) < 80:
                    line += word + " "
                else:
                    pdf.cell(0, 5, f"  {i}. {line.strip()}", ln=True)
                    line = "     " + word + " "
                    i = ""  # Don't repeat the number
            if line.strip():
                pdf.cell(0, 5, f"  {i if i else ''}{line.strip()}", ln=True)
            pdf.ln(2)
    
    def _add_charts_section(self, pdf: FPDF, budget_analysis: Dict, transactions_df: pd.DataFrame):
        """Add charts and visualizations (placeholder for future implementation)"""
        pdf.add_page()
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(0, 8, "Visual Analysis", ln=True)
        pdf.set_font("Arial", size=11)
        
        # Placeholder for charts
        pdf.cell(0, 6, "📊 Spending Distribution Chart", ln=True)
        pdf.cell(0, 6, "📈 Monthly Spending Trends", ln=True)
        pdf.cell(0, 6, "💰 Income vs Expenses Comparison", ln=True)
        pdf.cell(0, 6, "🎯 Financial Goals Progress", ln=True)
        pdf.ln(10)
        
        # Note about charts
        pdf.set_font("Arial", size=9, style='I')
        pdf.cell(0, 5, "Note: Interactive charts are available in the web dashboard.", ln=True)
    
    def _add_footer(self, pdf: FPDF):
        """Add professional footer"""
        pdf.ln(20)
        pdf.set_font("Arial", size=8)
        pdf.set_text_color(128, 128, 128)
        
        footer_text = (
            "This report is generated by your Personal Finance AI Assistant. "
            "The recommendations are based on your transaction data and profile. "
            "Please consult with a qualified financial advisor for major financial decisions."
        )
        
        # Word wrap for footer
        words = footer_text.split()
        line = ""
        for word in words:
            if len(line + word) < 90:
                line += word + " "
            else:
                pdf.cell(0, 4, line.strip(), ln=True, align='C')
                line = word + " "
        if line.strip():
            pdf.cell(0, 4, line.strip(), ln=True, align='C')
        
        pdf.ln(5)
        pdf.cell(0, 4, f"Generated by Personal Finance AI • {datetime.now().year}", ln=True, align='C')
    
    def create_quick_summary_report(self, user_profile: Dict, budget_analysis: Dict) -> bytes:
        """Create a quick 1-page summary report"""
        pdf = FPDF()
        pdf.add_page()
        
        # Quick header
        pdf.set_font("Arial", size=18, style='B')
        pdf.cell(0, 12, "Financial Summary Report", ln=True, align='C')
        
        pdf.set_font("Arial", size=11)
        pdf.cell(0, 6, f"For: {user_profile.get('name', 'User')} | {datetime.now().strftime('%B %Y')}", ln=True, align='C')
        pdf.ln(8)
        
        # Key metrics in boxes
        summary = budget_analysis.get('summary', {})
        health = budget_analysis.get('budget_health', {})
        
        # Create metric boxes
        metrics = [
            ("Monthly Income", f"₹{summary.get('total_income', 0):,.0f}"),
            ("Total Expenses", f"₹{summary.get('total_spent', 0):,.0f}"),
            ("Net Savings", f"₹{summary.get('net_savings', 0):,.0f}"),
            ("Savings Rate", f"{summary.get('savings_rate', 0):.1f}%"),
            ("Health Score", f"{health.get('score', 0)}/100"),
            ("Status", health.get('status', 'N/A'))
        ]
        
        for i, (label, value) in enumerate(metrics):
            if i % 2 == 0:
                x_pos = 20
            else:
                x_pos = 110
            
            y_pos = 50 + (i // 2) * 25
            
            pdf.set_xy(x_pos, y_pos)
            pdf.cell(80, 20, "", border=1)
            pdf.set_xy(x_pos + 2, y_pos + 3)
            pdf.set_font("Arial", size=9, style='B')
            pdf.cell(0, 5, label, ln=True)
            pdf.set_xy(x_pos + 2, y_pos + 10)
            pdf.set_font("Arial", size=12, style='B')
            pdf.cell(0, 5, value, ln=True)
        
        return pdf.output(dest='S').encode('latin1')