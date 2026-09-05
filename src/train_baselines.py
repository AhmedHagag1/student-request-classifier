import time
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import accuracy_score, precision_recall_fscore_support


DATA_PATH = "data/dataset.csv"
REAL_TEST_PATH = "data/real_test.csv"
REPORT_PATH = "reports/model_comparison.csv"


def calculate_metrics(y_true, predictions):
    accuracy = accuracy_score(y_true, predictions)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        predictions,
        average="weighted",
        zero_division=0
    )

    return accuracy, precision, recall, f1


def evaluate_model(name, model, x_train, x_test, y_train, y_test, real_test_df=None):
    start_train = time.time()
    model.fit(x_train, y_train)
    train_time = time.time() - start_train

    start_pred = time.time()
    predictions = model.predict(x_test)
    inference_time = time.time() - start_pred

    accuracy, precision, recall, f1 = calculate_metrics(y_test, predictions)

    result = {
        "model": name,
        "test_accuracy": round(accuracy, 4),
        "test_precision": round(precision, 4),
        "test_recall": round(recall, 4),
        "test_f1_score": round(f1, 4),
        "real_test_accuracy": None,
        "real_test_f1_score": None,
        "train_time_sec": round(train_time, 4),
        "inference_time_sec": round(inference_time, 4),
    }

    if real_test_df is not None:
        real_x = real_test_df["text"]
        real_y = real_test_df["label"]

        real_predictions = model.predict(real_x)

        real_accuracy, real_precision, real_recall, real_f1 = calculate_metrics(
            real_y,
            real_predictions
        )

        result["real_test_accuracy"] = round(real_accuracy, 4)
        result["real_test_f1_score"] = round(real_f1, 4)

    return result


def main():
    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded successfully!")
    print("Shape:", df.shape)
    print(df.head())

    real_test_df = None

    try:
        real_test_df = pd.read_csv(REAL_TEST_PATH)
        print("\nReal test set loaded successfully!")
        print("Real test shape:", real_test_df.shape)
    except FileNotFoundError:
        print("\nNo real_test.csv found. Skipping real test evaluation.")

    x = df["text"]
    y = df["label"]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    models = [
        (
            "TF-IDF + Logistic Regression",
            Pipeline([
                ("tfidf", TfidfVectorizer(
                    max_features=10000,
                    ngram_range=(1, 2)
                )),
                ("clf", LogisticRegression(
                    max_iter=1000
                ))
            ])
        ),

        (
            "TF-IDF + Linear SVM",
            Pipeline([
                ("tfidf", TfidfVectorizer(
                    max_features=10000,
                    ngram_range=(1, 2)
                )),
                ("clf", LinearSVC())
            ])
        ),

        (
            "TF-IDF + Naive Bayes",
            Pipeline([
                ("tfidf", TfidfVectorizer(
                    max_features=10000,
                    ngram_range=(1, 2)
                )),
                ("clf", MultinomialNB())
            ])
        )
    ]

    results = []

    for name, model in models:
        print(f"\nTraining: {name}")

        result = evaluate_model(
            name,
            model,
            x_train,
            x_test,
            y_train,
            y_test,
            real_test_df
        )

        results.append(result)
        print(result)

    results_df = pd.DataFrame(results)
    results_df.to_csv(REPORT_PATH, index=False, encoding="utf-8-sig")

    print("\nModel comparison saved successfully!")
    print(results_df)


if __name__ == "__main__":
    main()