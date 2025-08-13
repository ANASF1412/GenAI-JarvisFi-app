"""
Smart Financial Alerts and Notifications System
Provides intelligent spending alerts, budget warnings, and financial insights
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging
from collections import defaultdict

class SmartAlerts:
    """
    Intelligent alert system for financial monitoring and notifications
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.alert_thresholds = {
            'high_spending_percentage': 0.8,  # 80% of income
            'category_overspending': 0.4,     # 40% in single category
            'unusual_transaction_multiplier': 3.0,  # 3x average
            'low_savings_rate': 0.1,         # Below 10%
            'emergency_fund_months': 3       # Less than 3 months expenses
        }
        
        self.alert_types = {
            'critical': {'color': 'red', 'icon': '🚨', 'priority': 1},
            'warning': {'color': 'orange', 'icon': '⚠️', 'priority': 2},
            'info': {'color': 'blue', 'icon': 'ℹ️', 'priority': 3},
            'positive': {'color': 'green', 'icon': '✅', 'priority': 4},
            'tip': {'color': 'purple', 'icon': '💡', 'priority': 5}
        }
    
    def generate_all_alerts(self, 
                          transactions_df: pd.DataFrame, 
                          user_profile: Dict, 
                          budget_analysis: Dict) -> List[Dict]:
        """
        Generate comprehensive alerts based on spending patterns and profile
        """
        alerts = []
        
        if transactions_df.empty:
            return alerts
        
        # Generate different types of alerts
        alerts.extend(self._check_spending_alerts(transactions_df, user_profile))
        alerts.extend(self._check_budget_health_alerts(budget_analysis, user_profile))
        alerts.extend(self._check_savings_alerts(budget_analysis, user_profile))
        alerts.extend(self._check_unusual_activity_alerts(transactions_df))
        alerts.extend(self._check_category_alerts(budget_analysis, user_profile))
        alerts.extend(self._generate_positive_reinforcement(budget_analysis, user_profile))
        alerts.extend(self._generate_smart_tips(transactions_df, user_profile, budget_analysis))
        
        # Sort alerts by priority and return
        alerts.sort(key=lambda x: x['priority'])
        
        return alerts
    
    def _check_spending_alerts(self, transactions_df: pd.DataFrame, user_profile: Dict) -> List[Dict]:
        """Check for high spending alerts"""
        alerts = []
        
        monthly_income = user_profile.get('monthly_income', 0)
        if monthly_income == 0:
            return alerts
        
        # Calculate recent spending (last 30 days)
        recent_date = datetime.now() - timedelta(days=30)
        recent_transactions = transactions_df[transactions_df['date'] >= recent_date]
        
        total_spent = abs(recent_transactions[recent_transactions['amount'] < 0]['amount'].sum())
        spending_ratio = total_spent / monthly_income
        
        if spending_ratio >= self.alert_thresholds['high_spending_percentage']:
            alerts.append({
                'type': 'critical',
                'title': 'High Spending Alert!',
                'message': f"You've spent {spending_ratio*100:.1f}% of your monthly income (₹{total_spent:,.0f}). Consider reviewing your expenses.",
                'recommendation': "Review discretionary spending and look for areas to cut back.",
                'priority': 1,
                **self.alert_types['critical']
            })
        elif spending_ratio >= 0.7:
            alerts.append({
                'type': 'warning',
                'title': 'Budget Alert',
                'message': f"You've used {spending_ratio*100:.1f}% of your monthly budget. Keep an eye on spending.",
                'recommendation': "Monitor remaining expenses for the month carefully.",
                'priority': 2,
                **self.alert_types['warning']
            })
        
        return alerts
    
    def _check_budget_health_alerts(self, budget_analysis: Dict, user_profile: Dict) -> List[Dict]:
        """Check budget health and generate alerts"""
        alerts = []
        
        health = budget_analysis.get('budget_health', {})
        score = health.get('score', 0)
        
        if score < 40:
            alerts.append({
                'type': 'critical',
                'title': 'Budget Health Critical',
                'message': f"Your financial health score is {score}/100. Immediate action needed!",
                'recommendation': "Focus on increasing savings rate and reducing unnecessary expenses.",
                'priority': 1,
                **self.alert_types['critical']
            })
        elif score < 60:
            alerts.append({
                'type': 'warning',
                'title': 'Budget Health Needs Improvement',
                'message': f"Your financial health score is {score}/100. There's room for improvement.",
                'recommendation': "Work on building emergency fund and optimizing spending categories.",
                'priority': 2,
                **self.alert_types['warning']
            })
        
        return alerts
    
    def _check_savings_alerts(self, budget_analysis: Dict, user_profile: Dict) -> List[Dict]:
        """Check savings rate and generate alerts"""
        alerts = []
        
        summary = budget_analysis.get('summary', {})
        savings_rate = summary.get('savings_rate', 0) / 100
        demographic = user_profile.get('demographic', 'professional')
        
        min_savings_rate = 0.1 if demographic == 'student' else 0.2
        
        if savings_rate < self.alert_thresholds['low_savings_rate']:
            message = f"Your savings rate is {savings_rate*100:.1f}%. "
            if demographic == 'student':
                message += "Even as a student, try to save at least 10%."
                recommendation = "Start with small amounts - even ₹500/month builds good habits."
            else:
                message += "Aim for at least 20% savings rate."
                recommendation = "Automate your savings and review discretionary spending."
            
            alerts.append({
                'type': 'warning',
                'title': 'Low Savings Rate',
                'message': message,
                'recommendation': recommendation,
                'priority': 2,
                **self.alert_types['warning']
            })
        
        return alerts
    
    def _check_unusual_activity_alerts(self, transactions_df: pd.DataFrame) -> List[Dict]:
        """Detect unusual spending patterns"""
        alerts = []
        
        expenses = transactions_df[transactions_df['amount'] < 0].copy()
        if expenses.empty:
            return alerts
        
        expenses['amount'] = abs(expenses['amount'])
        
        # Check for unusually large transactions
        avg_transaction = expenses['amount'].mean()
        large_transactions = expenses[expenses['amount'] > avg_transaction * self.alert_thresholds['unusual_transaction_multiplier']]
        
        if not large_transactions.empty:
            largest = large_transactions.iloc[0]
            alerts.append({
                'type': 'info',
                'title': 'Large Transaction Detected',
                'message': f"Unusual large expense: ₹{largest['amount']:,.0f} for {largest['description']}",
                'recommendation': "Verify if this was planned and adjust budget accordingly.",
                'priority': 3,
                **self.alert_types['info']
            })
        
        # Check for frequency changes
        recent_transactions = expenses[expenses['date'] >= datetime.now() - timedelta(days=7)]
        if len(recent_transactions) > avg_transaction * 2:
            alerts.append({
                'type': 'info',
                'title': 'Increased Transaction Frequency',
                'message': f"You've made {len(recent_transactions)} transactions this week, more than usual.",
                'recommendation': "Review if increased spending aligns with your budget plan.",
                'priority': 3,
                **self.alert_types['info']
            })
        
        return alerts
    
    def _check_category_alerts(self, budget_analysis: Dict, user_profile: Dict) -> List[Dict]:
        """Check for category-specific spending alerts"""
        alerts = []
        
        categories = budget_analysis.get('category_breakdown', {})
        category_spending = categories.get('by_category', {})
        total_spending = budget_analysis.get('summary', {}).get('total_spent', 1)
        
        # Check for category overspending
        for category, amount in category_spending.items():
            category_percentage = amount / total_spending
            
            if category_percentage > self.alert_thresholds['category_overspending']:
                alerts.append({
                    'type': 'warning',
                    'title': f'High {category.title()} Spending',
                    'message': f"{category.title()} accounts for {category_percentage*100:.1f}% of your spending (₹{amount:,.0f})",
                    'recommendation': f"Consider ways to optimize {category} expenses.",
                    'priority': 2,
                    **self.alert_types['warning']
                })
        
        return alerts
    
    def _generate_positive_reinforcement(self, budget_analysis: Dict, user_profile: Dict) -> List[Dict]:
        """Generate positive reinforcement messages"""
        alerts = []
        
        summary = budget_analysis.get('summary', {})
        health = budget_analysis.get('budget_health', {})
        savings_rate = summary.get('savings_rate', 0)
        
        # Positive savings feedback
        if savings_rate >= 20:
            alerts.append({
                'type': 'positive',
                'title': 'Excellent Savings Rate! 🎉',
                'message': f"You're saving {savings_rate:.1f}% of your income - that's fantastic!",
                'recommendation': "Keep it up! Consider investing your savings for better returns.",
                'priority': 4,
                **self.alert_types['positive']
            })
        
        # Good budget health
        if health.get('score', 0) >= 80:
            alerts.append({
                'type': 'positive',
                'title': 'Great Financial Health! ⭐',
                'message': f"Your financial health score is {health.get('score')}/100 - excellent management!",
                'recommendation': "You're on track! Consider setting stretch financial goals.",
                'priority': 4,
                **self.alert_types['positive']
            })
        
        return alerts
    
    def _generate_smart_tips(self, transactions_df: pd.DataFrame, user_profile: Dict, budget_analysis: Dict) -> List[Dict]:
        """Generate intelligent financial tips based on spending patterns"""
        alerts = []
        
        demographic = user_profile.get('demographic', 'professional')
        categories = budget_analysis.get('category_breakdown', {}).get('by_category', {})
        
        # Demographic-specific tips
        if demographic == 'student':
            tips = [
                "Use student discounts whenever possible - they can save 10-50% on many purchases.",
                "Consider a part-time job or freelancing to boost income during studies.",
                "Start investing small amounts now - time is your biggest advantage!"
            ]
        else:
            tips = [
                "Automate your investments - set up SIPs for consistent wealth building.",
                "Review insurance coverage annually to ensure adequate protection.",
                "Consider tax-saving investments like ELSS funds for dual benefits."
            ]
        
        # Add category-specific tips
        if 'dining' in categories and categories['dining'] > 5000:
            tips.append("Try meal prepping on weekends to reduce dining out expenses.")
        
        if 'transportation' in categories and categories['transportation'] > 3000:
            tips.append("Consider carpooling or public transport to reduce commute costs.")
        
        # Convert tips to alerts
        for tip in tips[:2]:  # Limit to 2 tips to avoid overwhelming
            alerts.append({
                'type': 'tip',
                'title': 'Smart Money Tip 💰',
                'message': tip,
                'recommendation': "",
                'priority': 5,
                **self.alert_types['tip']
            })
        
        return alerts
    
    def format_alert_for_display(self, alert: Dict) -> str:
        """Format alert for display in Streamlit"""
        icon = alert.get('icon', '📢')
        title = alert.get('title', 'Alert')
        message = alert.get('message', '')
        recommendation = alert.get('recommendation', '')
        
        formatted = f"{icon} **{title}**\n\n{message}"
        if recommendation:
            formatted += f"\n\n💡 **Recommendation:** {recommendation}"
        
        return formatted
    
    def get_alert_counts_by_type(self, alerts: List[Dict]) -> Dict[str, int]:
        """Get count of alerts by type for dashboard display"""
        counts = defaultdict(int)
        for alert in alerts:
            counts[alert['type']] += 1
        return dict(counts)