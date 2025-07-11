# app/vision.py

import openai
import os

openai.api_key = os.getenv(\"OPENAI_API_KEY\")

def label_image(image_path):
    with open(image_path, \"rb\") as img_file:
        img_bytes = img_file.read()
    
    response = openai.ChatCompletion.create(
        model=\"gpt-4o-vision-preview\",
        messages=[
            {
                \"role\": \"user\",
                \"content\": [
                    {\"type\": \"text\", \"text\": \"Describe this image. List 3-5 key labels for ML training.\"},
                    {
                        \"type\": \"image_url\",
                        \"image_url\": {
                            \"url\": f\"data:image/jpeg;base64,{img_bytes.hex()}\"
                        }
                    }
                ]
            }
        ]
    )
    text = response.choices[0].message.content
    # Extract labels & description (simple split)
    if \"Labels:\" in text:
        parts = text.split(\"Labels:\")
        description = parts[0].strip()
        labels = parts[1].strip().split(\",\")
        labels = [label.strip() for label in labels]
    else:
        description = text.strip()
        labels = []
    return labels, description
