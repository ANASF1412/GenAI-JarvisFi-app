from typing import Dict, List, Tuple
import re
from enum import Enum

class UserDemographic(Enum):
    STUDENT = "student"
    PROFESSIONAL = "professional"
    ENTREPRENEUR = "entrepreneur"
    RETIRED = "retired"

class DemographicAdapter:
    """
    Adapts chatbot responses based on user demographic profiles
    """
    
    def __init__(self):
        self.demographic_profiles = {
            'student': {
                'tone': 'casual',
                'complexity': 'simple',
                'emoji_usage': 'high',
                'examples': 'relatable',
                'focus_areas': ['budgeting', 'saving', 'part_time_income', 'student_loans'],
                'vocabulary': 'informal',
                'response_length': 'medium'
            },
            'professional': {
                'tone': 'formal',
                'complexity': 'detailed',
                'emoji_usage': 'minimal',
                'examples': 'professional',
                'focus_areas': ['investment', 'tax_planning', 'retirement', 'insurance'],
                'vocabulary': 'technical',
                'response_length': 'comprehensive'
            },
            'entrepreneur': {
                'tone': 'motivational',
                'complexity': 'advanced',
                'emoji_usage': 'moderate',
                'examples': 'business_oriented',
                'focus_areas': ['business_finance', 'investment', 'tax_optimization', 'cash_flow'],
                'vocabulary': 'business',
                'response_length': 'detailed'
            },
            'retired': {
                'tone': 'respectful',
                'complexity': 'clear',
                'emoji_usage': 'minimal',
                'examples': 'conservative',
                'focus_areas': ['pension', 'healthcare', 'conservative_investment', 'estate_planning'],
                'vocabulary': 'traditional',
                'response_length': 'concise'
            }
        }
        
        self.financial_advice_templates = {
            'budget_management': {
                'student': {
                    'intro': "Hey! Let's talk budgeting - it's easier than you think! 💰",
                    'advice': "Start with the basics: track your income (part-time job, allowance, etc.) and categorize your expenses. The 50-30-20 rule works great - 50% for needs (food, transport), 30% for wants (entertainment, shopping), and 20% for savings. Even saving ₹500-1000 monthly makes a difference!",
                    'examples': "For example, if you get ₹10,000 monthly, aim to save ₹2,000, spend ₹5,000 on essentials, and ₹3,000 on fun stuff.",
                    'tools': "Try apps like Mint, YNAB, or even a simple Google Sheet to track expenses."
                },
                'professional': {
                    'intro': "Effective budget management is crucial for financial success.",
                    'advice': "Implement a comprehensive budgeting system using the zero-based budgeting method. Allocate every rupee of income to specific categories: fixed expenses, variable costs, emergency fund contributions, and investment allocations. Maintain a detailed expense tracking system and review monthly variances.",
                    'examples': "With a ₹80,000 monthly salary, consider: ₹35,000 for essentials, ₹15,000 for lifestyle, ₹16,000 for savings/investments, ₹8,000 for taxes, and ₹6,000 for miscellaneous expenses.",
                    'tools': "Consider professional tools like Quicken, Personal Capital, or comprehensive Excel templates for detailed analysis."
                }
            },
            'investment_guidance': {
                'student': {
                    'intro': "Investing as a student? You're ahead of the game! 🚀",
                    'advice': "Start small with SIPs (Systematic Investment Plans) - even ₹500/month helps! Focus on diversified equity mutual funds for long-term growth. Since you have time on your side, you can take slightly higher risks for better returns. Don't put all money in one place!",
                    'examples': "Start with index funds like Nifty 50 or broad market funds. Apps like Groww, Zerodha Coin make investing super easy.",
                    'tools': "Check out investment apps designed for beginners - they have great educational content too!"
                },
                'professional': {
                    'intro': "Let's develop a comprehensive investment strategy aligned with your professional goals.",
                    'advice': "Establish a diversified portfolio across asset classes: 60-70% equity (mix of large-cap, mid-cap, and international funds), 20-30% debt instruments, and 10% alternative investments. Consider tax-efficient options like ELSS funds, PPF, and NPS. Regularly rebalance your portfolio based on market conditions and life stage changes.",
                    'examples': "For a 30-year-old professional earning ₹12 lakhs annually: ₹50,000 in equity SIPs, ₹20,000 in debt funds, ₹15,000 in ELSS for tax saving, and ₹15,000 in EPF/PPF.",
                    'tools': "Use platforms like Kuvera, INDmoney, or direct mutual fund investments for lower expense ratios."
                }
            },
            'savings_advice': {
                'student': {
                    'intro': "Saving money as a student? You're building an awesome habit! 💪",
                    'advice': "Every rupee counts! Start with small goals - maybe save for a new phone or a trip with friends. Use the 'pay yourself first' method: save as soon as you get money, before spending on anything else. Even ₹50 a day adds up to ₹1,500 monthly!",
                    'examples': "Create specific goals: 'Save ₹5,000 for new laptop in 6 months' or 'Emergency fund of ₹3,000 for unexpected expenses'.",
                    'tools': "Use digital piggy banks, recurring deposits, or high-yield savings accounts."
                },
                'professional': {
                    'intro': "Strategic savings planning is fundamental to financial security.",
                    'advice': "Implement a multi-tiered savings approach: emergency fund (6 months expenses), short-term goals fund, and long-term wealth accumulation. Automate savings through systematic transfers and take advantage of high-yield instruments like fixed deposits, debt mutual funds, and government schemes.",
                    'examples': "For ₹1 lakh monthly income: ₹20,000 emergency fund building, ₹15,000 goal-based savings, ₹25,000 investment savings.",
                    'tools': "Utilize automatic investment plans, sweep-in accounts, and tax-saving instruments for optimal returns."
                }
            },
            'tax_planning': {
                'student': {
                    'intro': "Taxes might seem boring, but understanding them saves money! 📚",
                    'advice': "As a student, you might not earn much, but if you do internships or part-time work, know your basics! Income up to ₹2.5 lakhs is tax-free. Keep receipts for any work-related expenses. If you're doing freelancing, consider the new tax regime vs old one.",
                    'examples': "If you earn ₹3 lakhs from internships, you'll pay tax only on ₹50,000. But investments in ELSS can reduce this!",
                    'tools': "Use simple tax calculators online to understand your liability."
                },
                'professional': {
                    'intro': "Comprehensive tax planning is essential for wealth optimization.",
                    'advice': "Maximize deductions under Section 80C (₹1.5L), 80D (health insurance), and other applicable sections. Compare old vs new tax regimes based on your investment pattern. Consider tax-efficient investment vehicles like ELSS, PPF, NPS, and tax-free bonds. Plan capital gains harvesting and tax loss harvesting strategies.",
                    'examples': "Professional earning ₹15 lakhs: Save ₹46,000+ annually through 80C investments, health insurance premiums, and home loan interest deductions.",
                    'tools': "Consult tax professionals, use comprehensive tax planning software, and maintain detailed investment records."
                }
            }
        }
    
    def adapt_response(self, content: str, demographic: str, financial_topic: str = None) -> str:
        """
        Adapt response based on user demographic
        """
        if demographic not in self.demographic_profiles:
            demographic = 'professional'  # default
        
        profile = self.demographic_profiles[demographic]
        
        # Get specific financial advice if topic is provided
        if financial_topic and financial_topic in self.financial_advice_templates:
            if demographic in self.financial_advice_templates[financial_topic]:
                template = self.financial_advice_templates[financial_topic][demographic]
                return self._format_financial_advice(template, profile)
        
        # General content adaptation
        adapted_content = self._adjust_tone(content, profile)
        adapted_content = self._adjust_complexity(adapted_content, profile)
        adapted_content = self._add_emojis(adapted_content, profile)
        adapted_content = self._adjust_examples(adapted_content, profile, demographic)
        
        return adapted_content
    
    def _format_financial_advice(self, template: Dict, profile: Dict) -> str:
        """Format financial advice using template"""
        sections = []
        
        if 'intro' in template:
            sections.append(template['intro'])
        
        if 'advice' in template:
            sections.append(f"\n💡 **Advice:**\n{template['advice']}")
        
        if 'examples' in template:
            sections.append(f"\n📈 **Example:**\n{template['examples']}")
        
        if 'tools' in template:
            sections.append(f"\n🔧 **Tools & Resources:**\n{template['tools']}")
        
        return '\n'.join(sections)
    
    def _adjust_tone(self, content: str, profile: Dict) -> str:
        """Adjust tone based on demographic profile"""
        tone = profile['tone']
        
        if tone == 'casual':
            # Make content more conversational
            content = re.sub(r'\bYou should\b', 'You could', content)
            content = re.sub(r'\bIt is recommended\b', "It's a good idea", content)
            content = re.sub(r'\bConsider\b', 'Maybe try', content)
        
        elif tone == 'formal':
            # Make content more professional
            content = re.sub(r"\bcan't\b", 'cannot', content)
            content = re.sub(r"\bdon't\b", 'do not', content)
            content = re.sub(r"\bit's\b", 'it is', content)
        
        elif tone == 'motivational':
            # Add motivational elements
            motivational_phrases = [
                "This is a great opportunity to",
                "You're on the right track by",
                "Take advantage of",
                "Build momentum by"
            ]
            # Add motivational context where appropriate
        
        return content
    
    def _adjust_complexity(self, content: str, profile: Dict) -> str:
        """Adjust complexity based on user sophistication"""
        complexity = profile['complexity']
        
        if complexity == 'simple':
            # Simplify financial jargon
            replacements = {
                'systematic investment plan': 'SIP (regular monthly investment)',
                'asset allocation': 'how you divide your money',
                'diversification': 'spreading investments across different areas',
                'expense ratio': 'fees charged by funds',
                'market volatility': 'market ups and downs'
            }
            
            for technical_term, simple_term in replacements.items():
                content = re.sub(technical_term, simple_term, content, flags=re.IGNORECASE)
        
        elif complexity == 'detailed':
            # Add more technical details and explanations
            pass  # Keep technical terms as-is
        
        return content
    
    def _add_emojis(self, content: str, profile: Dict) -> str:
        """Add appropriate emoji usage"""
        emoji_usage = profile['emoji_usage']
        
        if emoji_usage == 'high':
            # Add relevant financial emojis
            emoji_map = {
                'budget': '💰',
                'saving': '💸',
                'investment': '📈',
                'money': '💵',
                'goal': '🎯',
                'tip': '💡',
                'warning': '⚠️',
                'success': '✅'
            }
            
            for keyword, emoji in emoji_map.items():
                if keyword in content.lower() and emoji not in content:
                    content = content.replace(keyword, f"{keyword} {emoji}", 1)
        
        elif emoji_usage == 'minimal':
            # Remove most emojis except essential ones
            essential_emojis = ['✅', '⚠️', '💰']
            # Keep only essential emojis
        
        return content
    
    def _adjust_examples(self, content: str, profile: Dict, demographic: str) -> str:
        """Add demographic-appropriate examples"""
        examples_type = profile['examples']
        
        example_scenarios = {
            'student': {
                'income_examples': ['₹5,000 from part-time job', '₹2,000 allowance', '₹8,000 from internship'],
                'expense_examples': ['college fees', 'textbooks', 'hostel food', 'transportation'],
                'saving_goals': ['new laptop', 'semester abroad', 'emergency fund'],
                'investment_amounts': ['₹500/month', '₹1,000/month', '₹2,000/month']
            },
            'professional': {
                'income_examples': ['₹80,000 salary', '₹1.2L monthly income', '₹15L annual package'],
                'expense_examples': ['EMI payments', 'insurance premiums', 'family expenses'],
                'saving_goals': ['house down payment', 'child education', 'retirement corpus'],
                'investment_amounts': ['₹10,000/month', '₹25,000/month', '₹50,000/month']
            }
        }
        
        if demographic in example_scenarios:
            scenarios = example_scenarios[demographic]
            # Context-aware example insertion could be implemented here
        
        return content
    
    def get_personalized_greeting(self, user_profile: Dict) -> str:
        """Generate personalized greeting based on user profile"""
        name = user_profile.get('name', 'there')
        demographic = user_profile.get('demographic', 'professional')
        
        greetings = {
            'student': [
                f"Hey {name}! 👋 Ready to level up your money game?",
                f"Hi {name}! Let's make your finances work smarter, not harder! 💪",
                f"What's up {name}! Your financial advisor bot is here to help! 🤖"
            ],
            'professional': [
                f"Good day {name}. How can I assist with your financial planning today?",
                f"Hello {name}. I'm here to provide comprehensive financial guidance.",
                f"Welcome {name}. Let's optimize your financial strategy together."
            ],
            'entrepreneur': [
                f"Hello {name}! Ready to grow your wealth like you grow your business? 🚀",
                f"Hi {name}! Let's strategize your financial success! 💼",
                f"Welcome {name}! Your business mindset + smart finance = success! 📊"
            ]
        }
        
        import random
        return random.choice(greetings.get(demographic, greetings['professional']))
    
    def suggest_relevant_topics(self, demographic: str) -> List[str]:
        """Suggest relevant financial topics based on demographic"""
        if demographic not in self.demographic_profiles:
            demographic = 'professional'
        
        focus_areas = self.demographic_profiles[demographic]['focus_areas']
        
        topic_suggestions = {
            'budgeting': 'Create a personalized budget plan',
            'saving': 'Build an emergency fund strategy',
            'investment': 'Start your investment journey',
            'tax_planning': 'Optimize your tax savings',
            'student_loans': 'Manage education loans effectively',
            'retirement': 'Plan for retirement security',
            'insurance': 'Review insurance coverage needs',
            'business_finance': 'Manage business cash flow',
            'part_time_income': 'Maximize earnings from part-time work'
        }
        
        relevant_topics = []
        for area in focus_areas:
            if area in topic_suggestions:
                relevant_topics.append(topic_suggestions[area])
        
        return relevant_topics[:5]  # Return top 5 suggestions
    
    def customize_financial_metrics(self, metrics: Dict, demographic: str) -> Dict:
        """Customize financial metrics display based on demographic"""
        if demographic == 'student':
            # Focus on simpler metrics for students
            student_metrics = {
                'monthly_budget': metrics.get('total_spent', 0),
                'savings_amount': metrics.get('net_savings', 0),
                'daily_spending': metrics.get('avg_daily_spending', 0),
                'top_expense_category': 'dining'  # Most relevant for students
            }
            return student_metrics
        
        elif demographic == 'professional':
            # Comprehensive metrics for professionals
            professional_metrics = {
                'monthly_income': metrics.get('total_income', 0),
                'monthly_expenses': metrics.get('total_spent', 0),
                'savings_rate': metrics.get('savings_rate', 0),
                'investment_allocation': 0,  # Would come from investment analysis
                'tax_efficiency_score': 0,  # Would come from tax analysis
                'emergency_fund_months': 0  # Would come from savings analysis
            }
            return professional_metrics
        
        return metrics  # Return as-is for other demographics