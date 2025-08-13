"""
Real-time Currency Converter and Financial Rate Service
Enhanced with multiple currency APIs and caching
"""

import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import streamlit as st

class CurrencyConverter:
    """
    Advanced currency converter with multiple API fallbacks and caching
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.base_currencies = ['USD', 'EUR', 'GBP', 'INR', 'JPY', 'AUD', 'CAD']
        self.cache = {}
        self.cache_duration = timedelta(hours=1)  # Cache for 1 hour
        
        # API endpoints (fallback sequence)
        self.api_endpoints = [
            'https://api.exchangerate-api.com/v4/latest/',
            'https://api.fixer.io/latest',
            'https://open.er-api.com/v6/latest/'
        ]
    
    def get_exchange_rate(self, from_currency: str = 'USD', to_currency: str = 'INR') -> Optional[float]:
        """
        Get real-time exchange rate with caching and fallback APIs
        """
        cache_key = f"{from_currency}_{to_currency}"
        
        # Check cache first
        if self._is_cached_valid(cache_key):
            return self.cache[cache_key]['rate']
        
        # Try multiple APIs
        for api_url in self.api_endpoints:
            try:
                rate = self._fetch_rate_from_api(api_url, from_currency, to_currency)
                if rate:
                    self._cache_rate(cache_key, rate)
                    return rate
            except Exception as e:
                self.logger.warning(f"Failed to fetch from {api_url}: {e}")
                continue
        
        # Fallback to hardcoded rates if all APIs fail
        return self._get_fallback_rate(from_currency, to_currency)
    
    def _fetch_rate_from_api(self, api_url: str, from_currency: str, to_currency: str) -> Optional[float]:
        """Fetch rate from specific API"""
        response = requests.get(f"{api_url}{from_currency}", timeout=5)
        data = response.json()
        
        if 'rates' in data and to_currency in data['rates']:
            return float(data['rates'][to_currency])
        
        return None
    
    def _is_cached_valid(self, cache_key: str) -> bool:
        """Check if cached rate is still valid"""
        if cache_key in self.cache:
            cache_time = self.cache[cache_key]['timestamp']
            return datetime.now() - cache_time < self.cache_duration
        return False
    
    def _cache_rate(self, cache_key: str, rate: float):
        """Cache the exchange rate"""
        self.cache[cache_key] = {
            'rate': rate,
            'timestamp': datetime.now()
        }
    
    def _get_fallback_rate(self, from_currency: str, to_currency: str) -> float:
        """Fallback exchange rates (approximate)"""
        fallback_rates = {
            ('USD', 'INR'): 83.0,
            ('EUR', 'INR'): 90.0,
            ('GBP', 'INR'): 105.0,
            ('INR', 'USD'): 0.012,
            ('INR', 'EUR'): 0.011,
            ('INR', 'GBP'): 0.0095,
        }
        
        return fallback_rates.get((from_currency, to_currency), 1.0)
    
    def convert_amount(self, amount: float, from_currency: str = 'USD', to_currency: str = 'INR') -> Dict:
        """
        Convert amount between currencies with detailed response
        """
        rate = self.get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * rate
        
        return {
            'original_amount': amount,
            'original_currency': from_currency,
            'converted_amount': round(converted_amount, 2),
            'target_currency': to_currency,
            'exchange_rate': rate,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'rate_source': 'real_time' if rate else 'fallback'
        }
    
    def get_popular_currencies(self) -> Dict[str, str]:
        """Get popular currency codes with names"""
        return {
            'USD': '🇺🇸 US Dollar',
            'EUR': '🇪🇺 Euro',
            'GBP': '🇬🇧 British Pound',
            'INR': '🇮🇳 Indian Rupee',
            'JPY': '🇯🇵 Japanese Yen',
            'AUD': '🇦🇺 Australian Dollar',
            'CAD': '🇨🇦 Canadian Dollar',
            'CHF': '🇨🇭 Swiss Franc',
            'CNY': '🇨🇳 Chinese Yuan',
            'SGD': '🇸🇬 Singapore Dollar'
        }
    
    def render_currency_widget(self):
        """Render interactive currency converter widget for Streamlit"""
        st.subheader("💱 Currency Converter")
        
        currencies = self.get_popular_currencies()
        currency_codes = list(currencies.keys())
        
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Amount:", min_value=0.01, value=100.0, step=0.01)
            from_curr = st.selectbox("From:", currency_codes, index=0)
        
        with col2:
            to_curr = st.selectbox("To:", currency_codes, index=3)  # Default to INR
            
            if from_curr != to_curr:
                result = self.convert_amount(amount, from_curr, to_curr)
                
                st.metric(
                    label=f"{currencies[to_curr]}",
                    value=f"{result['converted_amount']:,.2f}",
                    delta=f"Rate: {result['exchange_rate']:.4f}"
                )
                
                # Show rate freshness
                if result['rate_source'] == 'real_time':
                    st.success(f"✅ Live rate updated: {result['timestamp']}")
                else:
                    st.warning("⚠️ Using fallback rate (API unavailable)")
            else:
                st.info("Select different currencies to convert")
        
        # Quick conversion buttons
        st.subheader("🚀 Quick Conversions")
        quick_amounts = [1000, 5000, 10000, 25000, 50000]
        
        if from_curr == 'INR' and to_curr == 'USD':
            cols = st.columns(len(quick_amounts))
            for i, amt in enumerate(quick_amounts):
                result = self.convert_amount(amt, from_curr, to_curr)
                with cols[i]:
                    st.metric(f"₹{amt:,}", f"${result['converted_amount']:,.2f}")
        
        elif from_curr == 'USD' and to_curr == 'INR':
            usd_amounts = [100, 500, 1000, 2000, 5000]
            cols = st.columns(len(usd_amounts))
            for i, amt in enumerate(usd_amounts):
                result = self.convert_amount(amt, from_curr, to_curr)
                with cols[i]:
                    st.metric(f"${amt:,}", f"₹{result['converted_amount']:,.0f}")