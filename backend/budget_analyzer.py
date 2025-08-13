import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
from collections import defaultdict
import logging

class BudgetAnalyzer:
    """
    Comprehensive budget analysis and financial insights generator
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.spending_categories = {
            'essentials': ['rent', 'groceries', 'utilities', 'transportation', 'healthcare'],
            'lifestyle': ['dining', 'entertainment', 'shopping', 'subscriptions'],
            'financial': ['insurance', 'investments', 'savings', 'loan_payments'],
            'miscellaneous': ['gifts', 'charity', 'other']
        }
    
    def analyze_transactions(self, transactions_df: pd.DataFrame, user_profile: Dict) -> Dict:
        """
        Comprehensive analysis of user transactions
        """
        try:
            # Ensure proper data types
            transactions_df['date'] = pd.to_datetime(transactions_df['date'])
            transactions_df['amount'] = pd.to_numeric(transactions_df['amount'])
            
            # Get analysis period (last 3 months by default)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=90)
            
            recent_transactions = transactions_df[
                (transactions_df['date'] >= start_date) & 
                (transactions_df['date'] <= end_date)
            ]
            
            analysis = {
                'summary': self._generate_spending_summary(recent_transactions),
                'category_breakdown': self._analyze_spending_by_category(recent_transactions),
                'trends': self._analyze_spending_trends(transactions_df),
                'insights': self._generate_spending_insights(recent_transactions, user_profile),
                'recommendations': self._generate_recommendations(recent_transactions, user_profile),
                'budget_health': self._assess_budget_health(recent_transactions, user_profile)
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing transactions: {e}")
            return self._get_default_analysis()
    
    def _generate_spending_summary(self, transactions_df: pd.DataFrame) -> Dict:
        """Generate overall spending summary"""
        total_spent = abs(transactions_df[transactions_df['amount'] < 0]['amount'].sum())
        total_income = transactions_df[transactions_df['amount'] > 0]['amount'].sum()
        
        avg_daily_spending = total_spent / 90  # 3 months = 90 days
        largest_expense = abs(transactions_df[transactions_df['amount'] < 0]['amount'].min())
        transaction_count = len(transactions_df[transactions_df['amount'] < 0])
        
        return {
            'total_spent': round(total_spent, 2),
            'total_income': round(total_income, 2),
            'net_savings': round(total_income - total_spent, 2),
            'avg_daily_spending': round(avg_daily_spending, 2),
            'largest_expense': round(largest_expense, 2),
            'transaction_count': transaction_count,
            'savings_rate': round(((total_income - total_spent) / total_income * 100), 2) if total_income > 0 else 0
        }
    
    def _analyze_spending_by_category(self, transactions_df: pd.DataFrame) -> Dict:
        """Analyze spending breakdown by category"""
        expenses = transactions_df[transactions_df['amount'] < 0].copy()
        expenses['amount'] = abs(expenses['amount'])
        
        category_totals = expenses.groupby('category')['amount'].sum().to_dict()
        total_expenses = sum(category_totals.values())
        
        # Categorize into major groups
        categorized_spending = defaultdict(float)
        category_percentages = {}
        
        for category, amount in category_totals.items():
            category_group = self._categorize_expense(category.lower())
            categorized_spending[category_group] += amount
            category_percentages[category] = round((amount / total_expenses * 100), 2) if total_expenses > 0 else 0
        
        return {
            'by_category': dict(category_totals),
            'by_group': dict(categorized_spending),
            'percentages': category_percentages,
            'top_categories': sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def _categorize_expense(self, category: str) -> str:
        """Categorize expenses into major groups"""
        for group, categories in self.spending_categories.items():
            if any(cat in category for cat in categories):
                return group
        return 'miscellaneous'
    
    def _analyze_spending_trends(self, transactions_df: pd.DataFrame) -> Dict:
        """Analyze spending trends over time"""
        expenses = transactions_df[transactions_df['amount'] < 0].copy()
        expenses['amount'] = abs(expenses['amount'])
        expenses['month'] = expenses['date'].dt.to_period('M')
        
        monthly_spending = expenses.groupby('month')['amount'].sum()
        
        # Calculate trend
        if len(monthly_spending) >= 2:
            recent_avg = monthly_spending.tail(3).mean()
            older_avg = monthly_spending.head(-3).mean() if len(monthly_spending) > 3 else monthly_spending.iloc[0]
            trend_percentage = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
        else:
            trend_percentage = 0
        
        return {
            'monthly_spending': monthly_spending.to_dict(),
            'trend_percentage': round(trend_percentage, 2),
            'trend_direction': 'increasing' if trend_percentage > 5 else 'decreasing' if trend_percentage < -5 else 'stable',
            'highest_month': monthly_spending.idxmax() if not monthly_spending.empty else None,
            'lowest_month': monthly_spending.idxmin() if not monthly_spending.empty else None
        }
    
    def _generate_spending_insights(self, transactions_df: pd.DataFrame, user_profile: Dict) -> List[str]:
        """Generate personalized spending insights"""
        insights = []
        demographic = user_profile.get('demographic', 'professional')
        
        # Analyze spending patterns
        expenses = transactions_df[transactions_df['amount'] < 0].copy()
        expenses['amount'] = abs(expenses['amount'])
        
        if expenses.empty:
            return ["No expense data available for analysis."]
        
        # Weekend vs weekday spending
        expenses['day_of_week'] = expenses['date'].dt.day_name()
        weekend_spending = expenses[expenses['day_of_week'].isin(['Saturday', 'Sunday'])]['amount'].mean()
        weekday_spending = expenses[~expenses['day_of_week'].isin(['Saturday', 'Sunday'])]['amount'].mean()
        
        if weekend_spending > weekday_spending * 1.5:
            insights.append("Your weekend spending is significantly higher than weekdays. Consider planning weekend activities within budget.")
        
        # Category-specific insights
        category_analysis = self._analyze_spending_by_category(transactions_df)
        top_category = category_analysis['top_categories'][0] if category_analysis['top_categories'] else None
        
        if top_category:
            category_name, amount = top_category
            percentage = category_analysis['percentages'].get(category_name, 0)
            
            if percentage > 30:
                if demographic == 'student':
                    insights.append(f"You're spending {percentage}% of your budget on {category_name}. As a student, consider finding more cost-effective alternatives.")
                else:
                    insights.append(f"{category_name} accounts for {percentage}% of your spending. This might be an area to optimize.")
        
        # Savings rate insight
        summary = self._generate_spending_summary(transactions_df)
        savings_rate = summary.get('savings_rate', 0)
        
        if savings_rate < 10:
            if demographic == 'student':
                insights.append("Your savings rate is low. Even saving ₹500-1000 per month as a student can build good financial habits.")
            else:
                insights.append("Your savings rate is below recommended levels. Aim for saving at least 20% of your income.")
        elif savings_rate > 30:
            insights.append("Great job on saving! You're saving more than the recommended 20%. Consider investing some of your savings for better returns.")
        
        return insights
    
    def _generate_recommendations(self, transactions_df: pd.DataFrame, user_profile: Dict) -> List[str]:
        """Generate personalized financial recommendations"""
        recommendations = []
        demographic = user_profile.get('demographic', 'professional')
        income = user_profile.get('monthly_income', 0)
        
        summary = self._generate_spending_summary(transactions_df)
        category_analysis = self._analyze_spending_by_category(transactions_df)
        
        # Income-based recommendations
        if demographic == 'student':
            recommendations.extend([
                "Create a simple 50-30-20 budget: 50% needs, 30% wants, 20% savings",
                "Track your expenses using apps or a simple spreadsheet",
                "Consider part-time work or internships to increase income",
                "Look into student discounts and free activities for entertainment"
            ])
        else:
            recommendations.extend([
                "Build an emergency fund covering 3-6 months of expenses",
                "Consider systematic investment plans (SIP) for long-term wealth building",
                "Optimize your tax planning with ELSS and other 80C investments",
                "Review and increase your health insurance coverage"
            ])
        
        # Spending-specific recommendations
        if 'dining' in str(category_analysis['by_category']) or 'entertainment' in str(category_analysis['by_category']):
            dining_spending = category_analysis['by_category'].get('dining', 0) + category_analysis['by_category'].get('entertainment', 0)
            if dining_spending > income * 0.15:
                recommendations.append("Consider meal planning and cooking at home to reduce dining expenses")
        
        # Savings recommendations
        if summary['savings_rate'] < 20:
            recommendations.append("Automate your savings by setting up automatic transfers to a savings account")
        
        return recommendations[:6]  # Return top 6 recommendations
    
    def _assess_budget_health(self, transactions_df: pd.DataFrame, user_profile: Dict) -> Dict:
        """Assess overall budget health with scoring"""
        summary = self._generate_spending_summary(transactions_df)
        
        # Calculate health score (0-100)
        health_score = 0
        
        # Savings rate score (40 points max)
        savings_rate = summary.get('savings_rate', 0)
        if savings_rate >= 20:
            health_score += 40
        elif savings_rate >= 10:
            health_score += 25
        elif savings_rate >= 0:
            health_score += 10
        
        # Spending consistency score (30 points max)
        trends = self._analyze_spending_trends(transactions_df)
        if trends['trend_direction'] == 'stable':
            health_score += 30
        elif trends['trend_direction'] == 'decreasing':
            health_score += 25
        else:
            health_score += 10
        
        # Category balance score (30 points max)
        category_analysis = self._analyze_spending_by_category(transactions_df)
        essentials_pct = (category_analysis['by_group'].get('essentials', 0) / 
                         summary['total_spent'] * 100) if summary['total_spent'] > 0 else 0
        
        if 40 <= essentials_pct <= 60:
            health_score += 30
        elif 30 <= essentials_pct <= 70:
            health_score += 20
        else:
            health_score += 10
        
        # Determine health status
        if health_score >= 80:
            status = "Excellent"
            color = "green"
        elif health_score >= 60:
            status = "Good"
            color = "blue"
        elif health_score >= 40:
            status = "Fair"
            color = "orange"
        else:
            status = "Needs Improvement"
            color = "red"
        
        return {
            'score': health_score,
            'status': status,
            'color': color,
            'breakdown': {
                'savings_health': savings_rate,
                'spending_trend': trends['trend_direction'],
                'category_balance': round(essentials_pct, 1)
            }
        }
    
    def _get_default_analysis(self) -> Dict:
        """Return default analysis when data processing fails"""
        return {
            'summary': {
                'total_spent': 0,
                'total_income': 0,
                'net_savings': 0,
                'avg_daily_spending': 0,
                'largest_expense': 0,
                'transaction_count': 0,
                'savings_rate': 0
            },
            'category_breakdown': {'by_category': {}, 'by_group': {}, 'percentages': {}, 'top_categories': []},
            'trends': {'monthly_spending': {}, 'trend_percentage': 0, 'trend_direction': 'stable'},
            'insights': ["Unable to analyze transactions. Please check your data format."],
            'recommendations': ["Upload transaction data to get personalized recommendations."],
            'budget_health': {'score': 0, 'status': 'No Data', 'color': 'gray'}
        }
    
    def generate_budget_summary_report(self, analysis: Dict, user_profile: Dict) -> str:
        """Generate a comprehensive budget summary report"""
        demographic = user_profile.get('demographic', 'professional')
        name = user_profile.get('name', 'User')
        
        summary = analysis['summary']
        health = analysis['budget_health']
        
        # Adjust tone based on demographic
        if demographic == 'student':
            greeting = f"Hey {name}! 👋 Here's your budget snapshot:"
            tone = "casual and encouraging"
        else:
            greeting = f"Hello {name}, here's your comprehensive financial analysis:"
            tone = "professional and detailed"
        
        report = f"""
{greeting}

💰 FINANCIAL OVERVIEW
• Total Spent: ₹{summary['total_spent']:,.2f}
• Total Income: ₹{summary['total_income']:,.2f}
• Net Savings: ₹{summary['net_savings']:,.2f}
• Savings Rate: {summary['savings_rate']}%
• Budget Health: {health['status']} ({health['score']}/100)

📊 TOP INSIGHTS
"""
        
        for insight in analysis['insights'][:3]:
            report += f"• {insight}\n"
        
        report += f"""
🎯 KEY RECOMMENDATIONS
"""
        
        for rec in analysis['recommendations'][:3]:
            report += f"• {rec}\n"
        
        if demographic == 'student':
            report += "\nKeep up the great work on managing your finances! 🌟"
        else:
            report += "\nContinue monitoring your financial health for optimal results."
        
        return report