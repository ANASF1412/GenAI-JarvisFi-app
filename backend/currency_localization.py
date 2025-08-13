#!/usr/bin/env python3
"""
Currency Converter and Localization Module
Supports multi-currency operations and regional financial regulations
"""

import os
import json
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import re
from decimal import Decimal, ROUND_HALF_UP

# Forex and currency libraries
try:
    from forex_python.converter import CurrencyRates, CurrencyCodes
    FOREX_PYTHON_AVAILABLE = True
except ImportError:
    FOREX_PYTHON_AVAILABLE = False

# Geolocation
try:
    import geoip2.database
    import geoip2.errors
    GEOIP_AVAILABLE = True
except ImportError:
    GEOIP_AVAILABLE = False

class CurrencyLocalizationManager:
    """
    Comprehensive currency and localization manager
    """
    
    def __init__(self, cache_duration_hours: int = 1):
        """Initialize currency and localization manager"""
        self.logger = self._setup_logger()
        self.cache_duration = timedelta(hours=cache_duration_hours)
        
        # Initialize currency services
        self._setup_currency_services()
        
        # Regional configurations
        self.regional_configs = {
            'IN': {  # India
                'currency': 'INR',
                'currency_symbol': '₹',
                'decimal_places': 2,
                'thousand_separator': ',',
                'decimal_separator': '.',
                'number_format': 'indian',  # 1,00,000 format
                'tax_system': 'GST',
                'financial_year': 'april_march',
                'languages': ['hindi', 'english', 'tamil', 'telugu', 'bengali'],
                'regulatory_bodies': ['RBI', 'SEBI', 'IRDAI', 'CBDT'],
                'banking_hours': '10:00-16:00',
                'stock_market_hours': '09:15-15:30'
            },
            'US': {  # United States
                'currency': 'USD',
                'currency_symbol': '$',
                'decimal_places': 2,
                'thousand_separator': ',',
                'decimal_separator': '.',
                'number_format': 'western',
                'tax_system': 'Federal_State',
                'financial_year': 'january_december',
                'languages': ['english'],
                'regulatory_bodies': ['SEC', 'FDIC', 'IRS'],
                'banking_hours': '09:00-17:00',
                'stock_market_hours': '09:30-16:00'
            },
            'GB': {  # United Kingdom
                'currency': 'GBP',
                'currency_symbol': '£',
                'decimal_places': 2,
                'thousand_separator': ',',
                'decimal_separator': '.',
                'number_format': 'western',
                'tax_system': 'HMRC',
                'financial_year': 'april_march',
                'languages': ['english'],
                'regulatory_bodies': ['FCA', 'PRA', 'HMRC'],
                'banking_hours': '09:00-17:00',
                'stock_market_hours': '08:00-16:30'
            }
        }
        
        # Currency cache
        self.exchange_rate_cache = {}
        self.cache_timestamps = {}
        
        # Supported currencies
        self.supported_currencies = [
            'INR', 'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'SGD',
            'AED', 'SAR', 'QAR', 'KWD', 'BHD', 'OMR', 'THB', 'MYR', 'IDR', 'PHP'
        ]
        
        self.logger.info("Currency and localization manager initialized")
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _setup_currency_services(self):
        """Setup currency conversion services"""
        try:
            if FOREX_PYTHON_AVAILABLE:
                self.currency_rates = CurrencyRates()
                self.currency_codes = CurrencyCodes()
                self.logger.info("Forex Python initialized")
            else:
                self.currency_rates = None
                self.currency_codes = None
                self.logger.warning("Forex Python not available, using fallback")
            
            # API keys for external services
            self.exchange_api_key = os.getenv('EXCHANGE_API_KEY')
            self.fixer_api_key = os.getenv('FIXER_API_KEY')
            
        except Exception as e:
            self.logger.error(f"Currency services setup failed: {e}")
    
    def get_exchange_rate(self, from_currency: str, to_currency: str, use_cache: bool = True) -> Optional[float]:
        """Get exchange rate between two currencies"""
        try:
            if from_currency == to_currency:
                return 1.0
            
            cache_key = f"{from_currency}_{to_currency}"
            
            # Check cache first
            if use_cache and cache_key in self.exchange_rate_cache:
                cache_time = self.cache_timestamps.get(cache_key)
                if cache_time and datetime.now() - cache_time < self.cache_duration:
                    return self.exchange_rate_cache[cache_key]
            
            # Try multiple sources for exchange rates
            rate = None
            
            # Method 1: Forex Python
            if FOREX_PYTHON_AVAILABLE and self.currency_rates:
                try:
                    rate = self.currency_rates.get_rate(from_currency, to_currency)
                    self.logger.info(f"Exchange rate from Forex Python: {from_currency}/{to_currency} = {rate}")
                except Exception as e:
                    self.logger.warning(f"Forex Python failed: {e}")
            
            # Method 2: ExchangeRate-API
            if not rate and self.exchange_api_key:
                try:
                    rate = self._get_rate_from_exchange_api(from_currency, to_currency)
                except Exception as e:
                    self.logger.warning(f"ExchangeRate-API failed: {e}")
            
            # Method 3: Fixer.io
            if not rate and self.fixer_api_key:
                try:
                    rate = self._get_rate_from_fixer(from_currency, to_currency)
                except Exception as e:
                    self.logger.warning(f"Fixer.io failed: {e}")
            
            # Method 4: Free API fallback
            if not rate:
                try:
                    rate = self._get_rate_from_free_api(from_currency, to_currency)
                except Exception as e:
                    self.logger.warning(f"Free API failed: {e}")
            
            # Cache the result
            if rate:
                self.exchange_rate_cache[cache_key] = rate
                self.cache_timestamps[cache_key] = datetime.now()
            
            return rate
            
        except Exception as e:
            self.logger.error(f"Exchange rate retrieval failed: {e}")
            return None
    
    def _get_rate_from_exchange_api(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Get rate from ExchangeRate-API"""
        url = f"https://v6.exchangerate-api.com/v6/{self.exchange_api_key}/pair/{from_currency}/{to_currency}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('conversion_rate')
        
        return None
    
    def _get_rate_from_fixer(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Get rate from Fixer.io"""
        url = f"http://data.fixer.io/api/latest?access_key={self.fixer_api_key}&base={from_currency}&symbols={to_currency}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            rates = data.get('rates', {})
            return rates.get(to_currency)
        
        return None
    
    def _get_rate_from_free_api(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Get rate from free API"""
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            rates = data.get('rates', {})
            return rates.get(to_currency)
        
        return None
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> Dict:
        """Convert amount from one currency to another"""
        try:
            result = {
                'success': False,
                'original_amount': amount,
                'from_currency': from_currency,
                'to_currency': to_currency,
                'converted_amount': 0.0,
                'exchange_rate': 0.0,
                'formatted_original': '',
                'formatted_converted': '',
                'conversion_time': datetime.now().isoformat()
            }
            
            # Get exchange rate
            rate = self.get_exchange_rate(from_currency, to_currency)
            
            if rate:
                converted_amount = amount * rate
                
                result.update({
                    'success': True,
                    'converted_amount': round(converted_amount, 4),
                    'exchange_rate': rate,
                    'formatted_original': self.format_currency(amount, from_currency),
                    'formatted_converted': self.format_currency(converted_amount, to_currency)
                })
            
            return result
            
        except Exception as e:
            self.logger.error(f"Currency conversion failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'original_amount': amount,
                'from_currency': from_currency,
                'to_currency': to_currency
            }
    
    def format_currency(self, amount: float, currency: str, region: str = 'IN') -> str:
        """Format currency amount according to regional conventions"""
        try:
            config = self.regional_configs.get(region, self.regional_configs['IN'])
            
            # Round to appropriate decimal places
            decimal_places = config['decimal_places']
            rounded_amount = Decimal(str(amount)).quantize(
                Decimal('0.' + '0' * decimal_places), 
                rounding=ROUND_HALF_UP
            )
            
            # Get currency symbol
            symbol = config.get('currency_symbol', currency)
            if currency in ['USD', 'CAD', 'AUD', 'SGD']:
                symbol = '$'
            elif currency == 'EUR':
                symbol = '€'
            elif currency == 'GBP':
                symbol = '£'
            elif currency == 'JPY':
                symbol = '¥'
            elif currency == 'INR':
                symbol = '₹'
            
            # Format number according to regional style
            if config['number_format'] == 'indian':
                # Indian numbering system (1,00,000)
                formatted = self._format_indian_number(float(rounded_amount))
            else:
                # Western numbering system (100,000)
                formatted = f"{float(rounded_amount):,.{decimal_places}f}"
            
            return f"{symbol}{formatted}"
            
        except Exception as e:
            self.logger.error(f"Currency formatting failed: {e}")
            return f"{currency} {amount:.2f}"
    
    def _format_indian_number(self, number: float) -> str:
        """Format number in Indian numbering system"""
        try:
            # Convert to string with 2 decimal places
            num_str = f"{number:.2f}"
            integer_part, decimal_part = num_str.split('.')
            
            # Reverse the integer part for easier processing
            reversed_int = integer_part[::-1]
            
            # Add commas in Indian format
            formatted_parts = []
            
            # First group of 3 digits
            if len(reversed_int) > 3:
                formatted_parts.append(reversed_int[:3])
                remaining = reversed_int[3:]
                
                # Subsequent groups of 2 digits
                while remaining:
                    if len(remaining) >= 2:
                        formatted_parts.append(remaining[:2])
                        remaining = remaining[2:]
                    else:
                        formatted_parts.append(remaining)
                        break
            else:
                formatted_parts.append(reversed_int)
            
            # Join and reverse back
            formatted_integer = ','.join(formatted_parts)[::-1]
            
            return f"{formatted_integer}.{decimal_part}"
            
        except Exception as e:
            self.logger.error(f"Indian number formatting failed: {e}")
            return f"{number:.2f}"
    
    def get_regional_config(self, country_code: str = None, ip_address: str = None) -> Dict:
        """Get regional configuration based on location"""
        try:
            # Default to India
            region = 'IN'
            
            # Try to detect region from IP if available
            if ip_address and GEOIP_AVAILABLE:
                try:
                    # This would require a GeoIP database file
                    # For demo purposes, we'll use a simple mapping
                    pass
                except Exception as e:
                    self.logger.warning(f"GeoIP detection failed: {e}")
            
            # Use provided country code
            if country_code and country_code in self.regional_configs:
                region = country_code
            
            config = self.regional_configs[region].copy()
            config['region_code'] = region
            config['detected_at'] = datetime.now().isoformat()
            
            return config
            
        except Exception as e:
            self.logger.error(f"Regional config retrieval failed: {e}")
            return self.regional_configs['IN']
    
    def get_supported_currencies(self) -> List[Dict]:
        """Get list of supported currencies with details"""
        try:
            currencies = []
            
            for currency_code in self.supported_currencies:
                currency_info = {
                    'code': currency_code,
                    'name': self._get_currency_name(currency_code),
                    'symbol': self._get_currency_symbol(currency_code),
                    'supported': True
                }
                currencies.append(currency_info)
            
            return currencies
            
        except Exception as e:
            self.logger.error(f"Supported currencies retrieval failed: {e}")
            return []
    
    def _get_currency_name(self, currency_code: str) -> str:
        """Get full name of currency"""
        currency_names = {
            'INR': 'Indian Rupee',
            'USD': 'US Dollar',
            'EUR': 'Euro',
            'GBP': 'British Pound',
            'JPY': 'Japanese Yen',
            'AUD': 'Australian Dollar',
            'CAD': 'Canadian Dollar',
            'CHF': 'Swiss Franc',
            'CNY': 'Chinese Yuan',
            'SGD': 'Singapore Dollar',
            'AED': 'UAE Dirham',
            'SAR': 'Saudi Riyal'
        }
        
        return currency_names.get(currency_code, currency_code)
    
    def _get_currency_symbol(self, currency_code: str) -> str:
        """Get currency symbol"""
        currency_symbols = {
            'INR': '₹',
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'AUD': 'A$',
            'CAD': 'C$',
            'CHF': 'CHF',
            'CNY': '¥',
            'SGD': 'S$',
            'AED': 'د.إ',
            'SAR': '﷼'
        }
        
        return currency_symbols.get(currency_code, currency_code)
