import os
import torch
from diffusers import StableDiffusionPipeline


MODEL_ID = "runwayml/stable-diffusion-v1-5"

_pipe = None


def get_pipeline():
    global _pipe

    if _pipe is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

        dtype = (
            torch.float16
            if device == "cuda"
            else torch.float32
        )

        _pipe = StableDiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=dtype,
        )

        _pipe = _pipe.to(device)

    return _pipe


def generate_image(prompt):
    if not prompt or not prompt.strip():
        raise ValueError("Image prompt cannot be empty.")

    pipe = get_pipeline()

    image = pipe(
        prompt=prompt,
        num_inference_steps=20,
        guidance_scale=7.5,
    ).images[0]

    output_dir = os.path.join(
        "generated",
        "images",
    )

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    output_path = os.path.join(
        output_dir,
        "taskora_image.png",
    )

    image.save(output_path)

    return output_path
