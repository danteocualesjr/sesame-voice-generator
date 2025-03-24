"""
Test script for Hugging Face API connection
This script tests direct connectivity to the Sesame CSM-1B model API
"""

import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

def test_api(max_retries=3):
    token = os.getenv('HF_API_TOKEN')
    if not token:
        print("Error: No API token found in .env file")
        return
        
    api_url = "https://api-inference.huggingface.co/models/sesame/csm-1b"
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": "This is a test of the Sesame CSM-1B model."}
    
    print("API Token (first 5 chars):", token[:5] + "...")
    
    retries = 0
    while retries < max_retries:
        try:
            print(f"Attempt {retries + 1}/{max_retries}: Making API request...")
            response = requests.post(api_url, headers=headers, json=payload)
            
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 503:
                print("Service Unavailable (503) error received")
                retries += 1
                if retries < max_retries:
                    wait_time = 2 ** retries
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    print("Maximum retry attempts reached. Service is unavailable.")
                    return
            
            if response.status_code == 200:
                print("Success! Received audio data.")
                print(f"Response content length: {len(response.content)} bytes")
                
                # Save the test audio
                with open("test_output.wav", "wb") as f:
                    f.write(response.content)
                print("Saved audio to test_output.wav")
                break
            else:
                print(f"Error response: {response.text}")
                break
                
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            import traceback
            traceback.print_exc()
            retries += 1
            if retries < max_retries:
                wait_time = 2 ** retries
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Maximum retry attempts reached after exceptions.")

if __name__ == "__main__":
    test_api()