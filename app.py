"""
Sesame CSM-1B Voice Generator App
A modern web application for generating speech using Sesame's CSM-1B model,
with voice cloning capabilities.
"""

import os
import gradio as gr
from sesame_tts import SesameTTS
from voice_cloning import VoiceCloning
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the clients
try:
    tts_client = SesameTTS()
    voice_cloning = VoiceCloning()
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
        tuple: (audio_path, status_message, status_type)
    """
    if not text:
        return None, "Please enter some text to convert to speech.", None
    
    print(f"Generating speech for: {text}")
    print(f"Voice preset: {voice_preset if voice_preset else 'default'}")
    
    result = tts_client.generate_speech(text, voice_preset=voice_preset if voice_preset else None)
    
    if result:
        return result, "✅ Speech generated successfully!", "success"
    else:
        return None, "❌ The Hugging Face API is currently unavailable. Please try again later.", "error"

def generate_speech_with_cloned_voice(text, voice_name):
    """
    Generate speech using a cloned voice.
    
    Args:
        text (str): Text to convert to speech
        voice_name (str): Name of the cloned voice to use
        
    Returns:
        tuple: (audio_path, status_message, status_type)
    """
    if not text:
        return None, "Please enter some text to convert to speech.", None
    
    if not voice_name:
        return None, "Please select a cloned voice.", None
    
    print(f"Generating speech for: {text}")
    print(f"Using cloned voice: {voice_name}")
    
    result = voice_cloning.generate_speech_with_voice(text, voice_name)
    
    if result:
        return result, f"✅ Speech generated with voice '{voice_name}' successfully!", "success"
    else:
        return None, "❌ Failed to generate speech with the cloned voice. The API may be unavailable.", "error"

def clone_voice(audio_file, voice_name):
    """
    Clone a voice from an audio file.
    
    Args:
        audio_file (tuple): (file_path, file_name, content_type)
        voice_name (str): Name to give the cloned voice
        
    Returns:
        str: Status message
    """
    if audio_file is None:
        return "❌ Please upload an audio file."
    
    file_path = audio_file
    
    if not voice_name:
        return "❌ Please enter a name for the cloned voice."
    
    print(f"Cloning voice from: {file_path}")
    print(f"Voice name: {voice_name}")
    
    success = voice_cloning.extract_voice(file_path, voice_name)
    
    if success:
        return f"✅ Voice '{voice_name}' cloned successfully!"
    else:
        return "❌ Failed to clone voice. Please try again with a different audio file."

def refresh_voices():
    """
    Refresh the list of available cloned voices.
    
    Returns:
        list: Available voice names
        str: Status message
    """
    voices = voice_cloning.list_available_voices()
    if voices:
        return gr.Dropdown.update(choices=voices, value=voices[0] if voices else None), f"Found {len(voices)} cloned voices."
    else:
        return gr.Dropdown.update(choices=[], value=None), "No cloned voices found. Clone a voice first."

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

.panel {
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    background: white;
    margin-bottom: 1.5rem;
}

.btn {
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

.btn:hover {
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

.tab-nav button {
    font-weight: bold;
    font-size: 1.1rem;
    padding: 10px 20px;
}

.active-tab {
    border-bottom: 3px solid #4776E6;
}
"""

# Create the Gradio interface
with gr.Blocks(css=css, title="Sesame CSM-1B Voice Generator", theme=gr.themes.Soft()) as demo:
    with gr.Column(elem_classes="container"):
        with gr.Column(elem_id="header"):
            gr.Markdown("# Sesame CSM-1B Voice Generator")
            gr.Markdown("Generate natural-sounding speech with voice cloning capabilities")
        
        with gr.Tabs() as tabs:
            # Standard TTS Tab
            with gr.TabItem("Text to Speech", elem_classes="tab-nav") as standard_tab:
                with gr.Column(elem_classes="panel"):
                    gr.Markdown("### Generate Speech")
                    text_input = gr.Textbox(
                        label="Text to speak", 
                        lines=5, 
                        placeholder="Enter the text you want to convert to speech..."
                    )
                    voice_preset = gr.Textbox(
                        label="Voice Preset (optional)", 
                        placeholder="Leave empty for default voice"
                    )
                    generate_button = gr.Button("Generate Speech", elem_classes="btn")
                    
                    audio_output = gr.Audio(label="Generated Speech")
                    status = gr.Textbox(
                        label="Status", 
                        interactive=False,
                        placeholder="Status will appear here..."
                    )
            
            # Voice Cloning Tab
            with gr.TabItem("Voice Cloning", elem_classes="tab-nav") as cloning_tab:
                with gr.Column(elem_classes="panel"):
                    gr.Markdown("### Clone Your Voice")
                    gr.Markdown("Upload an audio file of your voice to create a voice model for synthesis.")
                    
                    audio_upload = gr.Audio(
                        label="Upload Voice Sample (5-10 seconds of clear speech recommended)",
                        type="filepath"
                    )
                    voice_name_input = gr.Textbox(
                        label="Voice Name", 
                        placeholder="Enter a name for this voice..."
                    )
                    
                    clone_button = gr.Button("Clone Voice", elem_classes="btn")
                    clone_status = gr.Textbox(
                        label="Cloning Status", 
                        interactive=False,
                        placeholder="Status will appear here..."
                    )
                
                with gr.Column(elem_classes="panel"):
                    gr.Markdown("### Generate Speech with Cloned Voice")
                    
                    cloned_text_input = gr.Textbox(
                        label="Text to speak", 
                        lines=5, 
                        placeholder="Enter the text you want to convert to speech..."
                    )
                    
                    with gr.Row():
                        cloned_voice_dropdown = gr.Dropdown(
                            label="Select Cloned Voice",
                            choices=voice_cloning.list_available_voices(),
                            interactive=True
                        )
                        refresh_button = gr.Button("🔄 Refresh", size="sm")
                    
                    cloned_voice_status = gr.Textbox(
                        label="Status",
                        interactive=False,
                        placeholder="Status will appear here..."
                    )
                    
                    generate_cloned_button = gr.Button("Generate Speech with Cloned Voice", elem_classes="btn")
                    cloned_audio_output = gr.Audio(label="Generated Speech")
                    cloned_status = gr.Textbox(
                        label="Status", 
                        interactive=False,
                        placeholder="Status will appear here..."
                    )
        
        with gr.Column(elem_classes="about-section"):
            gr.Markdown("""
            ## About This Tool
            
            This application uses Sesame's CSM-1B voice AI model through Hugging Face's API to generate realistic speech 
            and clone voices.
            
            ### Text to Speech
            
            Use the first tab to generate speech with the default voice or preset voices.
            
            ### Voice Cloning
            
            Use the second tab to:
            1. Clone your voice by uploading an audio sample
            2. Generate speech using your cloned voice
            
            ### Note
            
            If you encounter a "Service Unavailable" message, the Hugging Face API might be experiencing high traffic or 
            maintenance. The application will automatically retry a few times, but if that fails, please try again later.
            """)
            
        with gr.Column(elem_classes="footer"):
            gr.Markdown("Created with Gradio • Powered by Sesame CSM-1B")
                
    # Define connections
    generate_button.click(
        generate_speech, 
        inputs=[text_input, voice_preset], 
        outputs=[audio_output, status]
    )
    
    clone_button.click(
        clone_voice,
        inputs=[audio_upload, voice_name_input],
        outputs=[clone_status]
    )
    
    refresh_button.click(
        refresh_voices,
        inputs=[],
        outputs=[cloned_voice_dropdown, cloned_voice_status]
    )
    
    generate_cloned_button.click(
        generate_speech_with_cloned_voice,
        inputs=[cloned_text_input, cloned_voice_dropdown],
        outputs=[cloned_audio_output, cloned_status]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()