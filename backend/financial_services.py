"""
Comprehensive Financial Services for JarvisFi
Includes credit score tracking, debt management, investment analysis, and farmer-specific tools
"""

import os
import json
import logging
import asyncio
import requests
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# External API integrations
import yfinance as yf
from forex_python.converter import CurrencyRates, CurrencyConverter

class FinancialServices:
    """
    Comprehensive financial services including credit scoring, investments, and specialized tools
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_api_clients()
        self.setup_financial_data()
        
        # Currency converter
        self.currency_converter = CurrencyConverter()
        self.currency_rates = CurrencyRates()
        
        # Financial constants
        self.FINANCIAL_CONSTANTS = {
            'emergency_fund_months': 6,
            'retirement_corpus_multiplier': 25,
            'sip_recommended_percentage': 0.15,
            'tax_saving_limit_80c': 150000,
            'home_loan_emi_ratio': 0.40,
            'credit_utilization_ideal': 0.30
        }
    
    def setup_api_clients(self):
        """Initialize external API clients"""
        try:
            # Credit score API configuration
            self.credit_apis = {
                'cibil': {
                    'base_url': 'https://api.cibil.com/v1',
                    'api_key': os.getenv('CIBIL_API_KEY'),
                    'enabled': bool(os.getenv('CIBIL_API_KEY'))
                },
                'experian': {
                    'base_url': 'https://api.experian.com/v1',
                    'api_key': os.getenv('EXPERIAN_API_KEY'),
                    'enabled': bool(os.getenv('EXPERIAN_API_KEY'))
                }
            }
            
            # Currency API
            self.currency_api = {
                'xe': {
                    'base_url': 'https://xecdapi.xe.com/v1',
                    'api_key': os.getenv('XE_API_KEY'),
                    'enabled': bool(os.getenv('XE_API_KEY'))
                }
            }
            
            # Government APIs
            self.govt_apis = {
                'rbi': {
                    'base_url': 'https://rbi.org.in/api/v1',
                    'enabled': True
                },
                'sebi': {
                    'base_url': 'https://sebi.gov.in/api/v1',
                    'enabled': True
                }
            }
            
            self.logger.info("✅ API clients initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Error setting up API clients: {e}")
    
    def setup_financial_data(self):
        """Initialize financial data and market information"""
        try:
            # MSP data for farmers
            self.msp_data = {
                'rice': {'price': 2183, 'unit': 'quintal', 'season': 'kharif'},
                'wheat': {'price': 2275, 'unit': 'quintal', 'season': 'rabi'},
                'cotton': {'price': 6620, 'unit': 'quintal', 'season': 'kharif'},
                'sugarcane': {'price': 315, 'unit': 'quintal', 'season': 'annual'},
                'maize': {'price': 2090, 'unit': 'quintal', 'season': 'kharif'},
                'bajra': {'price': 2500, 'unit': 'quintal', 'season': 'kharif'},
                'jowar': {'price': 3180, 'unit': 'quintal', 'season': 'kharif'},
                'tur': {'price': 7000, 'unit': 'quintal', 'season': 'kharif'}
            }
            
            # Government subsidies
            self.subsidies = {
                'pm_kisan': {
                    'amount': 6000,
                    'frequency': 'annual',
                    'eligibility': 'small_marginal_farmers',
                    'description': 'Direct income support to farmers'
                },
                'fertilizer_subsidy': {
                    'amount': 'variable',
                    'frequency': 'per_purchase',
                    'eligibility': 'all_farmers',
                    'description': 'Subsidy on fertilizer purchases'
                },
                'crop_insurance': {
                    'amount': 'premium_based',
                    'frequency': 'seasonal',
                    'eligibility': 'insured_farmers',
                    'description': 'Pradhan Mantri Fasal Bima Yojana'
                }
            }
            
            # Tax brackets (FY 2024-25)
            self.tax_brackets = {
                'old_regime': [
                    {'min': 0, 'max': 250000, 'rate': 0},
                    {'min': 250000, 'max': 500000, 'rate': 0.05},
                    {'min': 500000, 'max': 1000000, 'rate': 0.20},
                    {'min': 1000000, 'max': float('inf'), 'rate': 0.30}
                ],
                'new_regime': [
                    {'min': 0, 'max': 300000, 'rate': 0},
                    {'min': 300000, 'max': 600000, 'rate': 0.05},
                    {'min': 600000, 'max': 900000, 'rate': 0.10},
                    {'min': 900000, 'max': 1200000, 'rate': 0.15},
                    {'min': 1200000, 'max': 1500000, 'rate': 0.20},
                    {'min': 1500000, 'max': float('inf'), 'rate': 0.30}
                ]
            }
            
            self.logger.info("✅ Financial data initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Error setting up financial data: {e}")
    
    async def get_credit_score(self, user_id: str, pan_number: str) -> Dict[str, Any]:
        """Get credit score from CIBIL/Experian APIs"""
        try:
            credit_data = {
                'user_id': user_id,
                'timestamp': datetime.now().isoformat(),
                'sources': []
            }
            
            # Try CIBIL first
            if self.credit_apis['cibil']['enabled']:
                try:
                    cibil_score = await self.fetch_cibil_score(pan_number)
                    credit_data.update(cibil_score)
                    credit_data['sources'].append('CIBIL')
                except Exception as e:
                    self.logger.warning(f"CIBIL API error: {e}")
            
            # Fallback to Experian
            if not credit_data.get('score') and self.credit_apis['experian']['enabled']:
                try:
                    experian_score = await self.fetch_experian_score(pan_number)
                    credit_data.update(experian_score)
                    credit_data['sources'].append('Experian')
                except Exception as e:
                    self.logger.warning(f"Experian API error: {e}")
            
            # Generate mock data if APIs unavailable
            if not credit_data.get('score'):
                credit_data = self.generate_mock_credit_score(user_id)
            
            # Add recommendations
            credit_data['recommendations'] = self.get_credit_recommendations(credit_data['score'])
            
            return credit_data
            
        except Exception as e:
            self.logger.error(f"❌ Error fetching credit score: {e}")
            return self.generate_mock_credit_score(user_id)
    
    def generate_mock_credit_score(self, user_id: str) -> Dict[str, Any]:
        """Generate realistic mock credit score data"""
        import random
        
        # Generate score based on user_id hash for consistency
        hash_val = hash(user_id) % 1000
        base_score = 650 + (hash_val % 200)  # Score between 650-850
        
        return {
            'score': base_score,
            'range': self.get_credit_range(base_score),
            'factors': {
                'payment_history': random.randint(70, 95),
                'credit_utilization': random.randint(60, 90),
                'credit_age': random.randint(50, 85),
                'credit_mix': random.randint(65, 85),
                'new_credit': random.randint(70, 90)
            },
            'last_updated': datetime.now().isoformat(),
            'sources': ['Mock Data'],
            'trend': random.choice(['improving', 'stable', 'declining'])
        }
    
    def get_credit_range(self, score: int) -> str:
        """Get credit score range description"""
        if score >= 800:
            return 'Excellent'
        elif score >= 750:
            return 'Very Good'
        elif score >= 700:
            return 'Good'
        elif score >= 650:
            return 'Fair'
        else:
            return 'Poor'
    
    def get_credit_recommendations(self, score: int) -> List[str]:
        """Get personalized credit improvement recommendations"""
        recommendations = []
        
        if score < 650:
            recommendations.extend([
                "Pay all bills on time to improve payment history",
                "Reduce credit card balances to below 30% of limit",
                "Don't close old credit cards - keep credit history long",
                "Avoid applying for new credit frequently"
            ])
        elif score < 750:
            recommendations.extend([
                "Maintain low credit utilization (below 10%)",
                "Consider a credit mix with different types of loans",
                "Monitor credit report regularly for errors",
                "Pay more than minimum amounts on credit cards"
            ])
        else:
            recommendations.extend([
                "Excellent credit! Maintain current habits",
                "You qualify for the best interest rates",
                "Consider premium credit cards with rewards",
                "Help family members improve their credit"
            ])
        
        return recommendations
    
    async def analyze_debt_management(self, user_profile: Dict) -> Dict[str, Any]:
        """Comprehensive debt analysis and restructuring recommendations"""
        try:
            financial_data = user_profile.get('financial_profile', {})
            debt_info = financial_data.get('debt_info', {})
            monthly_income = user_profile.get('basic_info', {}).get('monthly_income', 30000)
            
            # Calculate debt metrics
            total_debt = sum(debt_info.values()) if debt_info else 0
            debt_to_income_ratio = (total_debt / (monthly_income * 12)) if monthly_income > 0 else 0
            
            # Debt categorization
            debt_analysis = {
                'total_debt': total_debt,
                'debt_to_income_ratio': debt_to_income_ratio,
                'risk_level': self.assess_debt_risk(debt_to_income_ratio),
                'monthly_income': monthly_income,
                'recommendations': []
            }
            
            # Generate recommendations based on debt level
            if debt_to_income_ratio > 0.4:
                debt_analysis['recommendations'].extend([
                    "🚨 High debt-to-income ratio - consider debt consolidation",
                    "💡 Prioritize high-interest debt (credit cards) first",
                    "📞 Contact lenders to negotiate payment plans",
                    "💰 Consider increasing income through side jobs"
                ])
            elif debt_to_income_ratio > 0.2:
                debt_analysis['recommendations'].extend([
                    "⚠️ Moderate debt level - create structured repayment plan",
                    "🎯 Use debt avalanche method (highest interest first)",
                    "💳 Avoid taking new debt until current debt reduces",
                    "📊 Track progress monthly"
                ])
            else:
                debt_analysis['recommendations'].extend([
                    "✅ Healthy debt level - maintain current payments",
                    "🏦 Consider prepaying loans to save interest",
                    "💰 Build emergency fund alongside debt payments",
                    "📈 Start investing surplus funds"
                ])
            
            # Debt restructuring options
            debt_analysis['restructuring_options'] = self.get_restructuring_options(debt_info, monthly_income)
            
            return debt_analysis
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing debt: {e}")
            return {'error': 'Unable to analyze debt', 'recommendations': []}
    
    def assess_debt_risk(self, debt_ratio: float) -> str:
        """Assess debt risk level"""
        if debt_ratio > 0.4:
            return 'High Risk'
        elif debt_ratio > 0.2:
            return 'Moderate Risk'
        else:
            return 'Low Risk'
    
    def get_restructuring_options(self, debt_info: Dict, monthly_income: int) -> List[Dict]:
        """Get debt restructuring options"""
        options = []
        
        if debt_info:
            # Debt consolidation option
            options.append({
                'type': 'Debt Consolidation',
                'description': 'Combine all debts into single loan with lower interest',
                'pros': ['Single EMI', 'Lower interest rate', 'Simplified tracking'],
                'cons': ['May extend repayment period', 'Requires good credit score'],
                'eligibility': 'Credit score > 650'
            })
            
            # Balance transfer option
            options.append({
                'type': 'Balance Transfer',
                'description': 'Transfer high-interest debt to lower-interest cards',
                'pros': ['0% intro APR offers', 'Lower monthly payments'],
                'cons': ['Transfer fees', 'Temporary benefit'],
                'eligibility': 'Good payment history'
            })
            
            # EMI restructuring
            options.append({
                'type': 'EMI Restructuring',
                'description': 'Negotiate with lenders for extended payment terms',
                'pros': ['Lower monthly EMI', 'Avoid default'],
                'cons': ['Higher total interest', 'Credit score impact'],
                'eligibility': 'Financial hardship proof'
            })
        
        return options
    
    async def get_investment_recommendations(self, user_profile: Dict) -> Dict[str, Any]:
        """Generate personalized investment recommendations"""
        try:
            basic_info = user_profile.get('basic_info', {})
            financial_profile = user_profile.get('financial_profile', {})
            
            monthly_income = basic_info.get('monthly_income', 30000)
            age = basic_info.get('age', 25)
            user_type = basic_info.get('user_type', 'professional')
            risk_tolerance = financial_profile.get('risk_tolerance', 'moderate')
            
            # Calculate investment capacity
            recommended_sip = int(monthly_income * self.FINANCIAL_CONSTANTS['sip_recommended_percentage'])
            
            # Age-based asset allocation
            equity_percentage = min(100 - age, 80)  # 100 minus age rule, max 80%
            debt_percentage = 100 - equity_percentage
            
            recommendations = {
                'monthly_investment_capacity': recommended_sip,
                'asset_allocation': {
                    'equity': equity_percentage,
                    'debt': debt_percentage
                },
                'recommended_funds': [],
                'tax_saving_options': [],
                'user_type_specific': []
            }
            
            # Mutual fund recommendations based on risk profile
            if risk_tolerance == 'aggressive':
                recommendations['recommended_funds'] = [
                    {'name': 'Large Cap Equity Fund', 'allocation': 40, 'risk': 'Medium'},
                    {'name': 'Mid Cap Equity Fund', 'allocation': 30, 'risk': 'High'},
                    {'name': 'Small Cap Equity Fund', 'allocation': 20, 'risk': 'Very High'},
                    {'name': 'Debt Fund', 'allocation': 10, 'risk': 'Low'}
                ]
            elif risk_tolerance == 'moderate':
                recommendations['recommended_funds'] = [
                    {'name': 'Large Cap Equity Fund', 'allocation': 50, 'risk': 'Medium'},
                    {'name': 'Mid Cap Equity Fund', 'allocation': 20, 'risk': 'High'},
                    {'name': 'Hybrid Fund', 'allocation': 20, 'risk': 'Medium'},
                    {'name': 'Debt Fund', 'allocation': 10, 'risk': 'Low'}
                ]
            else:  # conservative
                recommendations['recommended_funds'] = [
                    {'name': 'Large Cap Equity Fund', 'allocation': 30, 'risk': 'Medium'},
                    {'name': 'Hybrid Fund', 'allocation': 40, 'risk': 'Medium'},
                    {'name': 'Debt Fund', 'allocation': 20, 'risk': 'Low'},
                    {'name': 'Fixed Deposits', 'allocation': 10, 'risk': 'Very Low'}
                ]
            
            # Tax saving recommendations
            recommendations['tax_saving_options'] = [
                {'instrument': 'ELSS Mutual Funds', 'limit': 150000, 'lock_in': '3 years', 'returns': '12-15%'},
                {'instrument': 'PPF', 'limit': 150000, 'lock_in': '15 years', 'returns': '7-8%'},
                {'instrument': 'NSC', 'limit': 150000, 'lock_in': '5 years', 'returns': '6-7%'},
                {'instrument': 'Life Insurance', 'limit': 150000, 'lock_in': 'Policy term', 'returns': 'Variable'}
            ]
            
            # User type specific recommendations
            if user_type == 'student':
                recommendations['user_type_specific'] = [
                    "Start with small SIPs (₹500-1000) to build habit",
                    "Focus on equity funds for long-term growth",
                    "Avoid debt until you have stable income",
                    "Learn about investments through SIP calculators"
                ]
            elif user_type == 'farmer':
                recommendations['user_type_specific'] = [
                    "Invest surplus after crop sales in lump sum",
                    "Consider Kisan Vikas Patra for guaranteed returns",
                    "Diversify beyond agriculture through mutual funds",
                    "Use PM-KISAN amount for systematic investments"
                ]
            elif user_type == 'senior_citizen':
                recommendations['user_type_specific'] = [
                    "Focus on income-generating investments",
                    "Senior Citizen Savings Scheme (SCSS) for regular income",
                    "Avoid high-risk investments",
                    "Maintain higher cash reserves for emergencies"
                ]
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"❌ Error generating investment recommendations: {e}")
            return {'error': 'Unable to generate recommendations'}
    
    async def get_farmer_tools(self, location: str = 'India') -> Dict[str, Any]:
        """Comprehensive farmer-specific financial tools"""
        try:
            farmer_data = {
                'msp_rates': self.msp_data,
                'subsidies': self.subsidies,
                'crop_loan_calculator': self.get_crop_loan_info(),
                'insurance_schemes': self.get_agro_insurance_info(),
                'weather_alerts': await self.get_weather_financial_impact(),
                'market_prices': await self.get_market_prices(),
                'government_schemes': self.get_government_schemes()
            }
            
            return farmer_data
            
        except Exception as e:
            self.logger.error(f"❌ Error fetching farmer tools: {e}")
            return {'error': 'Unable to fetch farmer tools'}
    
    def get_crop_loan_info(self) -> Dict[str, Any]:
        """Get crop loan information and calculator"""
        return {
            'interest_rates': {
                'up_to_3_lakh': 7.0,
                'above_3_lakh': 9.0,
                'kcc_rate': 7.0
            },
            'loan_limits': {
                'small_farmer': 300000,
                'marginal_farmer': 100000,
                'large_farmer': 1000000
            },
            'repayment_period': '12 months (crop cycle)',
            'documents_required': [
                'Land records',
                'Aadhaar card',
                'Bank account details',
                'Crop cultivation certificate'
            ],
            'subsidy_available': 'Interest subvention of 2% for timely repayment'
        }
    
    def get_agro_insurance_info(self) -> Dict[str, Any]:
        """Get agricultural insurance information"""
        return {
            'pmfby': {
                'name': 'Pradhan Mantri Fasal Bima Yojana',
                'premium_farmer_share': {
                    'kharif': '2%',
                    'rabi': '1.5%',
                    'annual_commercial': '5%'
                },
                'coverage': 'Yield loss, prevented sowing, post-harvest losses',
                'claim_settlement': 'Within 2 months of harvest'
            },
            'weather_insurance': {
                'name': 'Weather Based Crop Insurance',
                'premium': '3-5% of sum insured',
                'coverage': 'Weather parameters (rainfall, temperature, humidity)',
                'payout': 'Automatic based on weather data'
            }
        }
    
    async def get_weather_financial_impact(self) -> Dict[str, Any]:
        """Get weather alerts with financial impact"""
        # Mock weather data - in production, integrate with weather APIs
        return {
            'current_alerts': [
                {
                    'type': 'Heavy Rainfall',
                    'severity': 'High',
                    'financial_impact': 'Potential crop damage, consider insurance claims',
                    'action_required': 'Document crop condition, contact insurance company'
                }
            ],
            'seasonal_forecast': {
                'monsoon_prediction': 'Normal',
                'financial_advice': 'Plan for normal crop yields, maintain standard investment'
            }
        }
    
    async def get_market_prices(self) -> Dict[str, Any]:
        """Get current market prices for agricultural commodities"""
        # Mock market data - in production, integrate with commodity APIs
        return {
            'mandi_prices': {
                'rice': {'price': 2200, 'change': '+1.2%', 'trend': 'up'},
                'wheat': {'price': 2300, 'change': '-0.5%', 'trend': 'down'},
                'cotton': {'price': 6800, 'change': '+2.1%', 'trend': 'up'}
            },
            'futures_prices': {
                'rice': {'price': 2250, 'expiry': '2024-03-15'},
                'wheat': {'price': 2320, 'expiry': '2024-04-15'}
            }
        }
    
    def get_government_schemes(self) -> List[Dict]:
        """Get list of government schemes for farmers"""
        return [
            {
                'name': 'PM-KISAN',
                'benefit': '₹6,000 per year',
                'eligibility': 'Small and marginal farmers',
                'application': 'Online at pmkisan.gov.in'
            },
            {
                'name': 'Kisan Credit Card',
                'benefit': 'Easy crop loans at subsidized rates',
                'eligibility': 'All farmers',
                'application': 'Through banks'
            },
            {
                'name': 'Soil Health Card',
                'benefit': 'Free soil testing and recommendations',
                'eligibility': 'All farmers',
                'application': 'Through agriculture department'
            }
        ]
    
    async def calculate_tax_optimization(self, user_profile: Dict) -> Dict[str, Any]:
        """Calculate tax optimization strategies"""
        try:
            monthly_income = user_profile.get('basic_info', {}).get('monthly_income', 30000)
            annual_income = monthly_income * 12
            
            # Calculate tax for both regimes
            old_regime_tax = self.calculate_tax(annual_income, 'old_regime')
            new_regime_tax = self.calculate_tax(annual_income, 'new_regime')
            
            tax_analysis = {
                'annual_income': annual_income,
                'old_regime': old_regime_tax,
                'new_regime': new_regime_tax,
                'recommended_regime': 'old_regime' if old_regime_tax['total_tax'] < new_regime_tax['total_tax'] else 'new_regime',
                'savings_potential': abs(old_regime_tax['total_tax'] - new_regime_tax['total_tax']),
                'tax_saving_recommendations': self.get_tax_saving_recommendations(annual_income)
            }
            
            return tax_analysis
            
        except Exception as e:
            self.logger.error(f"❌ Error calculating tax optimization: {e}")
            return {'error': 'Unable to calculate tax optimization'}
    
    def calculate_tax(self, annual_income: float, regime: str) -> Dict[str, Any]:
        """Calculate tax for given income and regime"""
        brackets = self.tax_brackets[regime]
        total_tax = 0
        tax_breakdown = []
        
        remaining_income = annual_income
        
        for bracket in brackets:
            if remaining_income <= 0:
                break
            
            taxable_in_bracket = min(remaining_income, bracket['max'] - bracket['min'])
            tax_in_bracket = taxable_in_bracket * bracket['rate']
            
            if tax_in_bracket > 0:
                tax_breakdown.append({
                    'range': f"₹{bracket['min']:,} - ₹{bracket['max']:,}" if bracket['max'] != float('inf') else f"₹{bracket['min']:,}+",
                    'rate': f"{bracket['rate']*100:.0f}%",
                    'taxable_amount': taxable_in_bracket,
                    'tax': tax_in_bracket
                })
            
            total_tax += tax_in_bracket
            remaining_income -= taxable_in_bracket
        
        # Add cess (4% on tax)
        cess = total_tax * 0.04
        total_tax_with_cess = total_tax + cess
        
        return {
            'total_tax': total_tax_with_cess,
            'tax_breakdown': tax_breakdown,
            'cess': cess,
            'effective_tax_rate': (total_tax_with_cess / annual_income * 100) if annual_income > 0 else 0
        }
    
    def get_tax_saving_recommendations(self, annual_income: float) -> List[Dict]:
        """Get tax saving recommendations based on income"""
        recommendations = []
        
        if annual_income > 250000:
            recommendations.append({
                'instrument': 'ELSS Mutual Funds',
                'max_deduction': 150000,
                'tax_saved': min(annual_income * 0.3, 45000),
                'additional_benefit': 'Potential for 12-15% returns'
            })
            
            recommendations.append({
                'instrument': 'PPF',
                'max_deduction': 150000,
                'tax_saved': min(annual_income * 0.3, 45000),
                'additional_benefit': 'Tax-free returns, 15-year lock-in'
            })
        
        if annual_income > 500000:
            recommendations.append({
                'instrument': 'NPS',
                'max_deduction': 50000,
                'tax_saved': min(annual_income * 0.3, 15000),
                'additional_benefit': 'Additional deduction under 80CCD(1B)'
            })
        
        return recommendations
