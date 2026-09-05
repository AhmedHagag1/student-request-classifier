import time
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from src.labels import (
    LABELS,
    LABEL_TRANSLATIONS,
    DEPARTMENT_MAP,
    RECOMMENDATION_MAP,
    PRIORITY_KEYWORDS,
)


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "model" / "final_model"


tokenizer = AutoTokenizer.from_pretrained(
    str(MODEL_PATH),
    local_files_only=True
)

model = AutoModelForSequenceClassification.from_pretrained(
    str(MODEL_PATH),
    local_files_only=True
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model.to(device)
model.eval()


def detect_priority(text: str, confidence: float) -> dict:
    text_lower = text.lower()

    for keyword in PRIORITY_KEYWORDS["high"]:
        if keyword in text_lower:
            return {
                "ru": "Высокий",
                "en": "High"
            }

    if confidence < 0.55:
        return {
            "ru": "Средний",
            "en": "Medium"
        }

    for keyword in PRIORITY_KEYWORDS["medium"]:
        if keyword in text_lower:
            return {
                "ru": "Средний",
                "en": "Medium"
            }

    return {
        "ru": "Низкий",
        "en": "Low"
    }


def predict_complaint(text: str) -> dict:
    start_time = time.time()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.nn.functional.softmax(
        outputs.logits,
        dim=1
    )[0]

    predicted_index = torch.argmax(probabilities).item()
    category_ru = LABELS[predicted_index]
    confidence = probabilities[predicted_index].item()

    top_indices = torch.topk(probabilities, k=3).indices.tolist()

    top_3 = []

    for index in top_indices:
        label_ru = LABELS[index]

        top_3.append({
            "category_ru": label_ru,
            "category_en": LABEL_TRANSLATIONS[label_ru],
            "confidence": probabilities[index].item()
        })

    execution_time = time.time() - start_time

    result = {
        "text": text,
        "category_ru": category_ru,
        "category_en": LABEL_TRANSLATIONS[category_ru],
        "confidence": confidence,
        "top_3": top_3,
        "department": DEPARTMENT_MAP[category_ru],
        "recommendation": RECOMMENDATION_MAP[category_ru],
        "priority": detect_priority(text, confidence),
        "execution_time": execution_time,
    }

    return result


if __name__ == "__main__":
    while True:
        user_text = input("\nВведите обращение / Enter student request: ")

        if user_text.lower() in ["exit", "quit", "выход"]:
            break

        result = predict_complaint(user_text)

        print("\nКатегория:", result["category_ru"])
        print("Category:", result["category_en"])

        print("\nОтдел:", result["department"]["ru"])
        print("Department:", result["department"]["en"])

        print("\nПриоритет:", result["priority"]["ru"])
        print("Priority:", result["priority"]["en"])

        print("\nУверенность:", round(result["confidence"] * 100, 2), "%")

        print("\nРекомендация:", result["recommendation"]["ru"])
        print("Recommendation:", result["recommendation"]["en"])

        print("\nTop-3:")
        for item in result["top_3"]:
            print(
                f"- {item['category_ru']} / {item['category_en']}: "
                f"{item['confidence'] * 100:.2f}%"
            )

        print("\nВремя обработки:", round(result["execution_time"], 4), "сек.")