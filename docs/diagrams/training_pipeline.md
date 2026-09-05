# Model Training Pipeline

```mermaid
flowchart TD
    A[Define Categories] --> B[Generate Bilingual Dataset]
    B --> C[Add Typos and Informal Phrases]
    C --> D[Create Mixed-Language Examples]
    D --> E[Save dataset.csv]

    E --> F[Train Baseline Models]
    F --> G[TF-IDF + Logistic Regression]
    F --> H[TF-IDF + Linear SVM]
    F --> I[TF-IDF + Naive Bayes]

    E --> J[Train Multilingual DistilBERT]

    G --> K[Model Comparison]
    H --> K
    I --> K
    J --> K

    J --> L[Save Final Model]
    L --> M[Evaluate Model]
    M --> N[Classification Report]
    M --> O[Confusion Matrix]
    M --> P[Language Performance]


    ## Описание

Диаграмма показывает процесс подготовки данных и обучения моделей. На первом этапе определяются категории обращений студентов. Затем формируется двуязычный набор данных на русском и английском языках.

Для повышения устойчивости модели в данные добавляются неформальные выражения, типичные орфографические ошибки и смешанные русско-английские обращения. После этого набор данных сохраняется в файл dataset.csv.

Далее выполняется обучение базовых моделей машинного обучения на основе TF-IDF, а также обучение Transformer-модели Multilingual DistilBERT. После обучения модели сравниваются по метрикам Accuracy, Precision, Recall и F1-score. Финальная модель сохраняется и используется в модуле инференса.