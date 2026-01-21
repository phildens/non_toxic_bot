from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# --- ТВОЙ КЛАСС (слегка адаптированный путь) ---
class ToxicClassifier:
    def __init__(self, model_path):
        self.device = torch.device('cpu')
        print(f"Загрузка модели из {model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path).to(self.device)
        self.model.eval()

    def predict(self, text):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        ).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
        toxic_prob = probabilities[0][1].item()
        return toxic_prob

# --- API ---
app = FastAPI()
# Инициализируем модель при старте. Путь /model будет создан через Docker Volume
classifier = ToxicClassifier("/model")

class TextRequest(BaseModel):
    text: str

@app.post("/predict")
def predict_toxicity(request: TextRequest):
    prob = classifier.predict(request.text)
    return {
        "text": request.text,
        "toxic_probability": prob,
        "is_toxic": prob > 0.8  # Порог считаем 80%
    }