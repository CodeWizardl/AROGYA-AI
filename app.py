import gradio as gr
from dotenv import load_dotenv
import os
import logging
import base64
from core.speech_processing import transcribe_with_groq, text_to_speech
from core.image_processing import analyze_image_with_query
from core.api_client import get_groq_client
from core.utils import play_audio  

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

system_prompt = """
You are a professional doctor providing medical insights based on visual observations and patient descriptions. Your role is to analyze both visual information and textual descriptions to offer a thoughtful assessment, considering potential medical concerns. If there are any visible abnormalities or described symptoms, provide a differential diagnosis with possible causes. Offer practical advice, including initial remedies or when to seek medical attention.

Structure your response as if you are speaking directly to a real patient, maintaining a compassionate and professional tone. Avoid technical jargon unless necessary, and explain in a way that is easy to understand. Present your observations naturally, such as: "Based on what I see and what you've described..." rather than referring to images or text analysis.

Your response should be clear, well-structured, and comprehensive, balancing brevity with enough detail to be informative. Use natural language and avoid unnecessary symbols or formatting. If multiple conditions are possible, list them logically and suggest appropriate next steps. Focus on providing value in a concise yet complete manner.
"""

def encode_image(image_path):
    """Encodes an image file to a base64 string."""
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' not found.")
        return ""
    
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Error encoding image: {e}")
        return ""

def process_inputs(text_input, audio_filepath, image_filepath):
    """Processes text, audio, and image inputs and generates a response."""
    try:
        query_text = ""
        
        if text_input and text_input.strip():
            query_text = text_input.strip()
            logger.info("Processing text input")
            
        elif audio_filepath:
            logger.info("Processing audio input")
            transcribed_text = transcribe_with_groq(audio_filepath)
            if transcribed_text:
                query_text = transcribed_text
                logger.info("Audio transcription successful")
            else:
                logger.warning("Audio transcription failed")
                
        if image_filepath:
            logger.info("Processing image input")
            full_query = f"{system_prompt}\n\nPatient's description: {query_text}" if query_text else system_prompt
            doctor_response = analyze_image_with_query(full_query, "llama-3.2-11b-vision-preview", image_filepath)
        elif query_text:
            logger.info("Generating text-only response")
            client = get_groq_client()
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query_text}
            ]
            response = client.chat.completions.create(
                messages=messages,
                model="llama-3.2-11b-vision-preview"
            )
            doctor_response = response.choices[0].message.content if response.choices else "No response available."
        else:
            logger.warning("No valid input provided")
            doctor_response = "Please provide either text input, audio input, or an image for analysis."

        output_filepath = os.path.join(os.getcwd(), "output", "response.mp3")
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        
        audio_file = text_to_speech(doctor_response, output_filepath)
        
        if not audio_file:
            logger.error("Failed to generate audio response")
            return query_text, doctor_response, None

        return query_text, doctor_response, audio_file
    except Exception as e:
        logger.error(f"Error in process_inputs: {e}")
        return "Error", f"An error occurred: {e}", None

def play_welcome_audio():
    """Play welcome audio and then switch to main interface."""
    try:
        welcome_audio_path = os.path.join(os.getcwd(), "welcome_message.mp3")
        if os.path.exists(welcome_audio_path):
            logger.info("Playing welcome audio message")
            play_audio(welcome_audio_path)
            logger.info("Welcome audio completed")
        else:
            logger.warning(f"Welcome audio file not found at: {welcome_audio_path}")
    except Exception as e:
        logger.error(f"Error playing welcome audio: {e}")
    
    return {splash_screen: gr.update(visible=False), main_interface: gr.update(visible=True)}

with gr.Blocks() as demo:
    show_main_interface = gr.State(False)
    
    # Splash screen
    with gr.Group(visible=True) as splash_screen:
        image_base64 = encode_image("logo.png")
        gr.HTML(f"""
            <div style="text-align: center; padding: 40px; background-color: #333333; color: white; border-radius: 10px;">
                {'<img src="data:image/png;base64,' + image_base64 + '" style="width: 150px; margin: 20px auto; display: block;" />' if image_base64 else ''}
                <h1 style="font-size: 50px; font-weight: bold; color: #2E86C1; margin-bottom: 10px;">AROGYA AI</h1>
                <h3 style="font-size: 25px">Your 24/7 Digital Health Assistant</h3>
            </div>
        """)

    
    # Main interface
    with gr.Group(visible=False) as main_interface:
        title="AI Doctor with Text, Voice, and Vision",
        description="Get medical insights by describing your symptoms through text, voice, or by uploading relevant medical images."
        
        with gr.Row():
            with gr.Column():
                text_input = gr.Textbox(
                    label="Describe your symptoms or ask a medical question",
                    placeholder="Example: I've been experiencing headaches and dizziness for the past week...",
                    lines=3
                )
                audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Or speak your symptoms (Optional)")
                image_input = gr.Image(type="filepath", label="Upload relevant medical image (Optional)")
                submit_btn = gr.Button("Get Medical Advice")
            
            with gr.Column():
                text_output = gr.Textbox(label="Your Input (Text/Transcribed)")
                response_output = gr.Textbox(label="Doctor's Response")
                audio_output = gr.Audio(label="Generated Voice Response")
        
        submit_btn.click(
            fn=process_inputs,
            inputs=[text_input, audio_input, image_input],
            outputs=[text_output, response_output, audio_output]
        )
    
    # Load event now calls play_welcome_audio which will play the audio and then switch to main interface
    demo.load(play_welcome_audio, [], [splash_screen, main_interface])

if __name__ == "__main__":
    demo.launch(debug=True)