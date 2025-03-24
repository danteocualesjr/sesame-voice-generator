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
:root {
    --primary-color: #7C3AED;
    --primary-light: #DDD6FE;
    --primary-dark: #5B21B6;
    --gradient-start: #7C3AED;
    --gradient-end: #2563EB;
    --text-primary: #1F2937;
    --text-secondary: #4B5563;
    --bg-color: #F9FAFB;
    --panel-bg: #FFFFFF;
    --success-color: #10B981;
    --error-color: #EF4444;
    --warning-color: #F59E0B;
    --radius-sm: 6px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    --transition: all 0.3s ease;
}

body {
    background-color: var(--bg-color);
    color: var(--text-primary);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.container {
    max-width: 1100px;
    margin: auto;
    padding: 2rem 1rem;
}

#header {
    text-align: center;
    margin-bottom: 2.5rem;
}

#header h1 {
    font-size: 2.75rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    background: linear-gradient(90deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent;
    letter-spacing: -0.025em;
}

#header p {
    font-size: 1.25rem;
    color: var(--text-secondary);
    max-width: 80%;
    margin: 0 auto;
}

.panel {
    border-radius: var(--radius-lg);
    padding: 1.75rem;
    box-shadow: var(--shadow-md);
    background: var(--panel-bg);
    margin-bottom: 1.75rem;
    border: 1px solid rgba(0,0,0,0.05);
    transition: var(--transition);
}

.panel:hover {
    box-shadow: var(--shadow-lg);
}

.btn {
    background: linear-gradient(90deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
    border: none;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius-md);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    opacity: 0.95;
}

.btn:active {
    transform: translateY(0);
}

.btn-secondary {
    background: white;
    color: var(--primary-color);
    border: 1px solid var(--primary-light);
}

.btn-secondary:hover {
    background: var(--primary-light);
    color: var(--primary-dark);
}

.status-success {
    color: var(--success-color);
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.status-error {
    color: var(--error-color);
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.status-warning {
    color: var(--warning-color);
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.panel-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-top: 0;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.panel-subtitle {
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
}

.about-section {
    margin-top: 2.5rem;
    padding: 2rem;
    border-radius: var(--radius-lg);
    background: var(--panel-bg);
    box-shadow: var(--shadow-sm);
    border: 1px solid rgba(0,0,0,0.05);
}

.about-section h2 {
    color: var(--text-primary);
    margin-top: 0;
    font-size: 1.75rem;
    font-weight: 700;
}

.about-section h3 {
    font-size: 1.25rem;
    color: var(--text-primary);
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
}

.feature-list {
    list-style-type: none;
    padding-left: 1rem;
}

.feature-list li {
    position: relative;
    padding-left: 1.5rem;
    margin-bottom: 0.5rem;
}

.feature-list li:before {
    content: "→";
    position: absolute;
    left: 0;
    color: var(--primary-color);
    font-weight: bold;
}

.footer {
    text-align: center;
    margin-top: 3rem;
    color: var(--text-secondary);
    font-size: 0.95rem;
    padding: 1.5rem;
    border-top: 1px solid rgba(0,0,0,0.05);
}

.tabs-container .tab-nav {
    background: transparent;
    padding: 0;
    border-bottom: 1px solid rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

.tabs-container button {
    font-weight: 600;
    font-size: 1.1rem;
    padding: 0.75rem 1.5rem;
    color: var(--text-secondary);
    border-bottom: 3px solid transparent;
    background: transparent;
    border-radius: 0;
    margin-right: 1rem;
}

.tabs-container button.selected {
    color: var(--primary-color);
    border-bottom: 3px solid var(--primary-color);
}

.icon {
    display: inline-block;
    vertical-align: middle;
    margin-right: 0.5rem;
}

.audio-container {
    border: 2px dashed var(--primary-light);
    border-radius: var(--radius-md);
    padding: 1.25rem;
    background-color: rgba(124, 58, 237, 0.05);
    margin-bottom: 1.5rem;
}

.voice-select-row {
    display: flex;
    align-items: center;
    gap: 1rem;
}

[data-testid="textbox"] textarea {
    border-radius: var(--radius-md);
    border: 1px solid rgba(0,0,0,0.1);
    padding: 0.75rem;
    transition: var(--transition);
}

[data-testid="textbox"] textarea:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px var(--primary-light);
}

[data-testid="textbox"] label, 
[data-testid="dropdown"] label,
[data-testid="audio"] label {
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

[data-testid="dropdown"] select {
    border-radius: var(--radius-md);
    padding: 0.75rem;
    border: 1px solid rgba(0,0,0,0.1);
}

[data-testid="button"] {
    border-radius: var(--radius-md);
}
"""

# Create the Gradio interface
with gr.Blocks(css=css, title="Sesame CSM-1B Voice Generator", theme=gr.themes.Soft()) as demo:
    with gr.Column(elem_classes="container"):
        with gr.Column(elem_id="header"):
            gr.Markdown("# Sesame CSM-1B Voice Generator")
            gr.Markdown("Create natural-sounding speech with advanced voice cloning technology")
        
        with gr.Tabs(elem_classes="tabs-container") as tabs:
            # Standard TTS Tab
            with gr.TabItem("✨ Text to Speech", elem_classes="tab-nav") as standard_tab:
                with gr.Column(elem_classes="panel"):
                    gr.Markdown('<h3 class="panel-title">🔊 Generate Speech</h3>')
                    gr.Markdown('<p class="panel-subtitle">Enter your text below and convert it to natural-sounding speech.</p>')
                    
                    text_input = gr.Textbox(
                        label="Text to speak", 
                        lines=5, 
                        placeholder="Enter the text you want to convert to speech..."
                    )
                    voice_preset = gr.Textbox(
                        label="Voice Preset (optional)", 
                        placeholder="Leave empty for default voice"
                    )
                    generate_button = gr.Button("🔊 Generate Speech", elem_classes="btn")
                    
                    with gr.Column(elem_classes="audio-container"):
                        audio_output = gr.Audio(label="Generated Speech")
                        
                    status = gr.Textbox(
                        label="Status", 
                        interactive=False,
                        placeholder="Status will appear here..."
                    )
            
            # Voice Cloning Tab
            with gr.TabItem("👤 Voice Cloning", elem_classes="tab-nav") as cloning_tab:
                with gr.Column(elem_classes="panel"):
                    gr.Markdown('<h3 class="panel-title">🎙️ Clone Your Voice</h3>')
                    gr.Markdown('<p class="panel-subtitle">Upload an audio file of your voice to create a personalized voice model.</p>')
                    
                    audio_upload = gr.Audio(
                        label="Upload Voice Sample",
                        type="filepath",
                        elem_id="voice-upload"
                    )
                    gr.Markdown('<small>5-10 seconds of clear speech recommended for best results</small>')
                    
                    voice_name_input = gr.Textbox(
                        label="Voice Name", 
                        placeholder="Enter a name for this voice..."
                    )
                    
                    clone_button = gr.Button("👤 Clone Voice", elem_classes="btn")
                    clone_status = gr.Textbox(
                        label="Cloning Status", 
                        interactive=False,
                        placeholder="Status will appear here..."
                    )
                
                with gr.Column(elem_classes="panel"):
                    gr.Markdown('<h3 class="panel-title">🎯 Generate Speech with Cloned Voice</h3>')
                    gr.Markdown('<p class="panel-subtitle">Use your cloned voice to generate personalized speech.</p>')
                    
                    cloned_text_input = gr.Textbox(
                        label="Text to speak", 
                        lines=5, 
                        placeholder="Enter the text you want to convert to speech..."
                    )
                    
                    with gr.Row(elem_classes="voice-select-row"):
                        cloned_voice_dropdown = gr.Dropdown(
                            label="Select Cloned Voice",
                            choices=voice_cloning.list_available_voices(),
                            interactive=True
                        )
                        refresh_button = gr.Button("🔄 Refresh", size="sm", elem_classes="btn-secondary")
                    
                    cloned_voice_status = gr.Textbox(
                        label="Status",
                        interactive=False,
                        placeholder="Status will appear here..."
                    )
                    
                    generate_cloned_button = gr.Button("🔊 Generate with Cloned Voice", elem_classes="btn")
                    
                    with gr.Column(elem_classes="audio-container"):
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
            and clone voices with advanced technology.
            
            ### Features
            
            <ul class="feature-list">
                <li>Generate natural-sounding speech with customizable presets</li>
                <li>Clone voices using just a short audio sample</li>
                <li>Create personalized speech with your own voice</li>
                <li>High-quality audio output for various applications</li>
            </ul>
            
            ### How to Use
            
            <ul class="feature-list">
                <li><strong>Text to Speech:</strong> Enter your text and generate speech instantly</li>
                <li><strong>Voice Cloning:</strong> Upload a voice sample, name it, and use it to generate personalized speech</li>
            </ul>
            
            ### Note
            
            If you encounter a "Service Unavailable" message, the Hugging Face API might be experiencing high traffic or 
            maintenance. The application will automatically retry a few times, but if that fails, please try again later.
            """)
            
        with gr.Column(elem_classes="footer"):
            gr.Markdown("Created with Gradio • Powered by Sesame CSM-1B • © 2023")
                
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