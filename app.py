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
    --primary-color: #6366F1;
    --primary-light: #C7D2FE;
    --primary-dark: #4338CA;
    --accent-color: #F43F5E;
    --accent-light: #FBD5DA;
    --gradient-start: #6366F1;
    --gradient-mid: #8B5CF6;
    --gradient-end: #EC4899;
    --text-primary: #111827;
    --text-secondary: #4B5563;
    --bg-color: #F8FAFC;
    --panel-bg: rgba(255, 255, 255, 0.85);
    --success-color: #10B981;
    --error-color: #EF4444;
    --warning-color: #F59E0B;
    --radius-sm: 6px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 20px;
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    --shadow-glass: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    --blur: 8px;
}

body {
    background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
    background-attachment: fixed;
    color: var(--text-primary);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    margin: 0;
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: auto;
    padding: 1.5rem 1rem;
    position: relative;
}

.container::before {
    content: "";
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at center, rgba(99, 102, 241, 0.05) 0%, transparent 50%);
    z-index: -1;
}

.container::after {
    content: "";
    position: fixed;
    bottom: -30%;
    right: -30%;
    width: 80%;
    height: 80%;
    background: radial-gradient(circle at center, rgba(236, 72, 153, 0.05) 0%, transparent 60%);
    z-index: -1;
}

.decorative-shape {
    position: absolute;
    border-radius: 50%;
    filter: blur(70px);
    opacity: 0.4;
    z-index: -1;
}

.shape-1 {
    top: 10%;
    left: 5%;
    width: 300px;
    height: 300px;
    background: rgba(99, 102, 241, 0.15);
}

.shape-2 {
    bottom: 5%;
    right: 10%;
    width: 250px;
    height: 250px;
    background: rgba(236, 72, 153, 0.15);
}

#header {
    text-align: center;
    margin-bottom: 1.5rem;
    position: relative;
}

#header h1 {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.25rem;
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-mid), var(--gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent;
    letter-spacing: -0.025em;
    position: relative;
    display: inline-block;
}

#header h1::after {
    content: "";
    position: absolute;
    bottom: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
    border-radius: 2px;
}

#header p {
    font-size: 1.1rem;
    color: var(--text-secondary);
    max-width: 70%;
    margin: 1rem auto 0;
    line-height: 1.5;
}

.panel {
    border-radius: var(--radius-lg);
    padding: 1.25rem;
    background: var(--panel-bg);
    backdrop-filter: blur(var(--blur));
    -webkit-backdrop-filter: blur(var(--blur));
    box-shadow: var(--shadow-glass);
    margin-bottom: 1.25rem;
    border: 1px solid rgba(255, 255, 255, 0.5);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.panel::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
    border-radius: 3px 3px 0 0;
    opacity: 0.8;
}

.panel:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg), 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.btn {
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
    border: none;
    color: white;
    padding: 0.6rem 1.25rem;
    border-radius: var(--radius-md);
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
    position: relative;
    overflow: hidden;
    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
}

.btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: 0.5s;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(99, 102, 241, 0.4);
}

.btn:hover::before {
    left: 100%;
}

.btn:active {
    transform: translateY(0);
}

.btn-secondary {
    background: white;
    color: var(--primary-color);
    border: 1px solid var(--primary-light);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.btn-secondary:hover {
    background: var(--primary-light);
    color: var(--primary-dark);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.status-message {
    padding: 0.5rem 0.75rem;
    border-radius: var(--radius-md);
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.75rem;
    font-size: 0.9rem;
}

.status-success {
    color: var(--success-color);
    background-color: rgba(16, 185, 129, 0.1);
    border-left: 3px solid var(--success-color);
}

.status-error {
    color: var(--error-color);
    background-color: rgba(239, 68, 68, 0.1);
    border-left: 3px solid var(--error-color);
}

.status-warning {
    color: var(--warning-color);
    background-color: rgba(245, 158, 11, 0.1);
    border-left: 3px solid var(--warning-color);
}

.panel-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-top: 0;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.panel-subtitle {
    color: var(--text-secondary);
    margin-bottom: 1rem;
    font-size: 0.95rem;
    line-height: 1.5;
}

.about-section {
    margin-top: 1.5rem;
    padding: 1.5rem;
    border-radius: var(--radius-xl);
    background: var(--panel-bg);
    backdrop-filter: blur(var(--blur));
    -webkit-backdrop-filter: blur(var(--blur));
    box-shadow: var(--shadow-glass);
    border: 1px solid rgba(255, 255, 255, 0.5);
    position: relative;
    overflow: hidden;
}

.about-section::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
    border-radius: 3px 3px 0 0;
    opacity: 0.7;
}

.about-section h2 {
    color: var(--text-primary);
    margin-top: 0;
    font-size: 1.5rem;
    font-weight: 700;
    position: relative;
    display: inline-block;
    margin-bottom: 1rem;
}

.about-section h2::after {
    content: "";
    position: absolute;
    bottom: -6px;
    left: 0;
    width: 50px;
    height: 3px;
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
    border-radius: 3px;
}

.about-section h3 {
    font-size: 1.15rem;
    color: var(--text-primary);
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
    position: relative;
    display: inline-block;
}

.about-section h3::after {
    content: "";
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 35px;
    height: 2px;
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
    border-radius: 2px;
}

.feature-list {
    list-style-type: none;
    padding-left: 0.5rem;
    margin-top: 1rem;
}

.feature-list li {
    position: relative;
    padding-left: 1.5rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    font-size: 0.95rem;
}

.feature-list li:before {
    content: "✦";
    position: absolute;
    left: 0;
    color: var(--primary-color);
    font-weight: bold;
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 1rem;
}

.footer {
    text-align: center;
    margin-top: 1.5rem;
    color: var(--text-secondary);
    font-size: 0.9rem;
    padding: 1.25rem 1rem;
    border-top: 1px solid rgba(0, 0, 0, 0.05);
    background: rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(var(--blur));
    -webkit-backdrop-filter: blur(var(--blur));
}

.tabs-container .tab-nav {
    background: transparent;
    padding: 0;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    margin-bottom: 1.5rem;
    display: flex;
    overflow-x: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;
}

.tabs-container .tab-nav::-webkit-scrollbar {
    display: none;
}

.tabs-container button {
    font-weight: 600;
    font-size: 1rem;
    padding: 0.75rem 1.25rem;
    color: var(--text-secondary);
    border-bottom: 3px solid transparent;
    background: transparent;
    border-radius: 0;
    margin-right: 1rem;
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.tabs-container button.selected {
    color: var(--primary-color);
    border-bottom: 3px solid var(--primary-color);
}

.tabs-container button:hover:not(.selected) {
    color: var(--primary-dark);
    background: rgba(99, 102, 241, 0.05);
}

.icon {
    display: inline-block;
    vertical-align: middle;
    font-size: 1.2rem;
    margin-right: 0.35rem;
}

.audio-container {
    border: 2px dashed var(--primary-light);
    border-radius: var(--radius-md);
    padding: 1rem;
    background-color: rgba(99, 102, 241, 0.05);
    margin-bottom: 1rem;
    transition: var(--transition);
    position: relative;
}

.audio-container:hover {
    border-color: var(--primary-color);
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.15);
}

.audio-container::before {
    content: "🎵";
    position: absolute;
    top: -12px;
    right: 12px;
    background: white;
    padding: 0.3rem;
    border-radius: 50%;
    font-size: 1rem;
    box-shadow: var(--shadow-sm);
}

.voice-select-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
}

[data-testid="textbox"] textarea {
    border-radius: var(--radius-md);
    border: 1px solid rgba(0,0,0,0.1);
    padding: 0.75rem;
    transition: var(--transition);
    font-size: 0.95rem;
    line-height: 1.5;
    resize: vertical;
    min-height: 80px;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

[data-testid="textbox"] textarea:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px var(--primary-light), inset 0 2px 4px rgba(0, 0, 0, 0.05);
    outline: none;
}

[data-testid="textbox"] label, 
[data-testid="dropdown"] label,
[data-testid="audio"] label {
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    display: block;
    font-size: 0.95rem;
}

[data-testid="dropdown"] select {
    border-radius: var(--radius-md);
    padding: 0.6rem 0.75rem;
    border: 1px solid rgba(0,0,0,0.1);
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
    font-size: 0.95rem;
    transition: var(--transition);
}

[data-testid="dropdown"] select:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px var(--primary-light), inset 0 2px 4px rgba(0, 0, 0, 0.05);
    outline: none;
}

[data-testid="button"] {
    border-radius: var(--radius-md);
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 1.25rem;
}

.feature-card {
    background: rgba(255, 255, 255, 0.7);
    border-radius: var(--radius-md);
    padding: 1rem;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
    border: 1px solid rgba(255, 255, 255, 0.8);
}

.feature-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
}

.feature-icon {
    font-size: 1.5rem;
    margin-bottom: 0.75rem;
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: inline-block;
}

.feature-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-primary);
}

.feature-description {
    color: var(--text-secondary);
    line-height: 1.5;
    font-size: 0.9rem;
}

.pill {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
    color: white;
    box-shadow: 0 2px 5px rgba(99, 102, 241, 0.3);
}

.sample-voice-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 0.75rem;
    margin-top: 1rem;
}

.sample-voice-card {
    background: white;
    border-radius: var(--radius-md);
    padding: 0.75rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    transition: var(--transition);
    border: 1px solid rgba(0,0,0,0.05);
    font-size: 0.9rem;
}

.sample-voice-card:hover {
    transform: scale(1.05);
    box-shadow: var(--shadow-md);
}

.sample-icon {
    font-size: 1.25rem;
    margin-bottom: 0.35rem;
    color: var(--primary-color);
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.25rem;
    margin-top: 1.25rem;
}

@media (max-width: 768px) {
    .card-grid, .feature-grid {
        grid-template-columns: 1fr;
    }
    
    #header h1 {
        font-size: 2rem;
    }
    
    #header p {
        max-width: 100%;
        font-size: 1rem;
    }
    
    .panel, .about-section {
        padding: 1.25rem;
    }
}

/* Animation Classes */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-in {
    animation: fadeIn 0.6s ease-out forwards;
}

.delay-1 {
    animation-delay: 0.1s;
}

.delay-2 {
    animation-delay: 0.2s;
}

.delay-3 {
    animation-delay: 0.3s;
}
"""

# Create the Gradio interface
with gr.Blocks(css=css, title="Sesame CSM-1B Voice Generator", theme=gr.themes.Soft()) as demo:
    with gr.Column(elem_classes="container"):
        # Decorative shapes
        gr.HTML('<div class="decorative-shape shape-1"></div>')
        gr.HTML('<div class="decorative-shape shape-2"></div>')
        
        with gr.Column(elem_id="header", elem_classes="animate-in"):
            gr.Markdown("# Sesame CSM-1B Voice Generator")
            gr.Markdown("Transform text into lifelike speech with our advanced voice cloning technology")
        
        with gr.Tabs(elem_classes="tabs-container animate-in delay-1") as tabs:
            # Standard TTS Tab
            with gr.TabItem("✨ Text to Speech", elem_classes="tab-nav") as standard_tab:
                with gr.Column(elem_classes="panel"):
                    gr.HTML('<div class="pill">Standard TTS</div>')
                    gr.Markdown('<h3 class="panel-title">🔊 Generate Speech</h3>')
                    with gr.Row():
                        with gr.Column(scale=3):
                            text_input = gr.Textbox(
                                label="Text to speak", 
                                lines=4, 
                                placeholder="Enter the text you want to convert to speech..."
                            )
                        with gr.Column(scale=1):
                            voice_preset = gr.Textbox(
                                label="Voice Preset (optional)", 
                                placeholder="Leave empty for default"
                            )
                            generate_button = gr.Button("🔊 Generate", elem_classes="btn")
                    
                    # Sample presets in a more compact row
                    gr.Markdown('<p style="margin-top: 0.5rem; margin-bottom: 0.25rem;"><strong>Sample presets:</strong></p>')
                    with gr.Row(elem_classes="sample-voice-grid"):
                        for preset in ["Female (US)", "Male (UK)", "Child", "Elder"]:
                            with gr.Column(elem_classes="sample-voice-card"):
                                gr.HTML(f'<div class="sample-icon">👤</div>')
                                gr.Markdown(f"{preset}")
                    
                    with gr.Column(elem_classes="audio-container"):
                        audio_output = gr.Audio(label="Generated Speech")
                        
                    status = gr.Textbox(
                        label="Status", 
                        interactive=False,
                        placeholder="Status will appear here...",
                        elem_classes="status-message"
                    )
            
            # Voice Cloning Tab
            with gr.TabItem("👤 Voice Cloning", elem_classes="tab-nav") as cloning_tab:
                with gr.Column(elem_classes="panel"):
                    gr.HTML('<div class="pill">Voice Cloning</div>')
                    gr.Markdown('<h3 class="panel-title">🎙️ Clone Your Voice</h3>')
                    
                    with gr.Row():
                        with gr.Column(scale=2):
                            audio_upload = gr.Audio(
                                label="Upload Voice Sample",
                                type="filepath",
                                elem_id="voice-upload"
                            )
                        with gr.Column(scale=1):
                            voice_name_input = gr.Textbox(
                                label="Voice Name", 
                                placeholder="Enter a name for this voice..."
                            )
                            clone_button = gr.Button("👤 Clone Voice", elem_classes="btn")
                    
                    gr.Markdown('<small style="display: block; margin-top: -0.25rem; color: var(--text-secondary);">5-10 seconds of clear speech recommended</small>')
                    clone_status = gr.Textbox(
                        label="Cloning Status", 
                        interactive=False,
                        placeholder="Status will appear here...",
                        elem_classes="status-message"
                    )
                
                with gr.Column(elem_classes="panel"):
                    gr.HTML('<div class="pill">Text Generation</div>')
                    gr.Markdown('<h3 class="panel-title">🎯 Generate with Cloned Voice</h3>')
                    
                    with gr.Row():
                        with gr.Column(scale=3):
                            cloned_text_input = gr.Textbox(
                                label="Text to speak", 
                                lines=3, 
                                placeholder="Enter the text you want to convert to speech..."
                            )
                        with gr.Column(scale=1):
                            with gr.Row():
                                cloned_voice_dropdown = gr.Dropdown(
                                    label="Select Cloned Voice",
                                    choices=voice_cloning.list_available_voices(),
                                    interactive=True
                                )
                                refresh_button = gr.Button("🔄", size="sm", elem_classes="btn-secondary")
                            generate_cloned_button = gr.Button("🔊 Generate", elem_classes="btn")
                    
                    with gr.Column(elem_classes="audio-container"):
                        cloned_audio_output = gr.Audio(label="Generated Speech")
                        
                    cloned_status = gr.Textbox(
                        label="Status", 
                        interactive=False,
                        placeholder="Status will appear here...",
                        elem_classes="status-message"
                    )
        
        with gr.Column(elem_classes="about-section animate-in delay-2"):
            gr.Markdown("""
            ## About This Tool
            
            This tool uses Sesame's CSM-1B voice AI model through Hugging Face's API to generate realistic speech and clone voices.
            """)
            
            with gr.Row(elem_classes="feature-grid"):
                with gr.Column(elem_classes="feature-card"):
                    gr.HTML('<div class="feature-icon">🔊</div>')
                    gr.Markdown('<div class="feature-title">Natural Speech</div>')
                    gr.Markdown('<div class="feature-description">Generate human-like speech with natural intonation and rhythm.</div>')
                
                with gr.Column(elem_classes="feature-card"):
                    gr.HTML('<div class="feature-icon">👤</div>')
                    gr.Markdown('<div class="feature-title">Voice Cloning</div>')
                    gr.Markdown('<div class="feature-description">Create a digital copy of any voice with a short sample.</div>')
                
                with gr.Column(elem_classes="feature-card"):
                    gr.HTML('<div class="feature-icon">⚡</div>')
                    gr.Markdown('<div class="feature-title">Fast Processing</div>')
                    gr.Markdown('<div class="feature-description">Generate speech in seconds with our optimized AI.</div>')
                
                with gr.Column(elem_classes="feature-card"):
                    gr.HTML('<div class="feature-icon">🎛️</div>')
                    gr.Markdown('<div class="feature-title">Customizable</div>')
                    gr.Markdown('<div class="feature-description">Fine-tune voice characteristics with parameters.</div>')
            
        with gr.Column(elem_classes="footer animate-in delay-3"):
            gr.Markdown("Created with Gradio • Powered by Sesame CSM-1B • © 2023 All Rights Reserved")
                
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
        outputs=[cloned_voice_dropdown, cloned_status]
    )
    
    generate_cloned_button.click(
        generate_speech_with_cloned_voice,
        inputs=[cloned_text_input, cloned_voice_dropdown],
        outputs=[cloned_audio_output, cloned_status]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()