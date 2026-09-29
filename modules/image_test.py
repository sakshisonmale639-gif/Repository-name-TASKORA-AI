import os
from dotenv import load_dotenv

from modules.image_generator import generate_image

load_dotenv()

print("================================")
print("       TASKORA IMAGE TEST")
print("================================")

try:

    path = generate_image(
        "A beautiful futuristic AI workspace with a glowing TASKORA logo, modern computer screens, cinematic lighting, highly detailed",
        "16:9"
    )

    print()
    print("SUCCESS!")
    print("Image created:")
    print(path)

except Exception as e:

    print()
    print("IMAGE GENERATION FAILED")
    print()
    print(e)