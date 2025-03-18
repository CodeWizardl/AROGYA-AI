import os
import logging
from gtts import gTTS
from core.api_client import get_groq_client
from core.utils import play_audio, convert_to_wav

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transcribe_with_groq(audio_filepath, model="whisper-large-v3"):
    """Transcribes audio using Groq's Whisper model."""
    client = get_groq_client()
    try:
        wav_filepath = convert_to_wav(audio_filepath)
        
        with open(wav_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                language="en"
            )
        
        if wav_filepath != audio_filepath:
            os.remove(wav_filepath)
            
        return transcription.text if transcription else "No transcription available."
    except FileNotFoundError:
        logger.error(f"Audio file not found: {audio_filepath}")
        return None
    except Exception as e:
        logger.error(f"Error in transcription: {e}")
        return None

def text_to_speech(input_text, output_filepath):
    """Converts text to speech using gTTS."""
    try:
        os.makedirs(os.path.dirname(output_filepath) if os.path.dirname(output_filepath) else '.', exist_ok=True)
        
        tts = gTTS(text=input_text, lang="en", slow=False)
        
        mp3_filepath = output_filepath
        if not output_filepath.lower().endswith('.mp3'):
            mp3_filepath = f"{os.path.splitext(output_filepath)[0]}.mp3"
        
        tts.save(mp3_filepath)
        logger.info(f"Generated speech saved to {mp3_filepath}")
        
        try:
            play_audio(mp3_filepath)
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
            
        return mp3_filepath
    except Exception as e:
        logger.error(f"Error in TTS: {e}")
        return None