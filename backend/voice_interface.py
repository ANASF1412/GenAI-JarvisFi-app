#!/usr/bin/env python3
"""
Multilingual Voice Interface for Personal Finance Chatbot
Supports Telugu, Hindi, Tamil, and English with STT/TTS
"""

import os
import io
import logging
import tempfile
from typing import Dict, List, Optional, Tuple, Any
import json
import asyncio
from datetime import datetime

# Speech Recognition and TTS
try:
    import speech_recognition as sr
    from gtts import gTTS
    import pygame
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

# Whisper for better STT
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

# Coqui TTS for offline support
try:
    from TTS.api import TTS
    COQUI_AVAILABLE = True
except ImportError:
    COQUI_AVAILABLE = False

# Audio processing
try:
    import librosa
    import soundfile as sf
    import numpy as np
    AUDIO_PROCESSING_AVAILABLE = True
except ImportError:
    AUDIO_PROCESSING_AVAILABLE = False

class VoiceInterface:
    """
    Comprehensive voice interface supporting multiple Indian languages
    """
    
    def __init__(self):
        """Initialize voice interface"""
        self.logger = self._setup_logger()
        
        # Language configurations
        self.supported_languages = {
            'english': {'code': 'en', 'gtts': 'en', 'whisper': 'en'},
            'hindi': {'code': 'hi', 'gtts': 'hi', 'whisper': 'hi'},
            'tamil': {'code': 'ta', 'gtts': 'ta', 'whisper': 'ta'},
            'telugu': {'code': 'te', 'gtts': 'te', 'whisper': 'te'},
            'bengali': {'code': 'bn', 'gtts': 'bn', 'whisper': 'bn'},
            'gujarati': {'code': 'gu', 'gtts': 'gu', 'whisper': 'gu'},
            'kannada': {'code': 'kn', 'gtts': 'kn', 'whisper': 'kn'},
            'malayalam': {'code': 'ml', 'gtts': 'ml', 'whisper': 'ml'},
            'marathi': {'code': 'mr', 'gtts': 'mr', 'whisper': 'mr'},
            'punjabi': {'code': 'pa', 'gtts': 'pa', 'whisper': 'pa'}
        }
        
        # Initialize components
        self._setup_speech_recognition()
        self._setup_tts_engines()
        self._setup_audio_processing()
        
        # Voice settings
        self.audio_format = 'wav'
        self.sample_rate = 16000
        self.chunk_size = 1024
        
        # Farmer-friendly features
        self.number_menu_enabled = True
        self.voice_commands = self._setup_voice_commands()
        
        self.logger.info("Voice interface initialized")
    
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
    
    def _setup_speech_recognition(self):
        """Setup speech recognition engines"""
        self.recognizers = {}
        
        try:
            if SPEECH_AVAILABLE:
                self.recognizers['google'] = sr.Recognizer()
                self.microphone = sr.Microphone()
                
                # Adjust for ambient noise
                with self.microphone as source:
                    self.recognizers['google'].adjust_for_ambient_noise(source)
                
                self.logger.info("Google Speech Recognition initialized")
            
            if WHISPER_AVAILABLE:
                # Load Whisper model (base model for balance of speed/accuracy)
                self.whisper_model = whisper.load_model("base")
                self.logger.info("Whisper model loaded")
            
        except Exception as e:
            self.logger.error(f"Speech recognition setup failed: {e}")
    
    def _setup_tts_engines(self):
        """Setup Text-to-Speech engines"""
        self.tts_engines = {}
        
        try:
            if COQUI_AVAILABLE:
                # Initialize Coqui TTS for offline support
                self.coqui_tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts")
                self.logger.info("Coqui TTS initialized")
            
            # Initialize pygame for audio playback
            if SPEECH_AVAILABLE:
                pygame.mixer.init()
                self.logger.info("Audio playback initialized")
                
        except Exception as e:
            self.logger.error(f"TTS setup failed: {e}")
    
    def _setup_audio_processing(self):
        """Setup audio processing capabilities"""
        try:
            if AUDIO_PROCESSING_AVAILABLE:
                self.audio_processor = {
                    'sample_rate': 16000,
                    'channels': 1,
                    'format': 'float32'
                }
                self.logger.info("Audio processing initialized")
        except Exception as e:
            self.logger.error(f"Audio processing setup failed: {e}")
    
    def _setup_voice_commands(self) -> Dict:
        """Setup voice commands for different languages"""
        return {
            'english': {
                'help': ['help', 'assist', 'support'],
                'repeat': ['repeat', 'say again', 'pardon'],
                'yes': ['yes', 'correct', 'right', 'okay'],
                'no': ['no', 'wrong', 'incorrect', 'cancel'],
                'menu': ['menu', 'options', 'choices'],
                'back': ['back', 'previous', 'return'],
                'exit': ['exit', 'quit', 'bye', 'goodbye']
            },
            'hindi': {
                'help': ['मदद', 'सहायता', 'हेल्प'],
                'repeat': ['दोहराएं', 'फिर से कहें', 'रिपीट'],
                'yes': ['हां', 'जी हां', 'सही', 'ठीक'],
                'no': ['नहीं', 'गलत', 'रद्द करें'],
                'menu': ['मेनू', 'विकल्प', 'चुनाव'],
                'back': ['वापस', 'पिछला', 'रिटर्न'],
                'exit': ['बाहर निकलें', 'बंद करें', 'अलविदा']
            },
            'tamil': {
                'help': ['உதவி', 'சहायता', 'ஹெல்ப்'],
                'repeat': ['மீண்டும் சொல்லுங்கள்', 'ரிபீட்'],
                'yes': ['ஆம்', 'சரி', 'ஓகே'],
                'no': ['இல்லை', 'தவறு', 'ரத்து செய்'],
                'menu': ['மெனு', 'விருப்பங்கள்', 'தேர்வுகள்'],
                'back': ['பின்னால்', 'முந்தைய', 'திரும்பு'],
                'exit': ['வெளியேறு', 'முடி', 'பை']
            },
            'telugu': {
                'help': ['సహాయం', 'హెల్ప్', 'మద్దతు'],
                'repeat': ['మళ్ళీ చెప్పండి', 'రిపీట్'],
                'yes': ['అవును', 'సరి', 'ఓకే'],
                'no': ['లేదు', 'తప్పు', 'రద్దు చేయి'],
                'menu': ['మెనూ', 'ఎంపికలు', 'ఎంపికలు'],
                'back': ['వెనుకకు', 'మునుపటి', 'తిరిగి'],
                'exit': ['నిష్క్రమించు', 'ముగించు', 'బై']
            }
        }
    
    def speech_to_text(self, audio_file: str = None, language: str = 'english') -> Dict:
        """Convert speech to text using multiple engines"""
        try:
            result = {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'language_detected': language,
                'engine_used': '',
                'processing_time': 0.0
            }
            
            start_time = datetime.now()
            
            # Try Whisper first (more accurate for Indian languages)
            if WHISPER_AVAILABLE and audio_file:
                try:
                    whisper_result = self.whisper_model.transcribe(
                        audio_file, 
                        language=self.supported_languages[language]['whisper']
                    )
                    
                    result.update({
                        'success': True,
                        'text': whisper_result['text'].strip(),
                        'confidence': 0.9,  # Whisper doesn't provide confidence
                        'engine_used': 'whisper'
                    })
                    
                    self.logger.info(f"Whisper STT successful: {result['text'][:50]}...")
                    
                except Exception as e:
                    self.logger.warning(f"Whisper STT failed: {e}")
            
            # Fallback to Google Speech Recognition
            if not result['success'] and SPEECH_AVAILABLE:
                try:
                    if audio_file:
                        # Process audio file
                        with sr.AudioFile(audio_file) as source:
                            audio = self.recognizers['google'].record(source)
                    else:
                        # Record from microphone
                        with self.microphone as source:
                            self.logger.info("Listening...")
                            audio = self.recognizers['google'].listen(source, timeout=5, phrase_time_limit=10)
                    
                    # Recognize speech
                    lang_code = self.supported_languages[language]['code']
                    text = self.recognizers['google'].recognize_google(audio, language=lang_code)
                    
                    result.update({
                        'success': True,
                        'text': text.strip(),
                        'confidence': 0.8,  # Google doesn't provide confidence
                        'engine_used': 'google'
                    })
                    
                    self.logger.info(f"Google STT successful: {result['text'][:50]}...")
                    
                except sr.UnknownValueError:
                    self.logger.warning("Could not understand audio")
                except sr.RequestError as e:
                    self.logger.error(f"Google STT request failed: {e}")
                except Exception as e:
                    self.logger.error(f"Google STT failed: {e}")
            
            # Calculate processing time
            result['processing_time'] = (datetime.now() - start_time).total_seconds()
            
            # Post-process text
            if result['success']:
                result['text'] = self._post_process_text(result['text'], language)
                result['intent'] = self._extract_intent(result['text'], language)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Speech to text failed: {e}")
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'language_detected': language,
                'engine_used': 'none',
                'processing_time': 0.0,
                'error': str(e)
            }
    
    def text_to_speech(self, text: str, language: str = 'english', voice_speed: float = 1.0) -> Dict:
        """Convert text to speech with multiple engine support"""
        try:
            result = {
                'success': False,
                'audio_file': '',
                'engine_used': '',
                'processing_time': 0.0
            }
            
            start_time = datetime.now()
            
            # Create temporary file for audio
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            
            # Try Coqui TTS first (better quality, offline)
            if COQUI_AVAILABLE:
                try:
                    self.coqui_tts.tts_to_file(
                        text=text,
                        file_path=temp_file.name,
                        speaker_wav=None,  # Use default speaker
                        language=self.supported_languages[language]['code']
                    )
                    
                    result.update({
                        'success': True,
                        'audio_file': temp_file.name,
                        'engine_used': 'coqui'
                    })
                    
                    self.logger.info(f"Coqui TTS successful for: {text[:50]}...")
                    
                except Exception as e:
                    self.logger.warning(f"Coqui TTS failed: {e}")
            
            # Fallback to Google TTS
            if not result['success'] and SPEECH_AVAILABLE:
                try:
                    lang_code = self.supported_languages[language]['gtts']
                    tts = gTTS(text=text, lang=lang_code, slow=(voice_speed < 1.0))
                    tts.save(temp_file.name)
                    
                    result.update({
                        'success': True,
                        'audio_file': temp_file.name,
                        'engine_used': 'gtts'
                    })
                    
                    self.logger.info(f"Google TTS successful for: {text[:50]}...")
                    
                except Exception as e:
                    self.logger.error(f"Google TTS failed: {e}")
            
            # Calculate processing time
            result['processing_time'] = (datetime.now() - start_time).total_seconds()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Text to speech failed: {e}")
            return {
                'success': False,
                'audio_file': '',
                'engine_used': 'none',
                'processing_time': 0.0,
                'error': str(e)
            }
    
    def play_audio(self, audio_file: str) -> bool:
        """Play audio file"""
        try:
            if SPEECH_AVAILABLE and os.path.exists(audio_file):
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                
                # Wait for playback to complete
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                return True
            else:
                self.logger.warning(f"Cannot play audio file: {audio_file}")
                return False
                
        except Exception as e:
            self.logger.error(f"Audio playback failed: {e}")
            return False
    
    def _post_process_text(self, text: str, language: str) -> str:
        """Post-process recognized text"""
        try:
            # Remove extra whitespace
            text = ' '.join(text.split())
            
            # Language-specific post-processing
            if language == 'hindi':
                # Convert English numbers to Hindi if needed
                pass
            elif language == 'tamil':
                # Tamil-specific processing
                pass
            elif language == 'telugu':
                # Telugu-specific processing
                pass
            
            return text
            
        except Exception as e:
            self.logger.error(f"Text post-processing failed: {e}")
            return text
    
    def _extract_intent(self, text: str, language: str) -> str:
        """Extract intent from voice input"""
        try:
            text_lower = text.lower()
            
            # Get voice commands for the language
            commands = self.voice_commands.get(language, self.voice_commands['english'])
            
            # Check for specific intents
            for intent, keywords in commands.items():
                if any(keyword in text_lower for keyword in keywords):
                    return intent
            
            # Financial intent detection
            financial_keywords = {
                'english': {
                    'loan': ['loan', 'credit', 'borrow', 'debt'],
                    'savings': ['save', 'savings', 'deposit', 'invest'],
                    'budget': ['budget', 'expense', 'spending', 'money'],
                    'insurance': ['insurance', 'policy', 'coverage', 'claim']
                },
                'hindi': {
                    'loan': ['ऋण', 'कर्ज', 'लोन', 'उधार'],
                    'savings': ['बचत', 'जमा', 'निवेश', 'सेविंग'],
                    'budget': ['बजट', 'खर्च', 'पैसा', 'व्यय'],
                    'insurance': ['बीमा', 'पॉलिसी', 'कवरेज', 'दावा']
                },
                'tamil': {
                    'loan': ['கடன்', 'லோன்', 'கடன் வாங்க'],
                    'savings': ['சேமிப்பு', 'முதலீடு', 'சேவிங்'],
                    'budget': ['பட்ஜெட்', 'செலவு', 'பணம்'],
                    'insurance': ['காப்பீடு', 'பாலிசி', 'கவரேஜ்']
                },
                'telugu': {
                    'loan': ['రుణం', 'లోన్', 'అప్పు'],
                    'savings': ['పొదుపు', 'పెట్టుబడి', 'సేవింగ్'],
                    'budget': ['బడ్జెట్', 'ఖర్చు', 'డబ్బు'],
                    'insurance': ['భీమా', 'పాలసీ', 'కవరేజ్']
                }
            }
            
            lang_keywords = financial_keywords.get(language, financial_keywords['english'])
            for intent, keywords in lang_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    return f"financial_{intent}"
            
            return 'general_query'
            
        except Exception as e:
            self.logger.error(f"Intent extraction failed: {e}")
            return 'unknown'

    def create_number_menu(self, options: List[str], language: str = 'english') -> str:
        """Create number-based menu for low-literacy users"""
        try:
            menu_text = ""

            # Language-specific menu headers
            headers = {
                'english': "Please choose an option by saying the number:",
                'hindi': "कृपया नंबर बोलकर विकल्प चुनें:",
                'tamil': "எண்ணைச் சொல்லி விருப்பத்தைத் தேர்ந்தெடுக்கவும்:",
                'telugu': "దయచేసి సంఖ్యను చెప్పి ఎంపికను ఎంచుకోండి:"
            }

            menu_text += headers.get(language, headers['english']) + "\n\n"

            for i, option in enumerate(options, 1):
                menu_text += f"{i}. {option}\n"

            return menu_text

        except Exception as e:
            self.logger.error(f"Number menu creation failed: {e}")
            return "Menu creation failed"

    def process_voice_pipeline(self, audio_input: str, language: str = 'english') -> Dict:
        """Complete voice processing pipeline: STT → Process → TTS"""
        try:
            pipeline_result = {
                'success': False,
                'original_audio': audio_input,
                'recognized_text': '',
                'processed_response': '',
                'response_audio': '',
                'language': language,
                'processing_steps': [],
                'total_time': 0.0
            }

            start_time = datetime.now()

            # Step 1: Speech to Text
            stt_result = self.speech_to_text(audio_input, language)
            pipeline_result['processing_steps'].append({
                'step': 'speech_to_text',
                'success': stt_result['success'],
                'time': stt_result['processing_time'],
                'engine': stt_result['engine_used']
            })

            if not stt_result['success']:
                return pipeline_result

            pipeline_result['recognized_text'] = stt_result['text']

            # Step 2: Process the query (this would integrate with your main AI system)
            # For now, we'll create a simple response
            response_text = self._generate_response(stt_result['text'], language)
            pipeline_result['processed_response'] = response_text

            # Step 3: Text to Speech
            tts_result = self.text_to_speech(response_text, language)
            pipeline_result['processing_steps'].append({
                'step': 'text_to_speech',
                'success': tts_result['success'],
                'time': tts_result['processing_time'],
                'engine': tts_result['engine_used']
            })

            if tts_result['success']:
                pipeline_result['response_audio'] = tts_result['audio_file']
                pipeline_result['success'] = True

            # Calculate total processing time
            pipeline_result['total_time'] = (datetime.now() - start_time).total_seconds()

            return pipeline_result

        except Exception as e:
            self.logger.error(f"Voice pipeline processing failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'total_time': 0.0
            }

    def _generate_response(self, query: str, language: str) -> str:
        """Generate response for voice query (placeholder for AI integration)"""
        try:
            # This is a placeholder - in production, this would integrate with your main AI system
            responses = {
                'english': {
                    'greeting': "Hello! How can I help you with your finances today?",
                    'loan': "I can help you understand different types of loans and their requirements.",
                    'savings': "Let me help you create a savings plan that works for you.",
                    'budget': "I'll help you create and manage your budget effectively.",
                    'default': "I understand you're asking about finances. Let me help you with that."
                },
                'hindi': {
                    'greeting': "नमस्ते! आज मैं आपकी वित्तीय सहायता कैसे कर सकता हूं?",
                    'loan': "मैं आपको विभिन्न प्रकार के ऋण और उनकी आवश्यकताओं को समझने में मदद कर सकता हूं।",
                    'savings': "मैं आपके लिए एक बचत योजना बनाने में मदद करूंगा।",
                    'budget': "मैं आपको बजट बनाने और प्रबंधित करने में मदद करूंगा।",
                    'default': "मैं समझ गया कि आप वित्त के बारे में पूछ रहे हैं। मैं आपकी मदद करूंगा।"
                },
                'tamil': {
                    'greeting': "வணக்கம்! இன்று உங்கள் நிதி விஷயங்களில் நான் எப்படி உதவ முடியும்?",
                    'loan': "பல்வேறு வகையான கடன்கள் மற்றும் அவற்றின் தேவைகளை புரிந்துகொள்ள உதவுகிறேன்.",
                    'savings': "உங்களுக்கு ஏற்ற சேமிப்பு திட்டத்தை உருவாக்க உதவுகிறேன்.",
                    'budget': "பட்ஜெட் உருவாக்கி நிர்வகிக்க உதவுகிறேன்.",
                    'default': "நீங்கள் நிதி பற்றி கேட்கிறீர்கள் என்று புரிகிறது. உதவுகிறேன்."
                },
                'telugu': {
                    'greeting': "నమస్కారం! ఈరోజు మీ ఆర్థిక విషయాలలో నేను ఎలా సహాయం చేయగలను?",
                    'loan': "వివిధ రకాల రుణాలు మరియు వాటి అవసరాలను అర్థం చేసుకోవడంలో సహాయం చేస్తాను.",
                    'savings': "మీకు అనుకూలమైన పొదుపు ప్రణాళికను రూపొందించడంలో సహాయం చేస్తాను.",
                    'budget': "బడ్జెట్ రూపొందించి నిర్వహించడంలో సహాయం చేస్తాను.",
                    'default': "మీరు ఆర్థిక విషయాల గురించి అడుగుతున్నారని అర్థమైంది. సహాయం చేస్తాను."
                }
            }

            lang_responses = responses.get(language, responses['english'])

            # Simple intent-based response selection
            query_lower = query.lower()
            if any(word in query_lower for word in ['loan', 'ऋण', 'கடன்', 'రుణం']):
                return lang_responses['loan']
            elif any(word in query_lower for word in ['save', 'savings', 'बचत', 'சேமிப்பு', 'పొదుపు']):
                return lang_responses['savings']
            elif any(word in query_lower for word in ['budget', 'बजट', 'பட்ஜெட்', 'బడ్జెట్']):
                return lang_responses['budget']
            elif any(word in query_lower for word in ['hello', 'hi', 'नमस्ते', 'வணக்கம்', 'నమస్కారం']):
                return lang_responses['greeting']
            else:
                return lang_responses['default']

        except Exception as e:
            self.logger.error(f"Response generation failed: {e}")
            return "I'm sorry, I couldn't process your request right now."
