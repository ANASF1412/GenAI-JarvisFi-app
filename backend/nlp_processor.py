import re
# import spacy  # Commented out to avoid dependency issues
from typing import Dict, List, Tuple, Optional
import pandas as pd
from datetime import datetime, timedelta
import logging
from collections import defaultdict

class NLPProcessor:
    """
    Advanced NLP processing for financial queries and context understanding
    """

    def __init__(self):
        # Initialize spacy model (use 'en_core_web_sm' or load lightweight model)
        # Using basic NLP processing without spacy for now
        self.nlp = None
        logging.warning("Using basic NLP processing without SpaCy.")

        self.logger = logging.getLogger(__name__)
        
        # Financial entity patterns
        self.financial_patterns = {
            'currency': [
                r'₹\s*([0-9,]+(?:\.[0-9]{2})?)',
                r'rupees?\s*([0-9,]+(?:\.[0-9]{2})?)',
                r'rs\.?\s*([0-9,]+(?:\.[0-9]{2})?)',
                r'inr\s*([0-9,]+(?:\.[0-9]{2})?)',
                r'\$\s*([0-9,]+(?:\.[0-9]{2})?)',
                r'dollars?\s*([0-9,]+(?:\.[0-9]{2})?)'
            ],
            'percentage': [
                r'([0-9]+(?:\.[0-9]+)?)\s*%',
                r'([0-9]+(?:\.[0-9]+)?)\s*percent'
            ],
            'time_period': [
                r'(\d+)\s*(?:years?|yrs?)',
                r'(\d+)\s*(?:months?|mons?)',
                r'(\d+)\s*(?:days?)',
                r'monthly|weekly|daily|annually|quarterly'
            ],
            'financial_goals': [
                r'(?:save|saving)\s+(?:for\s+)?(\w+(?:\s+\w+)*)',
                r'(?:buy|buying)\s+(?:a\s+)?(\w+(?:\s+\w+)*)',
                r'(?:invest|investing)\s+(?:in\s+)?(\w+(?:\s+\w+)*)'
            ]
        }
        
        # Intent classification patterns
        self.intent_patterns = {
            'budget_query': [
                r'budget', r'spending', r'expenses?', r'costs?', r'money management',
                r'track.*money', r'financial plan'
            ],
            'savings_query': [
                r'save|saving', r'emergency fund', r'savings account', r'save money',
                r'how to save', r'savings plan', r'savings goal'
            ],
            'investment_query': [
                r'invest|investment', r'stocks?', r'mutual funds?', r'sip', r'portfolio',
                r'returns?', r'market', r'equity', r'bonds?', r'securities'
            ],
            'tax_query': [
                r'tax', r'deduction', r'exemption', r'80c', r'tax saving', r'tax planning',
                r'tax return', r'tax filing', r'tds'
            ],
            'loan_query': [
                r'loan', r'emi', r'credit', r'debt', r'mortgage', r'home loan',
                r'personal loan', r'education loan', r'interest rate'
            ],
            'insurance_query': [
                r'insurance', r'policy', r'premium', r'coverage', r'health insurance',
                r'life insurance', r'term insurance'
            ],
            'general_query': [
                r'help', r'what', r'how', r'explain', r'tell me', r'advice', r'suggest'
            ]
        }
        
        # Financial keywords for context
        self.financial_keywords = {
            'investment_types': [
                'sip', 'mutual fund', 'equity', 'debt', 'bonds', 'stocks', 'shares',
                'gold', 'real estate', 'fixed deposit', 'fd', 'rd', 'ppf', 'nps',
                'elss', 'index fund', 'etf'
            ],
            'banking_terms': [
                'account', 'bank', 'savings', 'current', 'deposit', 'withdrawal',
                'transaction', 'balance', 'statement', 'branch', 'atm'
            ],
            'tax_terms': [
                '80c', '80d', 'hra', 'tds', 'tax return', 'itr', 'deduction',
                'exemption', 'tax slab', 'rebate', 'advance tax'
            ],
            'loan_terms': [
                'principal', 'interest', 'emi', 'tenure', 'processing fee',
                'prepayment', 'foreclosure', 'collateral', 'guarantor'
            ]
        }
    
    def process_query(self, query: str, user_context: Dict = None) -> Dict:
        """
        Comprehensive query processing to extract intent, entities, and context
        """
        try:
            # Clean and normalize the query
            cleaned_query = self._clean_query(query)
            
            # Extract basic information
            result = {
                'original_query': query,
                'cleaned_query': cleaned_query,
                'intent': self._classify_intent(cleaned_query),
                'entities': self._extract_entities(cleaned_query),
                'financial_context': self._extract_financial_context(cleaned_query),
                'sentiment': self._analyze_sentiment(cleaned_query),
                'complexity_level': self._assess_complexity(cleaned_query),
                'requires_data': self._check_data_requirement(cleaned_query),
                'suggested_followups': self._generate_followup_questions(cleaned_query)
            }
            
            # Enhanced processing with spaCy if available
            if self.nlp:
                result.update(self._advanced_nlp_analysis(cleaned_query))
            
            # Add user context information
            if user_context:
                result['user_context'] = self._process_user_context(user_context, result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return self._get_default_processing_result(query)
    
    def _clean_query(self, query: str) -> str:
        """Clean and normalize the input query"""
        # Remove extra whitespace
        query = re.sub(r'\s+', ' ', query.strip())
        
        # Normalize currency symbols
        query = re.sub(r'rs\.?|rupees?', '₹', query, flags=re.IGNORECASE)
        
        # Normalize common abbreviations
        abbreviations = {
            r'\bfd\b': 'fixed deposit',
            r'\brd\b': 'recurring deposit',
            r'\bsip\b': 'systematic investment plan',
            r'\bemi\b': 'equated monthly installment',
            r'\bppf\b': 'public provident fund',
            r'\bnps\b': 'national pension scheme'
        }
        
        for abbrev, full_form in abbreviations.items():
            query = re.sub(abbrev, full_form, query, flags=re.IGNORECASE)
        
        return query
    
    def _classify_intent(self, query: str) -> Dict:
        """Classify the main intent of the query"""
        intent_scores = defaultdict(float)
        query_lower = query.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, query_lower))
                intent_scores[intent] += matches
        
        # Determine primary intent
        if intent_scores:
            primary_intent = max(intent_scores.items(), key=lambda x: x[1])
            confidence = primary_intent[1] / sum(intent_scores.values()) if sum(intent_scores.values()) > 0 else 0
        else:
            primary_intent = ('general_query', 1)
            confidence = 0.5
        
        return {
            'primary': primary_intent[0],
            'confidence': confidence,
            'all_intents': dict(intent_scores)
        }
    
    def _extract_entities(self, query: str) -> Dict:
        """Extract financial entities from the query"""
        entities = {
            'currency_amounts': [],
            'percentages': [],
            'time_periods': [],
            'financial_instruments': [],
            'goals': []
        }
        
        # Extract currency amounts
        for pattern in self.financial_patterns['currency']:
            matches = re.finditer(pattern, query, re.IGNORECASE)
            for match in matches:
                amount_str = match.group(1).replace(',', '')
                try:
                    amount = float(amount_str)
                    entities['currency_amounts'].append({
                        'amount': amount,
                        'text': match.group(0),
                        'position': match.span()
                    })
                except ValueError:
                    continue
        
        # Extract percentages
        for pattern in self.financial_patterns['percentage']:
            matches = re.finditer(pattern, query, re.IGNORECASE)
            for match in matches:
                try:
                    percentage = float(match.group(1))
                    entities['percentages'].append({
                        'percentage': percentage,
                        'text': match.group(0),
                        'position': match.span()
                    })
                except ValueError:
                    continue
        
        # Extract time periods
        for pattern in self.financial_patterns['time_period']:
            matches = re.finditer(pattern, query, re.IGNORECASE)
            for match in matches:
                entities['time_periods'].append({
                    'text': match.group(0),
                    'position': match.span()
                })
        
        # Extract financial instruments
        query_lower = query.lower()
        for category, instruments in self.financial_keywords.items():
            for instrument in instruments:
                if instrument in query_lower:
                    entities['financial_instruments'].append({
                        'instrument': instrument,
                        'category': category
                    })
        
        return entities
    
    def _extract_financial_context(self, query: str) -> Dict:
        """Extract broader financial context from the query"""
        context = {
            'financial_domain': [],
            'urgency_level': 'medium',
            'planning_horizon': 'medium_term',
            'risk_indicators': [],
            'action_type': 'advice_seeking'
        }
        
        query_lower = query.lower()
        
        # Determine financial domain
        domain_keywords = {
            'personal_finance': ['budget', 'personal', 'family', 'household'],
            'investment': ['invest', 'portfolio', 'returns', 'market'],
            'tax_planning': ['tax', 'deduction', 'exemption', 'saving tax'],
            'insurance': ['insurance', 'policy', 'coverage', 'premium'],
            'banking': ['account', 'bank', 'deposit', 'loan'],
            'retirement': ['retirement', 'pension', 'old age', 'senior']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                context['financial_domain'].append(domain)
        
        # Assess urgency
        urgent_indicators = ['urgent', 'asap', 'immediately', 'soon', 'quickly']
        if any(indicator in query_lower for indicator in urgent_indicators):
            context['urgency_level'] = 'high'
        elif any(word in query_lower for word in ['plan', 'future', 'long term']):
            context['urgency_level'] = 'low'
        
        # Determine planning horizon
        if any(word in query_lower for word in ['retirement', 'long term', 'years']):
            context['planning_horizon'] = 'long_term'
        elif any(word in query_lower for word in ['monthly', 'short', 'immediate']):
            context['planning_horizon'] = 'short_term'
        
        # Identify risk indicators
        risk_keywords = ['risk', 'safe', 'secure', 'guaranteed', 'volatile', 'fluctuation']
        context['risk_indicators'] = [word for word in risk_keywords if word in query_lower]
        
        # Determine action type
        action_indicators = {
            'advice_seeking': ['how', 'what', 'should i', 'advice', 'suggest', 'recommend'],
            'information_request': ['tell me', 'explain', 'what is', 'define'],
            'calculation_request': ['calculate', 'compute', 'how much', 'amount'],
            'comparison_request': ['compare', 'difference', 'better', 'vs', 'versus']
        }
        
        for action, indicators in action_indicators.items():
            if any(indicator in query_lower for indicator in indicators):
                context['action_type'] = action
                break
        
        return context
    
    def _analyze_sentiment(self, query: str) -> Dict:
        """Analyze sentiment of the query"""
        positive_indicators = [
            'great', 'good', 'excellent', 'happy', 'satisfied', 'love',
            'awesome', 'fantastic', 'perfect', 'amazing'
        ]
        
        negative_indicators = [
            'bad', 'terrible', 'awful', 'hate', 'disappointed', 'frustrated',
            'confused', 'lost', 'stuck', 'worried', 'anxious', 'stressed'
        ]
        
        neutral_indicators = [
            'okay', 'fine', 'alright', 'normal', 'average', 'standard'
        ]
        
        query_lower = query.lower()
        
        positive_count = sum(1 for word in positive_indicators if word in query_lower)
        negative_count = sum(1 for word in negative_indicators if word in query_lower)
        neutral_count = sum(1 for word in neutral_indicators if word in query_lower)
        
        if positive_count > negative_count and positive_count > neutral_count:
            sentiment = 'positive'
            confidence = positive_count / (positive_count + negative_count + neutral_count + 1)
        elif negative_count > positive_count and negative_count > neutral_count:
            sentiment = 'negative'
            confidence = negative_count / (positive_count + negative_count + neutral_count + 1)
        else:
            sentiment = 'neutral'
            confidence = 0.5
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'indicators': {
                'positive': positive_count,
                'negative': negative_count,
                'neutral': neutral_count
            }
        }
    
    def _assess_complexity(self, query: str) -> str:
        """Assess the complexity level of the query"""
        # Simple indicators
        simple_indicators = ['what is', 'how to', 'explain', 'basic', 'simple']
        
        # Complex indicators
        complex_indicators = [
            'optimization', 'strategy', 'portfolio', 'allocation', 'diversification',
            'tax planning', 'estate planning', 'risk management', 'derivatives'
        ]
        
        # Advanced indicators
        advanced_indicators = [
            'hedging', 'arbitrage', 'options', 'futures', 'quantitative',
            'algorithmic', 'leverage', 'margin', 'structured products'
        ]
        
        query_lower = query.lower()
        
        if any(indicator in query_lower for indicator in advanced_indicators):
            return 'advanced'
        elif any(indicator in query_lower for indicator in complex_indicators):
            return 'intermediate'
        elif any(indicator in query_lower for indicator in simple_indicators):
            return 'beginner'
        else:
            return 'intermediate'  # default
    
    def _check_data_requirement(self, query: str) -> Dict:
        """Check if the query requires specific data analysis"""
        data_indicators = {
            'transaction_data': ['spending', 'expenses', 'transactions', 'budget analysis'],
            'investment_data': ['portfolio', 'returns', 'performance', 'allocation'],
            'income_data': ['salary', 'income', 'earnings', 'revenue'],
            'comparative_data': ['compare', 'benchmark', 'vs', 'versus']
        }
        
        required_data = []
        query_lower = query.lower()
        
        for data_type, indicators in data_indicators.items():
            if any(indicator in query_lower for indicator in indicators):
                required_data.append(data_type)
        
        return {
            'requires_data': len(required_data) > 0,
            'data_types': required_data,
            'can_provide_generic': len(required_data) == 0
        }
    
    def _generate_followup_questions(self, query: str) -> List[str]:
        """Generate relevant follow-up questions"""
        intent = self._classify_intent(query)
        primary_intent = intent['primary']
        
        followup_templates = {
            'budget_query': [
                "Would you like me to analyze your spending patterns?",
                "Do you have specific budget categories you'd like to focus on?",
                "What's your current monthly income range?"
            ],
            'savings_query': [
                "What's your savings goal and timeline?",
                "Are you looking for short-term or long-term savings strategies?",
                "What's your current monthly savings amount?"
            ],
            'investment_query': [
                "What's your risk tolerance - conservative, moderate, or aggressive?",
                "Are you looking for short-term or long-term investments?",
                "What's your investment budget?"
            ],
            'tax_query': [
                "Which tax-saving instruments are you currently using?",
                "What's your annual income range?",
                "Are you looking for this financial year or next year's planning?"
            ]
        }
        
        return followup_templates.get(primary_intent, [
            "Could you provide more details about your financial situation?",
            "What specific aspect would you like me to focus on?",
            "Do you have any particular goals in mind?"
        ])
    
    def _advanced_nlp_analysis(self, query: str) -> Dict:
        """Advanced NLP analysis using spaCy if available"""
        if not self.nlp:
            return {}
        
        doc = self.nlp(query)
        
        # Extract named entities
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'description': ent.label_  # Simplified without spacy.explain
            })
        
        # Extract key phrases
        key_phrases = []
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) > 1:
                key_phrases.append(chunk.text)
        
        # Analyze sentence structure
        sentences = [sent.text.strip() for sent in doc.sents]
        
        return {
            'named_entities': entities,
            'key_phrases': key_phrases,
            'sentences': sentences,
            'pos_tags': [(token.text, token.pos_) for token in doc],
            'dependency_relations': [(token.text, token.dep_, token.head.text) for token in doc]
        }
    
    def _process_user_context(self, user_context: Dict, query_analysis: Dict) -> Dict:
        """Process user context to enhance query understanding"""
        context_insights = {
            'demographic_relevance': self._assess_demographic_relevance(user_context, query_analysis),
            'personalization_opportunities': self._identify_personalization_opportunities(user_context, query_analysis),
            'historical_context': self._analyze_historical_context(user_context, query_analysis)
        }
        
        return context_insights
    
    def _assess_demographic_relevance(self, user_context: Dict, query_analysis: Dict) -> Dict:
        """Assess how user demographics affect query interpretation"""
        demographic = user_context.get('demographic', 'professional')
        age = user_context.get('age', 30)
        income_level = user_context.get('income_level', 'medium')
        
        relevance = {
            'demographic_match': demographic,
            'age_appropriate_advice': age < 25,  # Younger users get different advice
            'income_appropriate_suggestions': income_level,
            'complexity_adjustment': 'beginner' if demographic == 'student' else 'intermediate'
        }
        
        # Adjust based on query complexity and user profile
        query_complexity = query_analysis.get('complexity_level', 'intermediate')
        if demographic == 'student' and query_complexity == 'advanced':
            relevance['needs_simplification'] = True
        elif demographic == 'professional' and query_complexity == 'beginner':
            relevance['can_provide_advanced_details'] = True
        
        return relevance
    
    def _identify_personalization_opportunities(self, user_context: Dict, query_analysis: Dict) -> List[str]:
        """Identify opportunities to personalize the response"""
        opportunities = []
        
        # Income-based personalization
        monthly_income = user_context.get('monthly_income', 0)
        if monthly_income > 0 and 'currency_amounts' in query_analysis.get('entities', {}):
            opportunities.append('income_based_calculations')
        
        # Goal-based personalization
        financial_goals = user_context.get('financial_goals', [])
        if financial_goals and query_analysis.get('intent', {}).get('primary') == 'savings_query':
            opportunities.append('goal_aligned_advice')
        
        # Risk profile personalization
        risk_tolerance = user_context.get('risk_tolerance', 'moderate')
        if query_analysis.get('intent', {}).get('primary') == 'investment_query':
            opportunities.append('risk_adjusted_recommendations')
        
        # Life stage personalization
        age = user_context.get('age', 30)
        if age < 25:
            opportunities.append('early_career_focus')
        elif age > 50:
            opportunities.append('retirement_planning_focus')
        
        return opportunities
    
    def _analyze_historical_context(self, user_context: Dict, query_analysis: Dict) -> Dict:
        """Analyze historical context from user's previous interactions"""
        # This would integrate with conversation history in a real implementation
        return {
            'previous_topics': user_context.get('previous_topics', []),
            'recurring_concerns': user_context.get('recurring_concerns', []),
            'progress_tracking': user_context.get('progress_tracking', {})
        }
    
    def _get_default_processing_result(self, query: str) -> Dict:
        """Return default processing result when analysis fails"""
        return {
            'original_query': query,
            'cleaned_query': query,
            'intent': {'primary': 'general_query', 'confidence': 0.5, 'all_intents': {}},
            'entities': {'currency_amounts': [], 'percentages': [], 'time_periods': [], 'financial_instruments': [], 'goals': []},
            'financial_context': {'financial_domain': ['personal_finance'], 'urgency_level': 'medium', 'planning_horizon': 'medium_term'},
            'sentiment': {'sentiment': 'neutral', 'confidence': 0.5},
            'complexity_level': 'intermediate',
            'requires_data': {'requires_data': False, 'data_types': [], 'can_provide_generic': True},
            'suggested_followups': ["Could you provide more details about your financial situation?"]
        }
    
    def extract_transaction_query_params(self, query: str) -> Dict:
        """Extract parameters for transaction queries"""
        params = {
            'time_range': None,
            'categories': [],
            'amount_range': None,
            'transaction_type': None,
            'analysis_type': None
        }
        
        query_lower = query.lower()
        
        # Time range extraction
        time_patterns = {
            'last_month': ['last month', 'previous month', 'past month'],
            'last_3_months': ['last 3 months', 'past 3 months', 'last quarter'],
            'last_6_months': ['last 6 months', 'past 6 months', 'last half year'],
            'last_year': ['last year', 'past year', 'previous year'],
            'this_month': ['this month', 'current month'],
            'this_year': ['this year', 'current year']
        }
        
        for period, patterns in time_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                params['time_range'] = period
                break
        
        # Category extraction
        category_keywords = {
            'food': ['food', 'dining', 'restaurant', 'groceries', 'meals'],
            'transportation': ['transport', 'fuel', 'gas', 'uber', 'taxi', 'bus', 'metro'],
            'entertainment': ['entertainment', 'movies', 'games', 'fun', 'leisure'],
            'shopping': ['shopping', 'clothes', 'electronics', 'purchases'],
            'utilities': ['utilities', 'electricity', 'water', 'internet', 'phone'],
            'healthcare': ['medical', 'health', 'doctor', 'pharmacy', 'hospital']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                params['categories'].append(category)
        
        # Analysis type
        analysis_patterns = {
            'summary': ['summary', 'overview', 'total', 'overall'],
            'detailed': ['detailed', 'breakdown', 'analysis', 'deep dive'],
            'trends': ['trends', 'patterns', 'changes', 'comparison'],
            'insights': ['insights', 'recommendations', 'advice', 'suggestions']
        }
        
        for analysis, patterns in analysis_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                params['analysis_type'] = analysis
                break
        
        return params
    
    def generate_contextual_prompts(self, user_profile: Dict, recent_queries: List[str] = None) -> List[str]:
        """Generate contextual conversation starters based on user profile"""
        demographic = user_profile.get('demographic', 'professional')
        financial_goals = user_profile.get('financial_goals', [])
        
        prompts = []
        
        # Demographic-specific prompts
        if demographic == 'student':
            prompts.extend([
                "Want to create a student budget that actually works? 💰",
                "Looking for ways to save money while in college? 📚",
                "Curious about investing with small amounts? 🚀",
                "Need help managing student loans? 🎓"
            ])
        elif demographic == 'professional':
            prompts.extend([
                "Ready to optimize your tax savings this year? 📊",
                "Want to review your investment portfolio allocation? 💼",
                "Interested in planning for early retirement? 🏖️",
                "Need help with comprehensive financial planning? 📈"
            ])
        
        # Goal-based prompts
        if 'emergency_fund' in financial_goals:
            prompts.append("Let's build your emergency fund strategy step by step! 🛡️")
        if 'house_purchase' in financial_goals:
            prompts.append("Planning to buy a house? Let's calculate how much you need! 🏠")
        if 'retirement' in financial_goals:
            prompts.append("Want to know if you're on track for retirement? 🎯")
        
        # Seasonal prompts
        current_month = datetime.now().month
        if current_month in [3, 4]:  # March-April (Indian financial year end)
            prompts.append("Tax season is here! Need help with last-minute tax planning? 📋")
        elif current_month in [1, 2]:  # January-February
            prompts.append("New year, new financial goals! Want to set up a plan? ✨")
        
        return prompts[:5]  # Return top 5 prompts
    
    def validate_financial_input(self, input_text: str, expected_type: str) -> Dict:
        """Validate financial inputs (amounts, percentages, etc.)"""
        validation_result = {
            'is_valid': False,
            'parsed_value': None,
            'error_message': None,
            'suggestions': []
        }
        
        try:
            if expected_type == 'currency':
                # Extract currency amount
                currency_pattern = r'[₹$]?\s*([0-9,]+(?:\.[0-9]{1,2})?)'
                match = re.search(currency_pattern, input_text)
                
                if match:
                    amount_str = match.group(1).replace(',', '')
                    amount = float(amount_str)
                    
                    if amount < 0:
                        validation_result['error_message'] = "Amount cannot be negative"
                        validation_result['suggestions'] = ["Please enter a positive amount"]
                    elif amount > 10**10:  # 10 billion limit
                        validation_result['error_message'] = "Amount seems too large"
                        validation_result['suggestions'] = ["Please verify the amount"]
                    else:
                        validation_result['is_valid'] = True
                        validation_result['parsed_value'] = amount
                else:
                    validation_result['error_message'] = "Could not parse currency amount"
                    validation_result['suggestions'] = ["Try: ₹50000 or 50,000"]
            
            elif expected_type == 'percentage':
                # Extract percentage
                percentage_pattern = r'([0-9]+(?:\.[0-9]+)?)\s*%?'
                match = re.search(percentage_pattern, input_text)
                
                if match:
                    percentage = float(match.group(1))
                    
                    if percentage < 0 or percentage > 100:
                        validation_result['error_message'] = "Percentage should be between 0 and 100"
                        validation_result['suggestions'] = ["Try: 15% or 25"]
                    else:
                        validation_result['is_valid'] = True
                        validation_result['parsed_value'] = percentage
                else:
                    validation_result['error_message'] = "Could not parse percentage"
                    validation_result['suggestions'] = ["Try: 15% or 25"]
            
            elif expected_type == 'age':
                # Extract age
                age_pattern = r'([0-9]+)'
                match = re.search(age_pattern, input_text)
                
                if match:
                    age = int(match.group(1))
                    
                    if age < 18 or age > 100:
                        validation_result['error_message'] = "Age should be between 18 and 100"
                        validation_result['suggestions'] = ["Please enter a valid age"]
                    else:
                        validation_result['is_valid'] = True
                        validation_result['parsed_value'] = age
                else:
                    validation_result['error_message'] = "Could not parse age"
                    validation_result['suggestions'] = ["Try: 25 or twenty-five"]
        
        except Exception as e:
            validation_result['error_message'] = f"Validation error: {str(e)}"
            validation_result['suggestions'] = ["Please check your input format"]
        
        return validation_result