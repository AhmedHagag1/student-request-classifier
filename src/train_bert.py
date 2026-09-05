import time
import os
import pandas as pd
import torch

from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.optim import AdamW

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

from src.labels import LABELS


DATA_PATH = "data/dataset.csv"
REAL_TEST_PATH = "data/real_test.csv"
SAVE_PATH = "model/final_model"
REPORT_PATH = "reports/model_comparison.csv"

MODEL_NAME = "distilbert-base-multilingual-cased"

MAX_LENGTH = 128
BATCH_SIZE = 8
EPOCHS = 2
LEARNING_RATE = 2e-5


label2id = {label: index for index, label in enumerate(LABELS)}
id2label = {index: label for label, index in label2id.items()}


class ComplaintDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.texts = list(texts)
        self.labels = list(labels)
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):
        text = str(self.texts[index])
        label = self.labels[index]

        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=MAX_LENGTH,
            return_tensors="pt"
        )

        item = {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": torch.tensor(label, dtype=torch.long)
        }

        return item


def calculate_metrics(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0
    )

    return accuracy, precision, recall, f1


def evaluate_model(model, dataloader, device):
    model.eval()

    all_predictions = []
    all_labels = []

    start_time = time.time()

    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

            predictions = torch.argmax(outputs.logits, dim=1)

            all_predictions.extend(predictions.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    inference_time = time.time() - start_time

    accuracy, precision, recall, f1 = calculate_metrics(
        all_labels,
        all_predictions
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "inference_time": inference_time
    }


def main():
    print("Loading dataset...")

    df = pd.read_csv(DATA_PATH)

    df["label_id"] = df["label"].map(label2id)

    if df["label_id"].isnull().any():
        raise ValueError("Some labels in dataset.csv are not found in LABELS.")

    print("Dataset shape:", df.shape)
    print(df.head())

    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=df["label"]
    )

    print("\nTrain size:", len(train_df))
    print("Test size:", len(test_df))

    print("\nLoading tokenizer and model...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(LABELS),
        id2label=id2label,
        label2id=label2id
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device:", device)

    model.to(device)

    train_dataset = ComplaintDataset(
        train_df["text"],
        train_df["label_id"],
        tokenizer
    )

    test_dataset = ComplaintDataset(
        test_df["text"],
        test_df["label_id"],
        tokenizer
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    optimizer = AdamW(
        model.parameters(),
        lr=LEARNING_RATE
    )

    print("\nTraining started...")

    start_train = time.time()

    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0

        for step, batch in enumerate(train_loader, start=1):
            optimizer.zero_grad()

            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )

            loss = outputs.loss
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

            if step % 50 == 0:
                print(
                    f"Epoch {epoch + 1}/{EPOCHS} | "
                    f"Step {step}/{len(train_loader)} | "
                    f"Loss: {loss.item():.4f}"
                )

        avg_loss = total_loss / len(train_loader)

        print(f"\nEpoch {epoch + 1} finished.")
        print(f"Average loss: {avg_loss:.4f}")

        test_metrics = evaluate_model(
            model,
            test_loader,
            device
        )

        print(
            f"Validation Accuracy: {test_metrics['accuracy']:.4f} | "
            f"F1: {test_metrics['f1']:.4f}"
        )

    train_time = time.time() - start_train

    print("\nFinal evaluation on test set...")
    test_metrics = evaluate_model(
        model,
        test_loader,
        device
    )

    real_accuracy = None
    real_f1 = None

    if os.path.exists(REAL_TEST_PATH):
        print("\nEvaluating on real_test.csv...")

        real_df = pd.read_csv(REAL_TEST_PATH)
        real_df["label_id"] = real_df["label"].map(label2id)

        real_dataset = ComplaintDataset(
            real_df["text"],
            real_df["label_id"],
            tokenizer
        )

        real_loader = DataLoader(
            real_dataset,
            batch_size=BATCH_SIZE,
            shuffle=False
        )

        real_metrics = evaluate_model(
            model,
            real_loader,
            device
        )

        real_accuracy = real_metrics["accuracy"]
        real_f1 = real_metrics["f1"]

        print(
            f"Real Test Accuracy: {real_accuracy:.4f} | "
            f"Real Test F1: {real_f1:.4f}"
        )

    print("\nSaving model...")

    os.makedirs(SAVE_PATH, exist_ok=True)

    model.save_pretrained(SAVE_PATH)
    tokenizer.save_pretrained(SAVE_PATH)

    print(f"Model saved to: {SAVE_PATH}")

    bert_result = {
        "model": "Multilingual DistilBERT",
        "test_accuracy": round(test_metrics["accuracy"], 4),
        "test_precision": round(test_metrics["precision"], 4),
        "test_recall": round(test_metrics["recall"], 4),
        "test_f1_score": round(test_metrics["f1"], 4),
        "real_test_accuracy": round(real_accuracy, 4) if real_accuracy is not None else None,
        "real_test_f1_score": round(real_f1, 4) if real_f1 is not None else None,
        "train_time_sec": round(train_time, 4),
        "inference_time_sec": round(test_metrics["inference_time"], 4),
    }

    if os.path.exists(REPORT_PATH):
        comparison_df = pd.read_csv(REPORT_PATH)
        comparison_df = comparison_df[
            comparison_df["model"] != "Multilingual DistilBERT"
        ]
        comparison_df = pd.concat(
            [comparison_df, pd.DataFrame([bert_result])],
            ignore_index=True
        )
    else:
        comparison_df = pd.DataFrame([bert_result])

    comparison_df.to_csv(
        REPORT_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nUpdated model comparison:")
    print(comparison_df)

    print("\nTraining completed successfully!")


if __name__ == "__main__":
    main()