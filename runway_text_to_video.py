import os
from dotenv import load_dotenv
import requests
import time

# Load environment variables from .env file
load_dotenv()

# Get the API key
API_KEY = os.getenv("RUNWAY_API_KEY")
# https://api.runwayml.com/v1/models/gen3a_turbo/tasks
API_URL = "https://api.runwayml.com/v1/models/gen3-alpha-turbo/tasks"

def create_text_to_video(prompt_text):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # Step 1: Create a Task
        payload = {
            "prompt_text": prompt_text
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        task = response.json()
        task_id = task["id"]
        print(f"Task created. Task ID: {task_id}")

        # Step 2: Poll for Task Completion
        while True:
            time.sleep(10)  # Wait 10 seconds
            status_response = requests.get(f"https://api.runwayml.com/v1/tasks/{task_id}", headers=headers)
            status_response.raise_for_status()
            task_status = status_response.json()

            if task_status["status"] == "SUCCEEDED":
                print("Video generation successful. Video URL:", task_status["output_url"])
                return task_status["output_url"]
            elif task_status["status"] == "FAILED":
                print("Video generation failed:", task_status["error_message"])
                return None

    except requests.RequestException as e:
        print("Error during API call:", e)

# Example usage
create_text_to_video("Generate a cinematic video of a futuristic city.")