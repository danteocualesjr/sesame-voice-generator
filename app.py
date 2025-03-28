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
    /* Light Theme Colors */
    --primary-color: #4F46E5;
    --primary-light: #EEF2FF;
    --primary-dark: #4338CA;
    --accent-color: #F43F5E;
    --accent-light: #FFE4E6;
    --gradient-start: #4F46E5;
    --gradient-mid: #7C3AED;
    --gradient-end: #EC4899;
    
    /* Light Theme Neutral Colors */
    --text-primary: #1F2937;
    --text-secondary: #6B7280;
    --bg-color: #F8FAFC;
    --panel-bg: rgba(255, 255, 255, 0.95);
    --input-bg: rgba(255, 255, 255, 0.98);
    --border-color: rgba(0, 0, 0, 0.08);
    
    /* Light Theme Status Colors */
    --success-color: #10B981;
    --error-color: #EF4444;
    --warning-color: #F59E0B;
    
    /* Design System */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 24px;
    
    /* Shadows */
    --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-glass: 0 8px 32px rgba(0, 0, 0, 0.08);
    
    /* Effects */
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    --blur: 12px;
    
    /* Spacing */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.5rem;
    --space-6: 2rem;
}

/* Dark Theme Variables */
[data-theme="dark"] {
    --primary-color: #6366F1;
    --primary-light: #312E81;
    --primary-dark: #4F46E5;
    --accent-color: #FB7185;
    --accent-light: #831843;
    
    --text-primary: #F9FAFB;
    --text-secondary: #D1D5DB;
    --bg-color: #0F172A;
    --panel-bg: rgba(15, 23, 42, 0.95);
    --input-bg: rgba(30, 41, 59, 0.98);
    --border-color: rgba(255, 255, 255, 0.08);
    
    --success-color: #34D399;
    --error-color: #F87171;
    --warning-color: #FBBF24;
}

body {
    background: linear-gradient(135deg, var(--bg-color) 0%, var(--primary-light) 100%);
    background-attachment: fixed;
    color: var(--text-primary);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    margin: 0;
    min-height: 100vh;
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: auto;
    padding: var(--space-6) var(--space-4);
    position: relative;
    display: flex;
    flex-direction: column;
    gap: var(--space-6);
}

#header {
    text-align: center;
    margin-bottom: var(--space-6);
    position: relative;
    padding: var(--space-4) 0;
}

#header h1 {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: var(--space-3);
    background: linear-gradient(135deg, var(--gradient-start), var(--gradient-mid), var(--gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent;
    letter-spacing: -0.025em;
    line-height: 1.2;
}

#header p {
    font-size: 1.125rem;
    color: var(--text-secondary);
    max-width: 600px;
    margin: var(--space-4) auto 0;
    line-height: 1.6;
}

.panel {
    border-radius: var(--radius-xl);
    padding: var(--space-5);
    background: var(--panel-bg);
    backdrop-filter: blur(var(--blur));
    -webkit-backdrop-filter: blur(var(--blur));
    box-shadow: var(--shadow-glass);
    margin-bottom: var(--space-4);
    border: 1px solid var(--border-color);
    transition: var(--transition);
}

.panel:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.panel-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: var(--space-3) 0 var(--space-4);
    display: flex;
    align-items: center;
    gap: var(--space-2);
}

.btn {
    padding: var(--space-3) var(--space-4);
    font-size: 0.95rem;
    font-weight: 600;
    border-radius: var(--radius-md);
    background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
    color: white;
    border: none;
    cursor: pointer;
    transition: var(--transition);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.btn:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

.btn-secondary {
    background: var(--primary-light);
    color: var(--primary-color);
}

.theme-toggle {
    position: fixed;
    top: var(--space-4);
    right: var(--space-4);
    z-index: 1000;
    background: var(--panel-bg);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: var(--space-2) var(--space-3);
    cursor: pointer;
    transition: var(--transition);
    display: flex;
    align-items: center;
    gap: var(--space-2);
    color: var(--text-primary);
    font-size: 0.9rem;
    font-weight: 500;
    backdrop-filter: blur(var(--blur));
    -webkit-backdrop-filter: blur(var(--blur));
}

.theme-toggle:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

[data-testid="textbox"] textarea {
    border-radius: var(--radius-lg);
    border: 2px solid var(--border-color);
    padding: var(--space-3);
    font-size: 1rem;
    min-height: 100px;
    background: var(--input-bg);
    color: var(--text-primary);
    transition: var(--transition);
}

[data-testid="textbox"] textarea:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 4px var(--primary-light);
    outline: none;
}

[data-testid="dropdown"] select {
    border-radius: var(--radius-lg);
    padding: var(--space-3);
    border: 2px solid var(--border-color);
    background: var(--input-bg);
    color: var(--text-primary);
    font-size: 1rem;
    transition: var(--transition);
}

[data-testid="dropdown"] select:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 4px var(--primary-light);
    outline: none;
}

.feature-card {
    padding: var(--space-4);
    border-radius: var(--radius-lg);
    background: var(--panel-bg);
    border: 1px solid var(--border-color);
    transition: var(--transition);
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.feature-icon {
    font-size: 2rem;
    margin-bottom: var(--space-3);
}

.feature-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: var(--space-2);
    color: var(--text-primary);
}

.feature-description {
    font-size: 1rem;
    color: var(--text-secondary);
    line-height: 1.6;
}

.sample-voice-card {
    padding: var(--space-3);
    border-radius: var(--radius-lg);
    background: var(--panel-bg);
    border: 1px solid var(--border-color);
    transition: var(--transition);
    text-align: center;
}

.sample-voice-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.sample-icon {
    font-size: 1.5rem;
    margin-bottom: var(--space-2);
}

.status-message {
    padding: var(--space-3);
    font-size: 1rem;
    border-radius: var(--radius-lg);
    background: var(--panel-bg);
    border: 1px solid var(--border-color);
}

.pill {
    display: inline-block;
    padding: var(--space-2) var(--space-3);
    font-size: 0.875rem;
    font-weight: 600;
    border-radius: var(--radius-xl);
    background: var(--primary-light);
    color: var(--primary-color);
    margin-bottom: var(--space-3);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.audio-container {
    padding: var(--space-4);
    margin: var(--space-4) 0;
    border-radius: var(--radius-lg);
    background: var(--panel-bg);
    border: 1px solid var(--border-color);
}

/* Animations */
.animate-in {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.6s ease forwards;
}

.delay-1 {
    animation-delay: 0.2s;
}

.delay-2 {
    animation-delay: 0.4s;
}

.delay-3 {
    animation-delay: 0.6s;
}

@keyframes fadeInUp {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Responsive Design */
@media (max-width: 768px) {
    .container {
        padding: var(--space-4) var(--space-3);
    }
    
    #header h1 {
        font-size: 2.5rem;
    }
    
    .panel {
        padding: var(--space-4);
    }
    
    .theme-toggle {
        top: var(--space-3);
        right: var(--space-3);
        padding: var(--space-2);
    }
    
    .feature-card {
        padding: var(--space-3);
    }
}

/* Tab Styling */
.tabs-container {
    margin-top: var(--space-4);
}

.tab-nav {
    padding: var(--space-4);
    border-radius: var(--radius-lg);
    background: var(--panel-bg);
    border: 1px solid var(--border-color);
}

/* Footer */
.footer {
    text-align: center;
    padding: var(--space-4);
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-top: var(--space-6);
}

/* Grid Layouts */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--space-4);
    margin-top: var(--space-4);
}

.sample-voice-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--space-3);
    margin-top: var(--space-3);
}

/* About Section */
.about-section {
    margin-top: var(--space-6);
    text-align: center;
}

.about-section h2 {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: var(--space-4);
    color: var(--text-primary);
}

/* Decorative Elements */
.decorative-shape {
    position: fixed;
    border-radius: 50%;
    z-index: -1;
}

.shape-1 {
    width: 300px;
    height: 300px;
    background: linear-gradient(135deg, var(--primary-light), var(--accent-light));
    top: -100px;
    right: -100px;
    opacity: 0.5;
    filter: blur(60px);
}

.shape-2 {
    width: 200px;
    height: 200px;
    background: linear-gradient(135deg, var(--accent-light), var(--primary-light));
    bottom: -50px;
    left: -50px;
    opacity: 0.5;
    filter: blur(40px);
}
"""

# Create the Gradio interface
with gr.Blocks(css=css, title="Sesame CSM-1B Voice Generator", theme=gr.themes.Soft()) as demo:
    # Add theme toggle script to the head
    gr.HTML("""
        <script>
            // Wait for the page to load
            document.addEventListener('DOMContentLoaded', function() {
                // Initialize theme
                const savedTheme = localStorage.getItem('theme');
                if (savedTheme) {
                    document.documentElement.setAttribute('data-theme', savedTheme);
                }
                
                // Add click handler to theme toggle button
                const themeButton = document.querySelector('.theme-toggle');
                if (themeButton) {
                    themeButton.addEventListener('click', function() {
                        const root = document.documentElement;
                        const currentTheme = root.getAttribute('data-theme');
                        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                        root.setAttribute('data-theme', newTheme);
                        localStorage.setItem('theme', newTheme);
                        
                        // Update button text
                        this.textContent = newTheme === 'dark' ? '☀️ Light Mode' : '🌙 Dark Mode';
                    });
                }
            });
        </script>
    """)
    
    with gr.Column(elem_classes="container"):
        # Theme toggle button
        gr.Button(
            "🌙 Dark Mode",
            elem_classes="theme-toggle",
            size="sm"
        )
        
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