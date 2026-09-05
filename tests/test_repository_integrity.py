import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LABELS = {
    "IT-проблемы",
    "Библиотека",
    "Документы",
    "Иностранные студенты",
    "Преподаватели",
    "Расписание",
    "Регистрация",
    "Финансы",
    "Экзамены",
}


def read_rows(name: str) -> list[dict[str, str]]:
    with (ROOT / "data" / name).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["text", "label", "language"]:
            raise AssertionError(f"Unexpected columns in {name}: {reader.fieldnames}")
        return list(reader)


class DataContractTests(unittest.TestCase):
    def test_training_data_contract(self):
        rows = read_rows("dataset.csv")
        self.assertEqual(len(rows), 6075)
        self.assertEqual({row["label"] for row in rows}, EXPECTED_LABELS)
        self.assertEqual({row["language"] for row in rows}, {"ru", "en", "mixed"})
        self.assertTrue(all(row["text"].strip() for row in rows))

    def test_small_test_set_contract(self):
        rows = read_rows("real_test.csv")
        self.assertEqual(len(rows), 54)
        self.assertEqual({row["label"] for row in rows}, EXPECTED_LABELS)
        self.assertEqual({row["language"] for row in rows}, {"ru", "en"})
        self.assertEqual(len({row["text"].strip().lower() for row in rows}), len(rows))

    def test_required_portfolio_files_exist(self):
        for relative_path in (
            "README.md",
            "app.py",
            "src/inference.py",
            "src/labels.py",
            "reports/model_comparison.csv",
            "docs/preparation_review.md",
        ):
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)


if __name__ == "__main__":
    unittest.main()
