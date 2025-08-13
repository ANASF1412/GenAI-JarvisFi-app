"""
Backend module for Personal Finance Chatbot
Contains Watson integration, NLP processing, budget analysis, and demographic adaptation
Enhanced with innovative features: currency conversion, PDF reports, and smart alerts
"""

from .watson_integration import WatsonIntegration
from .budget_analyzer import BudgetAnalyzer
from .demographic_adapter import DemographicAdapter
from .nlp_processor import NLPProcessor
from .currency_converter import CurrencyConverter
from .pdf_generator import FinancialReportGenerator
from .smart_alerts import SmartAlertSystem

__version__ = "1.0.0"
__all__ = [
    "WatsonIntegration", 
    "BudgetAnalyzer", 
    "DemographicAdapter", 
    "NLPProcessor",
    "CurrencyConverter",
    "FinancialReportGenerator",
    "SmartAlertSystem"
]