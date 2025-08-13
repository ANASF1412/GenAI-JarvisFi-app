"""
Advanced Voice Processing System for JarvisFi
Supports multilingual STT/TTS with offline capabilities for low-literacy and farmer users
"""

import os
import io
import json
import logging
import asyncio
import tempfile
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import wave

# Voice processing imports
try:
    import speech_recognition as sr
    import pyttsx3
    from pydub import AudioSegment
    from pydub.playback import play
    STT_TTS_AVAILABLE = True
except ImportError:
    STT_TTS_AVAILABLE = False

# Advanced TTS imports
try:
    from coqui_tts import TTS
    import torch
    COQUI_AVAILABLE = True
except ImportError:
    COQUI_AVAILABLE = False

# Google Cloud Speech (if available)
try:
    from google.cloud import speech
    from google.cloud import texttospeech
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False

class VoiceProcessor:
    """
    Advanced multilingual voice processing with offline capabilities
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_voice_engines()
        self.setup_language_models()
        
        # Voice configuration
        self.voice_config = {
            'sample_rate': 16000,
            'channels': 1,
            'chunk_size': 1024,
            'timeout': 5,
            'phrase_timeout': 1
        }
        
        # Language mappings
        self.language_codes = {
            'en': {'google': 'en-US', 'azure': 'en-US', 'local': 'english'},
            'ta': {'google': 'ta-IN', 'azure': 'ta-IN', 'local': 'tamil'},
            'hi': {'google': 'hi-IN', 'azure': 'hi-IN', 'local': 'hindi'},
            'te': {'google': 'te-IN', 'azure': 'te-IN', 'local': 'telugu'}
        }
        
        # Voice personas for different user types
        self.voice_personas = {
            'student': {
                'tone': 'friendly',
                'speed': 'normal',
                'pitch': 'medium',
                'style': 'conversational'
            },
            'professional': {
                'tone': 'professional',
                'speed': 'normal',
                'pitch': 'medium',
                'style': 'formal'
            },
            'farmer': {
                'tone': 'supportive',
                'speed': 'slow',
                'pitch': 'low',
                'style': 'simple'
            },
            'senior_citizen': {
                'tone': 'respectful',
                'speed': 'slow',
                'pitch': 'medium',
                'style': 'clear'
            }
        }
    
    def setup_voice_engines(self):
        """Initialize voice processing engines"""
        try:
            # Speech Recognition
            if STT_TTS_AVAILABLE:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                
                # Adjust for ambient noise
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Text-to-Speech
                self.tts_engine = pyttsx3.init()
                self.configure_tts_engine()
                
                self.logger.info("✅ Basic STT/TTS engines initialized")
            
            # Advanced TTS with Coqui
            if COQUI_AVAILABLE:
                try:
                    # Load multilingual TTS model
                    self.coqui_tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts")
                    self.offline_tts_available = True
                    self.logger.info("✅ Coqui TTS initialized for offline multilingual support")
                except Exception as e:
                    self.logger.warning(f"⚠️ Coqui TTS initialization failed: {e}")
                    self.offline_tts_available = False
            
            # Google Cloud Speech (if credentials available)
            if GOOGLE_CLOUD_AVAILABLE and os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
                self.google_speech_client = speech.SpeechClient()
                self.google_tts_client = texttospeech.TextToSpeechClient()
                self.google_cloud_available = True
                self.logger.info("✅ Google Cloud Speech services initialized")
            else:
                self.google_cloud_available = False
                
        except Exception as e:
            self.logger.error(f"❌ Error setting up voice engines: {e}")
    
    def configure_tts_engine(self):
        """Configure the TTS engine settings"""
        if STT_TTS_AVAILABLE and hasattr(self, 'tts_engine'):
            # Set voice properties
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer female voice for better clarity
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 150)  # Words per minute
            self.tts_engine.setProperty('volume', 0.8)  # Volume level (0.0 to 1.0)
    
    def setup_language_models(self):
        """Setup language-specific models and configurations"""
        try:
            # Language-specific wake words
            self.wake_words = {
                'en': ['jarvis', 'jarvisfi', 'hey jarvis'],
                'ta': ['ஜார்விஸ்', 'ஜார்விஸ்ஃபை'],
                'hi': ['जार्विस', 'जार्विसफाई'],
                'te': ['జార్విస్', 'జార్విస్ఫై']
            }
            
            # Common financial terms in different languages
            self.financial_terms = {
                'en': {
                    'money': ['money', 'cash', 'funds', 'rupees'],
                    'save': ['save', 'savings', 'deposit'],
                    'invest': ['invest', 'investment', 'mutual fund', 'sip'],
                    'loan': ['loan', 'credit', 'emi', 'debt'],
                    'budget': ['budget', 'expense', 'spending']
                },
                'ta': {
                    'money': ['பணம்', 'காசு', 'ரூபாய்'],
                    'save': ['சேமிப்பு', 'சேமிக்க'],
                    'invest': ['முதலீடு', 'முதலீடு செய்ய'],
                    'loan': ['கடன்', 'வட்டி'],
                    'budget': ['பட்ஜெட்', 'செலவு']
                },
                'hi': {
                    'money': ['पैसा', 'रुपया', 'धन'],
                    'save': ['बचत', 'बचाना'],
                    'invest': ['निवेश', 'निवेश करना'],
                    'loan': ['ऋण', 'कर्ज', 'लोन'],
                    'budget': ['बजट', 'खर्च']
                },
                'te': {
                    'money': ['డబ్బు', 'రూపాయి', 'ధనం'],
                    'save': ['పొదుపు', 'సేవ్'],
                    'invest': ['పెట్టుబడి', 'ఇన్వెస్ట్'],
                    'loan': ['రుణం', 'లోన్'],
                    'budget': ['బడ్జెట్', 'ఖర్చు']
                }
            }
            
            self.logger.info("✅ Language models configured")
            
        except Exception as e:
            self.logger.error(f"❌ Error setting up language models: {e}")
    
    async def speech_to_text(self, 
                           audio_data: bytes, 
                           language: str = 'en',
                           user_type: str = 'professional') -> Dict[str, Any]:
        """
        Convert speech to text with multilingual support
        """
        try:
            result = {
                'text': '',
                'confidence': 0.0,
                'language': language,
                'processing_time': 0,
                'method': 'unknown'
            }
            
            start_time = asyncio.get_event_loop().time()
            
            # Try Google Cloud Speech first (highest accuracy)
            if self.google_cloud_available:
                try:
                    text, confidence = await self.google_speech_to_text(audio_data, language)
                    if text:
                        result.update({
                            'text': text,
                            'confidence': confidence,
                            'method': 'google_cloud'
                        })
                except Exception as e:
                    self.logger.warning(f"Google Cloud STT failed: {e}")
            
            # Fallback to local speech recognition
            if not result['text'] and STT_TTS_AVAILABLE:
                try:
                    text, confidence = await self.local_speech_to_text(audio_data, language)
                    if text:
                        result.update({
                            'text': text,
                            'confidence': confidence,
                            'method': 'local'
                        })
                except Exception as e:
                    self.logger.warning(f"Local STT failed: {e}")
            
            # Post-process text for financial context
            if result['text']:
                result['text'] = self.enhance_financial_text(result['text'], language)
                result['intent'] = self.classify_voice_intent(result['text'], language)
            
            result['processing_time'] = asyncio.get_event_loop().time() - start_time
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Speech to text error: {e}")
            return {
                'text': '',
                'confidence': 0.0,
                'language': language,
                'error': str(e),
                'method': 'error'
            }
    
    async def text_to_speech(self, 
                           text: str, 
                           language: str = 'en',
                           user_type: str = 'professional') -> Dict[str, Any]:
        """
        Convert text to speech with multilingual support and user-specific voice personas
        """
        try:
            result = {
                'audio_data': None,
                'duration': 0,
                'language': language,
                'user_type': user_type,
                'method': 'unknown'
            }
            
            # Get voice persona settings
            persona = self.voice_personas.get(user_type, self.voice_personas['professional'])
            
            # Try Coqui TTS first (best multilingual support)
            if self.offline_tts_available:
                try:
                    audio_data = await self.coqui_text_to_speech(text, language, persona)
                    if audio_data:
                        result.update({
                            'audio_data': audio_data,
                            'method': 'coqui_offline'
                        })
                except Exception as e:
                    self.logger.warning(f"Coqui TTS failed: {e}")
            
            # Try Google Cloud TTS
            if not result['audio_data'] and self.google_cloud_available:
                try:
                    audio_data = await self.google_text_to_speech(text, language, persona)
                    if audio_data:
                        result.update({
                            'audio_data': audio_data,
                            'method': 'google_cloud'
                        })
                except Exception as e:
                    self.logger.warning(f"Google Cloud TTS failed: {e}")
            
            # Fallback to local TTS
            if not result['audio_data'] and STT_TTS_AVAILABLE:
                try:
                    audio_data = await self.local_text_to_speech(text, language, persona)
                    if audio_data:
                        result.update({
                            'audio_data': audio_data,
                            'method': 'local'
                        })
                except Exception as e:
                    self.logger.warning(f"Local TTS failed: {e}")
            
            # Calculate duration
            if result['audio_data']:
                result['duration'] = len(result['audio_data']) / (self.voice_config['sample_rate'] * 2)
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Text to speech error: {e}")
            return {
                'audio_data': None,
                'error': str(e),
                'language': language,
                'method': 'error'
            }
    
    async def google_speech_to_text(self, audio_data: bytes, language: str) -> Tuple[str, float]:
        """Use Google Cloud Speech-to-Text"""
        if not self.google_cloud_available:
            raise Exception("Google Cloud not available")
        
        # Configure recognition
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.voice_config['sample_rate'],
            language_code=self.language_codes[language]['google'],
            enable_automatic_punctuation=True,
            model='latest_long'
        )
        
        audio = speech.RecognitionAudio(content=audio_data)
        
        # Perform recognition
        response = self.google_speech_client.recognize(config=config, audio=audio)
        
        if response.results:
            result = response.results[0]
            return result.alternatives[0].transcript, result.alternatives[0].confidence
        
        return '', 0.0
    
    async def local_speech_to_text(self, audio_data: bytes, language: str) -> Tuple[str, float]:
        """Use local speech recognition"""
        if not STT_TTS_AVAILABLE:
            raise Exception("Local STT not available")
        
        # Convert audio data to AudioData object
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file.flush()
            
            with sr.AudioFile(temp_file.name) as source:
                audio = self.recognizer.record(source)
        
        try:
            # Use Google Web Speech API (free tier)
            text = self.recognizer.recognize_google(
                audio, 
                language=self.language_codes[language]['google']
            )
            return text, 0.8  # Estimated confidence
        except sr.UnknownValueError:
            return '', 0.0
        except sr.RequestError:
            # Fallback to offline recognition if available
            try:
                text = self.recognizer.recognize_sphinx(audio)
                return text, 0.6
            except:
                return '', 0.0
    
    async def coqui_text_to_speech(self, text: str, language: str, persona: Dict) -> bytes:
        """Use Coqui TTS for offline multilingual speech synthesis"""
        if not self.offline_tts_available:
            raise Exception("Coqui TTS not available")
        
        # Generate speech
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            self.coqui_tts.tts_to_file(
                text=text,
                file_path=temp_file.name,
                speaker_wav=None,  # Use default speaker
                language=language
            )
            
            # Read the generated audio
            with open(temp_file.name, 'rb') as audio_file:
                return audio_file.read()
    
    async def google_text_to_speech(self, text: str, language: str, persona: Dict) -> bytes:
        """Use Google Cloud Text-to-Speech"""
        if not self.google_cloud_available:
            raise Exception("Google Cloud TTS not available")
        
        # Configure synthesis
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code=self.language_codes[language]['google'],
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            speaking_rate=1.0 if persona['speed'] == 'normal' else 0.8,
            pitch=0.0
        )
        
        # Perform synthesis
        response = self.google_tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        return response.audio_content
    
    async def local_text_to_speech(self, text: str, language: str, persona: Dict) -> bytes:
        """Use local TTS engine"""
        if not STT_TTS_AVAILABLE:
            raise Exception("Local TTS not available")
        
        # Configure TTS based on persona
        if persona['speed'] == 'slow':
            self.tts_engine.setProperty('rate', 120)
        elif persona['speed'] == 'fast':
            self.tts_engine.setProperty('rate', 180)
        else:
            self.tts_engine.setProperty('rate', 150)
        
        # Generate speech to temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            self.tts_engine.save_to_file(text, temp_file.name)
            self.tts_engine.runAndWait()
            
            # Read the generated audio
            with open(temp_file.name, 'rb') as audio_file:
                return audio_file.read()
    
    def enhance_financial_text(self, text: str, language: str) -> str:
        """Enhance recognized text with financial context"""
        try:
            # Common speech recognition errors in financial context
            corrections = {
                'en': {
                    'sip': ['ship', 'zip', 'tip'],
                    'mutual fund': ['mutual fun', 'mutual found'],
                    'investment': ['in west mint', 'invest mint'],
                    'rupees': ['rupee', 'rupi', 'roopee'],
                    'budget': ['budge it', 'but get']
                },
                'ta': {
                    'முதலீடு': ['முதலிடு', 'முதலீது'],
                    'சேமிப்பு': ['சேமிப்பூ', 'சேமிப்பு'],
                    'பணம்': ['பனம்', 'பணம்']
                }
            }
            
            if language in corrections:
                for correct_term, wrong_terms in corrections[language].items():
                    for wrong_term in wrong_terms:
                        text = text.replace(wrong_term, correct_term)
            
            return text.strip()
            
        except Exception as e:
            self.logger.error(f"❌ Error enhancing text: {e}")
            return text
    
    def classify_voice_intent(self, text: str, language: str) -> str:
        """Classify the intent of voice input"""
        try:
            text_lower = text.lower()
            
            # Intent keywords by language
            intent_keywords = {
                'budget': self.financial_terms[language].get('budget', []),
                'savings': self.financial_terms[language].get('save', []),
                'investment': self.financial_terms[language].get('invest', []),
                'loan': self.financial_terms[language].get('loan', []),
                'general': ['help', 'what', 'how', 'tell me']
            }
            
            # Check for intent matches
            for intent, keywords in intent_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    return intent
            
            return 'general'
            
        except Exception as e:
            self.logger.error(f"❌ Error classifying intent: {e}")
            return 'general'
    
    async def process_voice_command(self, 
                                  audio_data: bytes, 
                                  user_profile: Dict,
                                  language: str = 'en') -> Dict[str, Any]:
        """
        Complete voice command processing pipeline
        """
        try:
            user_type = user_profile.get('basic_info', {}).get('user_type', 'professional')
            
            # Speech to text
            stt_result = await self.speech_to_text(audio_data, language, user_type)
            
            if not stt_result['text']:
                return {
                    'success': False,
                    'error': 'Could not understand speech',
                    'stt_result': stt_result
                }
            
            # Process the recognized text
            processed_result = {
                'success': True,
                'recognized_text': stt_result['text'],
                'confidence': stt_result['confidence'],
                'intent': stt_result.get('intent', 'general'),
                'language': language,
                'user_type': user_type,
                'processing_method': stt_result['method'],
                'processing_time': stt_result.get('processing_time', 0)
            }
            
            return processed_result
            
        except Exception as e:
            self.logger.error(f"❌ Error processing voice command: {e}")
            return {
                'success': False,
                'error': str(e),
                'recognized_text': '',
                'confidence': 0.0
            }
    
    def get_voice_capabilities(self) -> Dict[str, Any]:
        """Get current voice processing capabilities"""
        return {
            'stt_available': STT_TTS_AVAILABLE,
            'tts_available': STT_TTS_AVAILABLE,
            'offline_tts': self.offline_tts_available,
            'google_cloud': self.google_cloud_available,
            'supported_languages': list(self.language_codes.keys()),
            'voice_personas': list(self.voice_personas.keys()),
            'sample_rate': self.voice_config['sample_rate'],
            'multilingual_support': True
        }
