import os
import platform
import subprocess
from pydub import AudioSegment

def convert_to_wav(input_filepath):
    """Converts audio file to WAV format if it's not already."""
    if not input_filepath.lower().endswith('.wav'):
        output_filepath = input_filepath.rsplit('.', 1)[0] + '.wav'
        audio = AudioSegment.from_file(input_filepath)
        audio.export(output_filepath, format='wav')
        return output_filepath
    return input_filepath

def play_audio(audio_filepath):
    """Plays an audio file in a cross-platform way."""
    os_name = platform.system()
    try:
        if os_name == "Windows":
            wav_filepath = convert_to_wav(audio_filepath)
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])
            if wav_filepath != audio_filepath:
                os.remove(wav_filepath)
        elif os_name == "Darwin":  
            subprocess.run(['afplay', audio_filepath])
        elif os_name == "Linux":
            players = [
                ['aplay', audio_filepath],
                ['paplay', audio_filepath],
                ['mpg123', audio_filepath]
            ]
            for player in players:
                try:
                    subprocess.run(player, check=True)
                    break
                except (subprocess.SubprocessError, FileNotFoundError):
                    continue
            else:
                raise OSError("No suitable audio player found")
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")