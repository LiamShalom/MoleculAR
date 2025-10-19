import os
import requests
from typing import Dict, Any, Optional
import logging
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

class VoiceGenerator:
    """
    Handles voice generation using ElevenLabs API
    """
    
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY', 'your-elevenlabs-api-key')
        self.base_url = 'https://api.elevenlabs.io/v1'
        self.default_voice_id = 'pNInz6obpgDQGcFmaJgB'  # Adam voice
        self.headers = {
            'Accept': 'audio/mpeg',
            'Content-Type': 'application/json',
            'xi-api-key': self.api_key
        }
    
    async def generate_voice(self, text: str, voice_settings: Optional[Dict[str, float]] = None) -> str:
        """
        Generate voice narration from text using ElevenLabs
        """
        try:
            if not self.api_key or self.api_key == 'your-elevenlabs-api-key':
                logger.warning("ElevenLabs API key not configured, returning mock audio URL")
                return "https://example.com/mock-audio.mp3"
            
            # Prepare voice settings
            settings = voice_settings or {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            }
            
            # Prepare request data
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": settings
            }
            
            # Make API request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/text-to-speech/{self.default_voice_id}",
                    headers=self.headers,
                    json=data
                ) as response:
                    
                    if response.status == 200:
                        # Save audio to temporary file
                        audio_data = await response.read()
                        audio_filename = f"temp_audio_{hash(text)}.mp3"
                        audio_path = f"temp/{audio_filename}"
                        
                        # Ensure temp directory exists
                        os.makedirs("temp", exist_ok=True)
                        
                        with open(audio_path, "wb") as f:
                            f.write(audio_data)
                        
                        # Return URL to the audio file
                        return f"/temp/{audio_filename}"
                    
                    else:
                        error_text = await response.text()
                        logger.error(f"ElevenLabs API error: {response.status} - {error_text}")
                        raise Exception(f"Voice generation failed: {error_text}")
            
        except Exception as e:
            logger.error(f"Voice generation failed: {str(e)}")
            # Return mock audio URL as fallback
            return "https://example.com/mock-audio.mp3"
    
    async def get_available_voices(self) -> List[Dict[str, Any]]:
        """
        Get list of available voices
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/voices",
                    headers=self.headers
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return data.get('voices', [])
                    else:
                        logger.error(f"Failed to get voices: {response.status}")
                        return []
        
        except Exception as e:
            logger.error(f"Failed to get available voices: {str(e)}")
            return []
    
    def _clean_text_for_speech(self, text: str) -> str:
        """
        Clean text for better speech synthesis
        """
        # Remove markdown formatting
        text = text.replace('**', '').replace('*', '')
        text = text.replace('`', '').replace('```', '')
        
        # Replace chemical notation with spoken form
        text = text.replace('SMILES:', 'SMILES string:')
        text = text.replace('kcal/mol', 'kilocalories per mole')
        text = text.replace('Da', 'Daltons')
        text = text.replace('Ų', 'square Angstroms')
        
        # Add pauses for better speech
        text = text.replace('.', '. ')
        text = text.replace(',', ', ')
        
        return text.strip()
    
    async def generate_voice_with_cleaning(self, text: str, voice_settings: Optional[Dict[str, float]] = None) -> str:
        """
        Generate voice with text cleaning
        """
        cleaned_text = self._clean_text_for_speech(text)
        return await self.generate_voice(cleaned_text, voice_settings)
