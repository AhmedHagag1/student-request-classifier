import os
from pathlib import Path

import pandas as pd
import torch
import matplotlib.pyplot as plt

from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    accuracy_score,
    precision_recall_fscore_support,
)

from src.labels import LABELS


BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "model" / "final_model"
DATA_PATH = BASE_DIR / "data" / "dataset.csv"
REAL_TEST_PATH = BASE_DIR / "data" / "real_test.csv"
REPORTS_DIR = BASE_DIR / "reports"

MAX_LENGTH = 128
BATCH_SIZE = 8

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

        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": torch.tensor(label, dtype=torch.long),
        }


def predict_dataset(model, dataloader, device):
    model.eval()

    all_predictions = []
    all_labels = []

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

    return all_labels, all_predictions


def evaluate_dataframe(df, tokenizer, model, device, name):
    df = df.copy()
    df["label_id"] = df["label"].map(label2id)

    dataset = ComplaintDataset(
        df["text"],
        df["label_id"],
        tokenizer
    )

    dataloader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    y_true, y_pred = predict_dataset(
        model,
        dataloader,
        device
    )

    report_dict = classification_report(
        y_true,
        y_pred,
        target_names=LABELS,
        output_dict=True,
        zero_division=0
    )

    report_df = pd.DataFrame(report_dict).transpose()

    report_path = REPORTS_DIR / f"{name}_classification_report.csv"
    report_df.to_csv(report_path, encoding="utf-8-sig")

    cm = confusion_matrix(
        y_true,
        y_pred,
        labels=list(range(len(LABELS)))
    )

    fig, ax = plt.subplots(figsize=(12, 10))

    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=LABELS
    )

    display.plot(
        ax=ax,
        xticks_rotation=45,
        cmap="Blues",
        values_format="d"
    )

    plt.title(f"Confusion Matrix - {name}")
    plt.tight_layout()

    cm_path = REPORTS_DIR / f"{name}_confusion_matrix.png"
    plt.savefig(cm_path, dpi=300)
    plt.close()

    accuracy = accuracy_score(y_true, y_pred)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0
    )

    summary = {
        "dataset": name,
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "samples": len(df)
    }

    return summary


def evaluate_by_language(real_test_df, tokenizer, model, device):
    results = []

    for language in real_test_df["language"].unique():
        language_df = real_test_df[real_test_df["language"] == language]

        summary = evaluate_dataframe(
            language_df,
            tokenizer,
            model,
            device,
            f"real_test_{language}"
        )

        results.append(summary)

    language_df = pd.DataFrame(results)
    language_path = REPORTS_DIR / "language_performance.csv"
    language_df.to_csv(language_path, index=False, encoding="utf-8-sig")

    return language_df


def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)

    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(
        str(MODEL_PATH),
        local_files_only=True
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        str(MODEL_PATH),
        local_files_only=True
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device:", device)

    model.to(device)

    summaries = []

    print("\nEvaluating dataset.csv...")
    df = pd.read_csv(DATA_PATH)

    dataset_summary = evaluate_dataframe(
        df,
        tokenizer,
        model,
        device,
        "dataset"
    )

    summaries.append(dataset_summary)

    if REAL_TEST_PATH.exists():
        print("\nEvaluating real_test.csv...")
        real_test_df = pd.read_csv(REAL_TEST_PATH)

        real_summary = evaluate_dataframe(
            real_test_df,
            tokenizer,
            model,
            device,
            "real_test"
        )

        summaries.append(real_summary)

        print("\nEvaluating real_test by language...")
        language_results = evaluate_by_language(
            real_test_df,
            tokenizer,
            model,
            device
        )

        print(language_results)

    summary_df = pd.DataFrame(summaries)
    summary_path = REPORTS_DIR / "evaluation_summary.csv"
    summary_df.to_csv(summary_path, index=False, encoding="utf-8-sig")

    print("\nEvaluation completed successfully!")
    print(summary_df)
    print("\nReports saved in:", REPORTS_DIR)


if __name__ == "__main__":
    main()