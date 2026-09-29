from modules.image_generator import generate_image


print("================================")
print("       TASKORA IMAGE TEST")
print("================================")
print()

prompt = (
    "A futuristic AI assistant helping a college student "
    "organize tasks in a beautiful modern digital workspace, "
    "purple and blue neon lighting, cinematic, highly detailed"
)

try:
    image_path = generate_image(prompt)

    print()
    print("SUCCESS!")
    print()
    print("Image created:")
    print(image_path)

except Exception as e:

    print()
    print("IMAGE GENERATION FAILED")
    print()
    print("Error:")
    print(e)