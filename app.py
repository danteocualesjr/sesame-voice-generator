"""
Sesame CSM-1B Voice Generator App
A simple web application for generating speech using Sesame's CSM-1B model.
"""

import os
import gradio as gr
from sesame_tts import SesameTTS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Sesame TTS client
try:
    tts_client = SesameTTS()
except ValueError as e:
    print(f"Error: {e}")
    print("Please set your Hugging Face API token in .env file")
    exit(1)

def generate_speech(text, voice_preset=None):
    """
    Generate speech from text and return the audio file path.
    
    Args:
        text (str): Text to convert to speech
        voice_preset (str, optional): Voice preset to use
        
    Returns:
        str: Path to the generated audio file
    """
    if not text:
        return None
    
    return tts_client.generate_speech(text, voice_preset=voice_preset if voice_preset else None)

# Create the Gradio interface
with gr.Blocks(title="Sesame CSM-1B Voice Generator") as demo:
    gr.Markdown("# Sesame CSM-1B Voice Generator")
    gr.Markdown("Generate natural-sounding speech using Sesame's CSM-1B model")
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Text to speak", 
                lines=5, 
                placeholder="Enter the text you want to convert to speech..."
            )
            voice_preset = gr.Textbox(
                label="Voice Preset (optional)", 
                placeholder="Leave empty for default voice"
            )
            generate_button = gr.Button("Generate Speech")
        
        with gr.Column():
            audio_output = gr.Audio(label="Generated Speech")
            
    generate_button.click(
        generate_speech, 
        inputs=[text_input, voice_preset], 
        outputs=audio_output
    )
    
    gr.Markdown("""
    ## About
    This application uses Sesame's CSM-1B voice AI model through Hugging Face's API.
    
    ### How to Use
    1. Enter the text you want to convert to speech
    2. Optionally specify a voice preset
    3. Click "Generate Speech"
    4. Listen to the generated audio
    
    ### Note
    The first generation might take longer as the model loads.
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch()