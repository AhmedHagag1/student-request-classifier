# Use Case Diagram

```mermaid
flowchart TD
    Student[Student / Студент]
    Admin[University Staff / Сотрудник университета]

    UC1[Submit Request]
    UC2[Choose Interface Language]
    UC3[View Classification Result]
    UC4[View Responsible Department]
    UC5[View Recommendation]
    UC6[View Priority]
    UC7[Analyze Reports]
    UC8[Compare Models]
    UC9[Review Evaluation Metrics]

    Student --> UC1
    Student --> UC2
    Student --> UC3
    Student --> UC4
    Student --> UC5
    Student --> UC6

    Admin --> UC7
    Admin --> UC8
    Admin --> UC9


    ## Описание

Диаграмма вариантов использования показывает основные действия пользователей системы. Студент может выбрать язык интерфейса, ввести текст обращения, получить результат классификации, увидеть ответственный отдел, рекомендацию и приоритет обращения.

Сотрудник университета или администратор может использовать результаты системы для анализа обращений, просмотра отчетов, сравнения моделей и оценки качества классификации.

Таким образом, система может использоваться как интеллектуальный модуль первичной обработки и маршрутизации обращений студентов.