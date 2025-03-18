# Arogya AI - Your 24/7 Digital Health Assistant

Arogya AI is a multimodal digital health assistant that provides medical insights through text, voice, and image analysis. It allows users to describe their symptoms or medical concerns through text, voice recordings, or by uploading relevant medical images to receive AI-generated medical advice.

## Features

- **Text Input**: Describe your symptoms or ask medical questions through text.
- **Voice Input**: Record your symptoms using your microphone for automatic transcription.
- **Image Analysis**: Upload medical images for AI-powered visual analysis.
- **Voice Response**: Receive responses in both text and audio formats.
- **Professional Medical Insights**: Get comprehensive medical assessments based on the information you provide.

## Chatbot Interface

**Splash Screen**

![1](https://github.com/user-attachments/assets/1df59612-0ecf-4991-a06b-1c52d0577381)

**User Input & Customization**

![2](https://github.com/user-attachments/assets/64e45f6a-f251-495a-b2f5-1f388cbe0322)

**Generated Response**

![3](https://github.com/user-attachments/assets/851193ba-ede5-4148-9b65-30f8fa90f1f1)

## Technical Overview

Arogya AI leverages several advanced AI technologies to provide a seamless user experience:

![Architecture](https://github.com/user-attachments/assets/7ea87489-aa67-4f76-a887-a4e02d2300e6)

- **LLM Integration**: Uses Groq's LLama 3.2 (11B vision preview) for text processing and image analysis
- **Speech-to-Text**: Transcribes voice inputs for processing
- **Text-to-Speech**: Converts AI responses into natural-sounding speech
- **Gradio Interface**: Provides an intuitive web-based user interface

## Installation

### Prerequisites

- Python 3.7+
- Required API keys (Groq)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/CodeWizardl/AROGYA-AI.git
   cd AROGYA-AI
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Make sure you have the welcome audio file:
   ```
   welcome_message.mp3
   ```

5. Make sure you have a `logo.png` file in the project root directory.

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Access the interface through your web browser at `http://localhost:7860`.

3. Use the application in one of three ways:
   - Type your symptoms or questions in the text box
   - Record your voice using the microphone button
   - Upload a relevant medical image

4. Click "Get Medical Advice" to receive AI-generated medical insights.

## Project Structure

```
arogya-ai/
├── app.py                   # Main application file
├── core/
│   ├── __init__.py
│   ├── api_client.py        # API client for Groq
│   ├── image_processing.py  # Image analysis functions
│   ├── speech_processing.py # Voice transcription and TTS
│   └── utils.py             # Utility functions
├── output/                  # Directory for generated audio files
├── logo.png                 # Application logo
├── welcome_message.mp3      # Welcome audio message
├── .env                     # Environment variables
└── requirements.txt         # Project dependencies
```

## Dependencies

- `gradio`: Web interface
- `python-dotenv`: Environment variable management
- `groq`: API client for Groq LLM
- Additional dependencies for speech processing and image analysis

## Important Notes

- The system is designed to provide general medical insights and should not replace professional medical advice.
- User data is processed temporarily and not stored permanently.
- Internet connection is required for API calls to Groq.

## Future Work

- Store conversation history in a database for better user experience and analysis.
- Implement multilingual support to enhance accessibility for users worldwide.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
