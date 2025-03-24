"""
Sesame CSM-1B Voice Generator App
A modern web application for generating speech using Sesame's CSM-1B model.
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
    Generate speech from text and return the audio file path and status message.
    
    Args:
        text (str): Text to convert to speech
        voice_preset (str, optional): Voice preset to use
        
    Returns:
        tuple: (audio_path, status_message)
    """
    if not text:
        return None, "Please enter some text to convert to speech.", None
    
    print(f"Generating speech for: {text}")
    print(f"Voice preset: {voice_preset if voice_preset else 'default'}")
    
    # Show processing indicator
    processing_message = "Processing... This may take a moment."
    
    result = tts_client.generate_speech(text, voice_preset=voice_preset if voice_preset else None)
    
    if result:
        return result, "✅ Speech generated successfully!", "success"
    else:
        return None, "❌ The Hugging Face API is currently unavailable. Please try again later.", "error"

# CSS for styling
css = """
.container {
    max-width: 1000px;
    margin: auto;
    padding-top: 1.5rem;
}

#header {
    text-align: center;
    margin-bottom: 2rem;
}

#header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

#header p {
    font-size: 1.2rem;
    color: #666;
}

.input-panel {
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    background: white;
    margin-bottom: 1.5rem;
}

.output-panel {
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    background: white;
}

.generate-btn {
    background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
    border: none;
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}

.generate-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.status-success {
    color: #10B981;
    font-weight: bold;
}

.status-error {
    color: #EF4444;
    font-weight: bold;
}

.about-section {
    margin-top: 2rem;
    padding: 1.5rem;
    border-radius: 12px;
    background: #f9f9f9;
}

.about-section h2 {
    color: #333;
    margin-top: 0;
}

.footer {
    text-align: center;
    margin-top: 2rem;
    color: #666;
    font-size: 0.9rem;
}

/* Custom colors for gradio components */
.gradio-container {
    background: #f5f7fa;
}

.gr-button {
    background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
    color: white;
}

.gr-panel {
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.gr-box {
    border-radius: 8px;
}
"""

# Create the Gradio interface
with gr.Blocks(css=css, title="Sesame CSM-1B Voice Generator", theme=gr.themes.Soft()) as demo:
    with gr.Column(elem_classes="container"):
        with gr.Column(elem_id="header"):
            gr.Markdown("# Sesame CSM-1B Voice Generator")
            gr.Markdown("Generate natural-sounding speech using state-of-the-art AI technology")
        
        with gr.Row():
            with gr.Column(elem_classes="input-panel"):
                gr.Markdown("### Input")
                text_input = gr.Textbox(
                    label="Text to speak", 
                    lines=5, 
                    placeholder="Enter the text you want to convert to speech...",
                    elem_id="text-input"
                )
                voice_preset = gr.Textbox(
                    label="Voice Preset (optional)", 
                    placeholder="Leave empty for default voice",
                    elem_id="voice-preset"
                )
                generate_button = gr.Button("Generate Speech", elem_classes="generate-btn")
            
            with gr.Column(elem_classes="output-panel"):
                gr.Markdown("### Output")
                audio_output = gr.Audio(label="Generated Speech", elem_id="audio-output")
                status = gr.Textbox(
                    label="Status", 
                    interactive=False,
                    placeholder="Status will appear here...",
                    elem_id="status-message"
                )
                
        with gr.Column(elem_classes="about-section"):
            gr.Markdown("""
            ## About This Tool
            
            This application uses Sesame's CSM-1B voice AI model through Hugging Face's API to generate realistic speech from text input.
            
            ### How to Use
            
            1. Enter the text you want to convert to speech in the input box
            2. Optionally specify a voice preset (if available)
            3. Click "Generate Speech" button
            4. Wait for processing (may take a few seconds)
            5. Listen to or download the generated audio
            
            ### Note
            
            If you encounter a "Service Unavailable" message, the Hugging Face API might be experiencing high traffic or maintenance. 
            The application will automatically retry a few times, but if that fails, please try again later.
            """)
            
        with gr.Column(elem_classes="footer"):
            gr.Markdown("Created with Gradio • Powered by Sesame CSM-1B")
                
    # Define the function to update the status message style based on success/error
    def update_status_style(message, status_type):
        if status_type == "success":
            return f"""<div class="status-success">{message}</div>"""
        elif status_type == "error":
            return f"""<div class="status-error">{message}</div>"""
        else:
            return message
            
    # Connect the generate button to the function
    generate_button.click(
        generate_speech, 
        inputs=[text_input, voice_preset], 
        outputs=[audio_output, status]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()