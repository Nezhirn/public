from diffusers import BitsAndBytesConfig, SD3Transformer2DModel
from diffusers import StableDiffusion3Pipeline
import torch
import os
import string
import random

def generate_current_image_id(length=''): 
    characters = string.ascii_letters
    current_image_id = ''.join(random.choice(characters) for _ in range(length))
    return current_image_id

username = os.getlogin()

model_id = "stabilityai/stable-diffusion-3.5-large"

nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    disable_safety_checker=True
)

model_nf4 = SD3Transformer2DModel.from_pretrained(
    model_id,
    subfolder="transformer",
    quantization_config=nf4_config,
    torch_dtype=torch.bfloat16,
    disable_safety_checker=True
)

pipeline = StableDiffusion3Pipeline.from_pretrained(
    model_id, 
    transformer=model_nf4,
    torch_dtype=torch.bfloat16,
    disable_safety_checker=True
)
pipeline.enable_model_cpu_offload()

# Задайте свой промпт
prompt = ""

output_directory = f"/home/{username}/output"
os.makedirs(output_directory, exist_ok=True)

def generate_and_save_image(prompt, image_id):
    image = pipeline(
        prompt=prompt,
        num_inference_steps=10,
        guidance_scale=9,
        max_sequence_length=512
    ).images[0]

    filename = f"output_{image_id}.png"
    filepath = os.path.join(output_directory, filename)
    
    image.save(filepath)  # Используйте переменную filepath для сохранения
    print(f"Image saved as {filepath}")

# Начальное значение счётчика
current_image_id = generate_current_image_id(5)

# Используйте разрешение, которое поддерживается моделью
generate_and_save_image(prompt, current_image_id)  # Для начала используем допустимое разрешение