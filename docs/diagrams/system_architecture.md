# System Architecture Diagram

```mermaid
flowchart TD
    A[Student / Студент] --> B[Streamlit User Interface]

    B --> C[Inference Module]
    C --> D[Text Preprocessing]
    D --> E[Multilingual DistilBERT Model]

    E --> F[Classification Result]

    F --> G[Category]
    F --> H[Confidence Score]
    F --> I[Top-3 Predictions]
    F --> J[Priority Detection]
    F --> K[Responsible Department]
    F --> L[Recommendation]

    M[Dataset Generator] --> N[Dataset CSV]
    N --> O[Baseline Models Training]
    N --> P[Transformer Model Training]

    O --> Q[Model Comparison Report]
    P --> E
    P --> R[Evaluation Module]

    R --> S[Classification Report]
    R --> T[Confusion Matrix]
    R --> U[Language Performance Report]


    ## Описание

Данная диаграмма показывает общую архитектуру разработанной системы. Студент вводит обращение через пользовательский интерфейс, реализованный с помощью Streamlit. Далее текст передается в модуль инференса, где выполняется предварительная обработка и токенизация текста.

После этого обращение передается в обученную модель Multilingual DistilBERT, которая определяет категорию обращения. На основе результата система выводит категорию, вероятность классификации, три наиболее вероятные категории, приоритет, ответственный отдел и рекомендацию.

Также в архитектуре выделен обучающий контур системы, включающий генерацию набора данных, обучение базовых моделей, обучение Transformer-модели и формирование отчетов оценки качества.