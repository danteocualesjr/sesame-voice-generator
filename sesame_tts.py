"""
Sesame CSM-1B Text-to-Speech Module
This module provides functions to interact with the Sesame CSM-1B model via Hugging Face.
"""

import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SesameTTS:
    """A class to handle text-to-speech conversion using Sesame's CSM-1B model."""
    
    def __init__(self, api_token=None):
        """
        Initialize the SesameTTS object.
        
        Args:
            api_token (str, optional): Hugging Face API token. If not provided,
                                     looks for HF_API_TOKEN in environment variables.
        """
        self.api_token = api_token or os.getenv('HF_API_TOKEN')
        if not self.api_token:
            raise ValueError("API token is required. Set it in .env file or pass it to the constructor.")
            
        self.api_url = "https://api-inference.huggingface.co/models/sesame/csm-1b"
        
    def generate_speech(self, text, output_dir="outputs", voice_preset=None):
        """
        Generate speech from text using the Sesame CSM-1B model.
        
        Args:
            text (str): The text to convert to speech
            output_dir (str): Directory to save the output audio file
            voice_preset (str, optional): Name of a voice preset to use
            
        Returns:
            str: Path to the generated audio file
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Set up headers and payload
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {"inputs": text}
        
        # Add voice preset if provided
        if voice_preset:
            payload["parameters"] = {"voice_preset": voice_preset}
            
        # Generate a filename based on timestamp
        timestamp = int(time.time())
        output_path = os.path.join(output_dir, f"output_{timestamp}.wav")
        
        try:
            print(f"Generating speech for: {text}")
            print("This may take a moment...")
            
            # Make the API request
            response = requests.post(self.api_url, headers=headers, json=payload)
            
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                print(response.text)
                return None
            
            # Save the audio file
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            print(f"Speech generated and saved to {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error generating speech: {e}")
            return None

    def list_available_voices(self):
        """
        List available voice presets from the model.
        Note: This is a placeholder - CSM-1B might not expose this functionality directly.
        
        Returns:
            list: Available voice presets
        """
        # This is a placeholder. In reality, you'd need to check the model documentation
        # for available voice presets or implement a way to query them.
        print("Voice preset functionality is model-dependent.")
        print("Check the Sesame documentation for available presets.")
        
        # Example presets (these may not be actual presets for CSM-1B)
        return ["default", "male", "female", "child"]