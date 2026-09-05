LABELS = [
    "IT-проблемы",
    "Библиотека",
    "Документы",
    "Иностранные студенты",
    "Преподаватели",
    "Расписание",
    "Регистрация",
    "Финансы",
    "Экзамены"
]


LABEL_TRANSLATIONS = {
    "IT-проблемы": "IT Issues",
    "Библиотека": "Library",
    "Документы": "Documents",
    "Иностранные студенты": "International Students",
    "Преподаватели": "Teachers",
    "Расписание": "Schedule",
    "Регистрация": "Registration",
    "Финансы": "Finance",
    "Экзамены": "Exams",
}


DEPARTMENT_MAP = {
    "IT-проблемы": {
        "ru": "IT-отдел",
        "en": "IT Department",
    },
    "Библиотека": {
        "ru": "Библиотека университета",
        "en": "University Library",
    },
    "Документы": {
        "ru": "Учебный офис / деканат",
        "en": "Academic Office / Dean's Office",
    },
    "Иностранные студенты": {
        "ru": "Отдел по работе с иностранными студентами",
        "en": "International Students Office",
    },
    "Преподаватели": {
        "ru": "Учебная часть / кафедра",
        "en": "Academic Department",
    },
    "Расписание": {
        "ru": "Учебный отдел",
        "en": "Scheduling Department",
    },
    "Регистрация": {
        "ru": "Регистрационный отдел",
        "en": "Registration Office",
    },
    "Финансы": {
        "ru": "Финансовый отдел",
        "en": "Finance Department",
    },
    "Экзамены": {
        "ru": "Экзаменационный отдел",
        "en": "Examination Office",
    },
}


RECOMMENDATION_MAP = {
    "IT-проблемы": {
        "ru": "Передать обращение в IT-отдел для проверки доступа к системе или платформе.",
        "en": "Forward the request to the IT Department to check access to the system or platform.",
    },
    "Библиотека": {
        "ru": "Передать обращение в библиотеку для проверки доступа к электронным ресурсам.",
        "en": "Forward the request to the library to check access to electronic resources.",
    },
    "Документы": {
        "ru": "Передать обращение в учебный офис или деканат для проверки документов.",
        "en": "Forward the request to the academic office or dean's office for document verification.",
    },
    "Иностранные студенты": {
        "ru": "Передать обращение в отдел по работе с иностранными студентами.",
        "en": "Forward the request to the International Students Office.",
    },
    "Преподаватели": {
        "ru": "Передать обращение в учебную часть или на соответствующую кафедру.",
        "en": "Forward the request to the relevant academic department.",
    },
    "Расписание": {
        "ru": "Передать обращение в учебный отдел для проверки расписания.",
        "en": "Forward the request to the scheduling department.",
    },
    "Регистрация": {
        "ru": "Передать обращение в регистрационный отдел для проверки записи на курс или экзамен.",
        "en": "Forward the request to the registration office to check course or exam enrollment.",
    },
    "Финансы": {
        "ru": "Передать обращение в финансовый отдел для проверки оплаты или квитанции.",
        "en": "Forward the request to the finance department to check payment or receipt status.",
    },
    "Экзамены": {
        "ru": "Передать обращение в экзаменационный отдел для проверки оценок или результатов.",
        "en": "Forward the request to the examination office to check grades or results.",
    },
}


PRIORITY_KEYWORDS = {
    "high": [
        "срочно",
        "urgent",
        "экзамен завтра",
        "exam tomorrow",
        "завтра экзамен",
        "deadline",
        "дедлайн",
        "не могу сдать",
        "cannot submit",
        "blocked",
        "заблокирован",
        "важно",
        "important",
    ],
    "medium": [
        "ошибка",
        "error",
        "не работает",
        "not working",
        "не могу",
        "cannot",
        "проблема",
        "problem",
        "нет доступа",
        "no access",
        "зависает",
        "лагает",
        "login",
        "payment",
    ],
}