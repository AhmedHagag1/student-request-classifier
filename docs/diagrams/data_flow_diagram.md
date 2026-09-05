# Data Flow Diagram

```mermaid
flowchart LR
    A[Student Request Text] --> B[Input Validation]
    B --> C[Tokenization]
    C --> D[Trained AI Model]
    D --> E[Prediction Probabilities]

    E --> F[Select Highest Probability Category]
    E --> G[Generate Top-3 Categories]

    F --> H[Map Category to Department]
    F --> I[Generate Recommendation]
    F --> J[Detect Priority]

    H --> K[Final Response]
    I --> K
    J --> K
    G --> K

    K --> L[User Interface Output]



    ## Описание

Диаграмма потока данных показывает путь обращения от момента ввода текста пользователем до получения итогового результата. Сначала текст проходит проверку и токенизацию, после чего передается в обученную модель классификации.

Модель возвращает вероятности принадлежности обращения к каждой категории. Затем система выбирает категорию с наибольшей вероятностью, формирует список Top-3 наиболее вероятных категорий, определяет ответственный отдел, рекомендацию и приоритет обращения.

Итоговый результат отображается пользователю в интерфейсе на выбранном языке.