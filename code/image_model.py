import torch
import base64
import requests
from PIL import Image
from io import BytesIO
from transformers import AutoModelForImageClassification, ViTImageProcessor


local_image_path = './media/car.png'

with open(local_image_path, 'rb') as image_file:
    car_image_data = base64.b64encode(image_file.read()).decode('utf-8')

car_image_base64 = f"data:image/png;base64,{car_image_data}"

MODEL = "/tmp/models/nsfw_image_detection"

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = AutoModelForImageClassification.from_pretrained(MODEL)
processor = ViTImageProcessor.from_pretrained(MODEL)
model.to(device)

def detect_nsfw_image(url):

    print("- Detecting NSFW Image...")
    response = requests.get(url)

    if url.endswith(".svg") or response.status_code != 200:
        return url
    else:
        img = Image.open(BytesIO(response.content)).convert("RGB")

    with torch.no_grad():
        inputs = processor(images=img, return_tensors="pt")
        outputs = model(**inputs.to(device))
        logits = outputs.logits

    predicted_label = logits.argmax(-1).item()
    label = model.config.id2label[predicted_label]

    if label == "nsfw":
        print("- Replaceing NSFW Image...")
        return car_image_base64
    elif label == "normal":
        return url

