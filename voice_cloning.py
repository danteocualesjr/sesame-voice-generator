"""
Voice Cloning Module for Sesame CSM-1B
Adapted from https://github.com/isaiahbjork/csm-voice-cloning
"""

import os
import requests
import time
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VoiceCloning:
    """Handles voice cloning functionality using Sesame's CSM-1B model."""
    
    def __init__(self, api_token=None):
        """
        Initialize the VoiceCloning object.
        
        Args:
            api_token (str, optional): Hugging Face API token. If not provided,
                                     looks for HF_API_TOKEN in environment variables.
        """
        self.api_token = api_token or os.getenv('HF_API_TOKEN')
        if not self.api_token:
            raise ValueError("API token is required. Set it in .env file or pass it to the constructor.")
            
        self.api_url = "https://api-inference.huggingface.co/models/sesame/csm-1b"
        self.voice_dir = "voice_models"
        
        # Create directory for voice models if it doesn't exist
        os.makedirs(self.voice_dir, exist_ok=True)
    
    def extract_voice(self, audio_file_path, voice_name):
        """
        Extract voice characteristics from an audio file and save as a voice model.
        
        Args:
            audio_file_path (str): Path to the audio file containing the voice to clone
            voice_name (str): Name to give the cloned voice
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if file exists
        if not os.path.exists(audio_file_path):
            print(f"Error: Audio file {audio_file_path} not found")
            return False
            
        try:
            print(f"Processing audio file for voice extraction: {audio_file_path}")
            
            # Read the audio file
            with open(audio_file_path, 'rb') as f:
                audio_data = f.read()
            
            # Set up headers for the API request
            headers = {"Authorization": f"Bearer {self.api_token}"}
            
            # Create the payload for voice extraction
            # Note: This is a simplified version - the actual API might have different parameters
            payload = {
                "inputs": audio_data,
                "parameters": {
                    "task": "voice_extraction"
                }
            }
            
            print("Sending voice extraction request to the API...")
            
            # Make the API request
            # In a real implementation, this would be the actual API endpoint for voice extraction
            # The current implementation is a placeholder since the exact API might differ
            
            # Simulating API behavior for now
            print("This is a placeholder for the actual API call to extract voice.")
            print("The real implementation would send the audio to CSM-1B for processing.")
            
            # Create a voice file path
            voice_file_path = os.path.join(self.voice_dir, f"{voice_name}.json")
            
            # Create a simple voice model (placeholder)
            voice_model = {
                "name": voice_name,
                "created": time.time(),
                "source_file": audio_file_path,
                "parameters": {
                    # This would contain actual voice parameters extracted by the model
                    "pitch": 0.0,
                    "timbre": 0.0,
                    "pace": 1.0
                }
            }
            
            # Save the voice model
            with open(voice_file_path, 'w') as f:
                json.dump(voice_model, f, indent=2)
                
            print(f"Voice model saved to {voice_file_path}")
            return True
            
        except Exception as e:
            print(f"Error extracting voice: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_speech_with_voice(self, text, voice_name, output_dir="outputs", max_retries=3):
        """
        Generate speech using a cloned voice.
        
        Args:
            text (str): The text to convert to speech
            voice_name (str): Name of the cloned voice to use
            output_dir (str): Directory to save the output audio file
            max_retries (int): Maximum number of retry attempts for 503 errors
            
        Returns:
            str: Path to the generated audio file
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Check if voice model exists
        voice_file_path = os.path.join(self.voice_dir, f"{voice_name}.json")
        if not os.path.exists(voice_file_path):
            print(f"Error: Voice model {voice_name} not found")
            return None
            
        try:
            # Load the voice model
            with open(voice_file_path, 'r') as f:
                voice_model = json.load(f)
                
            # Set up headers and payload
            headers = {"Authorization": f"Bearer {self.api_token}"}
            payload = {
                "inputs": text,
                "parameters": {
                    "voice_preset": voice_name,
                    # Add voice parameters from the model
                    "pitch": voice_model.get("parameters", {}).get("pitch", 0.0),
                    "timbre": voice_model.get("parameters", {}).get("timbre", 0.0),
                    "pace": voice_model.get("parameters", {}).get("pace", 1.0)
                }
            }
            
            # Generate a filename based on timestamp
            timestamp = int(time.time())
            output_path = os.path.join(output_dir, f"output_{voice_name}_{timestamp}.wav")
            
            retries = 0
            while retries < max_retries:
                try:
                    print(f"Attempt {retries + 1}/{max_retries}: Generating speech with voice {voice_name}")
                    
                    # Make the API request
                    response = requests.post(self.api_url, headers=headers, json=payload)
                    
                    print(f"Response status code: {response.status_code}")
                    
                    if response.status_code == 503:
                        retries += 1
                        if retries < max_retries:
                            wait_time = 2 ** retries  # Exponential backoff
                            print(f"Service unavailable. Retrying in {wait_time} seconds...")
                            time.sleep(wait_time)
                            continue
                        else:
                            print("Maximum retry attempts reached. Service is unavailable.")
                            return None
                    
                    if response.status_code != 200:
                        print(f"Error response: {response.text}")
                        return None
                    
                    # Save the audio file
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    
                    print(f"Speech generated with voice {voice_name} and saved to {output_path}")
                    return output_path
                    
                except Exception as e:
                    print(f"Error generating speech: {e}")
                    import traceback
                    traceback.print_exc()
                    retries += 1
                    if retries < max_retries:
                        wait_time = 2 ** retries
                        print(f"Exception occurred. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        print("Maximum retry attempts reached after exceptions.")
                        return None
            
            return None
            
        except Exception as e:
            print(f"Error loading voice model: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def list_available_voices(self):
        """
        List all available cloned voices.
        
        Returns:
            list: Names of available voice models
        """
        voices = []
        for file in os.listdir(self.voice_dir):
            if file.endswith(".json"):
                voices.append(file.replace(".json", ""))
        return voices