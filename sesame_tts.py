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
        
    def generate_speech(self, text, output_dir="outputs", voice_preset=None, max_retries=3):
        """
        Generate speech from text using the Sesame CSM-1B model.
        
        Args:
            text (str): The text to convert to speech
            output_dir (str): Directory to save the output audio file
            voice_preset (str, optional): Name of a voice preset to use
            max_retries (int): Maximum number of retry attempts for 503 errors
            
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
        
        retries = 0
        while retries < max_retries:
            try:
                print(f"Attempt {retries + 1}/{max_retries}: Generating speech for: {text}")
                
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
                
                print(f"Speech generated and saved to {output_path}")
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