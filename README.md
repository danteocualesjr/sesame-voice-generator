# Sesame CSM-1B Voice Generator with Voice Cloning

A Python application for generating natural-sounding speech using Sesame's CSM-1B voice AI model with added voice cloning capabilities. This project allows you to not only convert text to speech but also clone your own voice for personalized speech synthesis.

## Features

- Convert text to speech using Sesame's CSM-1B voice AI model
- Clone voices from audio samples
- Generate speech using your cloned voice
- Modern, easy-to-use web interface built with Gradio
- Automatic retries for API availability issues

## Prerequisites

- Python 3.10 or later
- A Hugging Face account and API token
- Internet connection

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/sesame-voice-generator.git
   cd sesame-voice-generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your Hugging Face API token:
   ```
   HF_API_TOKEN=your_huggingface_token_here
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://127.0.0.1:7860)

3. The application offers two main features:

### Text to Speech
- Enter text in the input field
- Optionally specify a voice preset
- Click "Generate Speech"
- Listen to or download the generated audio

### Voice Cloning
- Record or upload an audio file containing your voice (5-10 seconds of clear speech recommended)
- Enter a name for this voice
- Click "Clone Voice" to create a voice model
- Once your voice is cloned, you can use it to generate speech:
  - Enter text in the input field
  - Select your cloned voice from the dropdown
  - Click "Generate Speech with Cloned Voice"
  - Listen to or download the generated audio

## How Voice Cloning Works

The voice cloning feature uses Sesame's CSM-1B model to analyze an audio sample of your voice and create a voice model. This model captures your voice characteristics such as pitch, timbre, and speech patterns. When generating speech with your cloned voice, the application applies these characteristics to make the synthesized speech sound like you.

For optimal results:
- Use a high-quality audio recording with minimal background noise
- Speak clearly and naturally in your sample
- Provide at least 5 seconds of speech
- Experiment with different voice samples if needed

## Project Structure

- `app.py`: Main application with Gradio web interface
- `sesame_tts.py`: Core functionality for text-to-speech
- `voice_cloning.py`: Functionality for voice cloning
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (not included in repository)
- `voice_models/`: Directory for storing cloned voice models
- `outputs/`: Directory for storing generated audio files

## Troubleshooting

### API Unavailability
The Hugging Face API may sometimes return 503 Service Unavailable errors due to high demand or maintenance. The application includes automatic retry logic with exponential backoff. If you consistently encounter availability issues:
- Try again during off-peak hours
- Check the Hugging Face status page for any announced outages

### Voice Cloning Issues
If you're having trouble with voice cloning:
- Ensure your audio sample is clear and at least 5 seconds long
- Try a different audio sample with less background noise
- Make sure your audio file is in a common format (WAV, MP3, etc.)
- Check the terminal output for specific error messages

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Sesame AI](https://www.sesame.com/) for releasing the CSM-1B model
- [Isaiah Bjork](https://github.com/isaiahbjork) for the CSM voice cloning repository
- [Hugging Face](https://huggingface.co/) for hosting the model
- [Gradio](https://gradio.app/) for the web interface framework