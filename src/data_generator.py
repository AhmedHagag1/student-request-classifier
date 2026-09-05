import random
import pandas as pd


DATA = {
    "IT-проблемы": {
        "ru": [
            "Не работает личный кабинет",
            "Не могу войти в систему",
            "Сайт университета не открывается",
            "Портал университета зависает",
            "Ошибка при входе в аккаунт",
            "Не загружается электронная платформа",
            "Система выдает ошибку при авторизации",
            "Не могу отправить задание через платформу",
            "Проблема с доступом к университетскому порталу",
            "Личный кабинет работает слишком медленно",
            "Не могу восстановить пароль",
            "Портал не отвечает",
            "Ошибка сервера при открытии страницы",
            "Не работает онлайн система обучения",
            "Сайт университета лагает",
            "Не могу зайти в кабинет",
            "Система выбрасывает меня из аккаунта",
            "Не приходит код подтверждения",
            "Платформа не принимает файл",
            "Не открывается расписание в личном кабинете",
            "универ сайт лагает",
            "портал умер",
            "кабинет не грузится",
            "не могу логиниться",
            "сайт тупит",
            "личный кабнет не работает",
        ],
        "en": [
            "The student portal is not working",
            "I cannot log in to my student account",
            "The university website does not open",
            "The online platform keeps freezing",
            "Login error in my account",
            "The e-learning platform is not loading",
            "The system shows an error during authorization",
            "I cannot submit my assignment through the platform",
            "I have a problem accessing the university portal",
            "My student account is working very slowly",
            "I cannot reset my password",
            "The portal is not responding",
            "Server error when opening the page",
            "The online learning system is not working",
            "The university website is lagging",
            "I cannot access my account",
            "The platform logs me out automatically",
            "The confirmation code does not arrive",
            "The system does not accept my file",
            "My student portal is frozen",
            "uni website is down",
            "student account not loading",
            "portal keeps crashing",
            "login problem in university system",
            "can't open my account",
        ],
        "mixed": [
            "не могу login в личный кабинет",
            "portal не открывается",
            "student account не работает",
            "сайт универа keeps crashing",
            "не могу upload файл на платформу",
        ],
    },

    "Библиотека": {
        "ru": [
            "Не могу получить доступ к библиотеке",
            "Ошибка при входе в электронную библиотеку",
            "Книга недоступна",
            "Проблема с библиотечным аккаунтом",
            "Не работает электронная библиотека",
            "Не удается скачать учебный материал",
            "Ошибка поиска книги",
            "Нет доступа к учебным материалам",
            "Библиотечная система не отвечает",
            "Проблема с продлением книги",
            "Не могу открыть электронный учебник",
            "Не отображается список книг",
            "Не могу продлить срок книги",
            "Материал заблокирован",
            "Библиотека не дает скачать файл",
            "не могу скачать методичку",
            "электронка библиотеки лагает",
            "книга не открывается",
        ],
        "en": [
            "I cannot access the library",
            "Error while logging into the digital library",
            "The book is not available",
            "There is a problem with my library account",
            "The digital library is not working",
            "I cannot download study materials",
            "Error while searching for a book",
            "I do not have access to study materials",
            "The library system is not responding",
            "I have a problem renewing a book",
            "I cannot open the electronic textbook",
            "The list of books is not displayed",
            "I cannot extend the book loan period",
            "The study material is blocked",
            "The library website does not let me download the file",
            "digital library is lagging",
            "book file does not open",
            "I need access to course materials",
        ],
        "mixed": [
            "не могу download книгу",
            "library account не работает",
            "электронная library лагает",
        ],
    },

    "Документы": {
        "ru": [
            "Не могу получить справку",
            "Ошибка при запросе документа",
            "Документ не готов",
            "Проблема с оформлением документов",
            "Не отображается статус документа",
            "Не могу скачать документ",
            "Система не принимает заявление",
            "Нет доступа к документам",
            "Проблема с университетскими документами",
            "Нужна академическая справка",
            "Не могу получить студенческий билет",
            "Транскрипт не готов",
            "Справка об обучении не загружается",
            "Заявление зависло в системе",
            "Документ оформлен с ошибкой",
            "не могу забрать справку",
            "деканат не обновил документ",
            "нужен документ для визы",
        ],
        "en": [
            "I cannot get a certificate",
            "Error while requesting a document",
            "The document is not ready",
            "There is a problem with document processing",
            "The document status is not displayed",
            "I cannot download the document",
            "The system does not accept my application",
            "I do not have access to documents",
            "There is a problem with university documents",
            "I need an academic certificate",
            "I cannot get my student ID card",
            "My transcript is not ready",
            "The enrollment certificate is not loading",
            "My document request is stuck in the system",
            "The document contains an error",
            "I need a document for my visa",
            "academic certificate is missing",
            "document request not processed",
        ],
        "mixed": [
            "нужен certificate для визы",
            "не могу download справку",
            "document status не обновляется",
        ],
    },

    "Иностранные студенты": {
        "ru": [
            "Проблема с визой",
            "Не могу продлить визу",
            "Ошибка при регистрации миграционных документов",
            "Не хватает информации для иностранных студентов",
            "Проблема с переводом документов",
            "Не могу получить помощь для иностранных студентов",
            "Проблема с миграционной службой",
            "Не принимают иностранные документы",
            "Ошибка при оформлении визы",
            "Нет информации на английском языке",
            "Не могу оформить регистрацию по месту пребывания",
            "Проблема с миграционной картой",
            "Не знаю как продлить регистрацию",
            "Нужна помощь с паспортом",
            "Паспортные данные указаны неверно",
            "Не принимают копию паспорта",
            "Проблема с медицинскими анализами",
            "Не могу пройти медосмотр",
            "Нужно сдать анализы для университета",
            "Не понимаю где пройти медицинскую комиссию",
            "Проблема со страховкой",
            "Не могу оформить медицинскую страховку",
            "Страховка не отображается в системе",
            "Проблема с общежитием для иностранного студента",
            "Не могу получить место в общежитии",
            "Нужна помощь с жильем",
            "Проблема с заселением в общежитие",
            "Не могу оформить временную регистрацию",
            "Проблема с ВНЖ",
            "Нужно оформить РВП",
            "Не знаю какие документы нужны для визы",
            "Миграционный учет не готов",
            "Отдел иностранных студентов не отвечает",
            "нет инфы на английском",
            "не понимаю что делать с визой",
            "общага для иностранцев не подтверждена",
            "мед анализы не приняли",
            "паспорт не приняли в деканате",
        ],
        "en": [
            "I have a problem with my visa",
            "I cannot extend my visa",
            "Error while registering migration documents",
            "There is not enough information for international students",
            "There is a problem with document translation",
            "I cannot get support as an international student",
            "There is a problem with the migration office",
            "My foreign documents are not accepted",
            "Error while applying for a visa",
            "There is no information in English",
            "I cannot complete my residence registration",
            "There is a problem with my migration card",
            "I do not know how to extend my registration",
            "I need help with my passport",
            "My passport information is incorrect",
            "The passport copy was not accepted",
            "There is a problem with medical tests",
            "I cannot complete the medical checkup",
            "I need to submit medical tests for the university",
            "I do not know where to pass the medical examination",
            "There is a problem with my medical insurance",
            "I cannot get medical insurance",
            "My insurance is not displayed in the system",
            "There is a problem with dormitory for international students",
            "I cannot get a place in the dormitory",
            "I need help with accommodation",
            "There is a problem with dormitory check-in",
            "I cannot complete temporary registration",
            "There is a problem with residence permit",
            "I need to apply for temporary residence permit",
            "I do not know what documents are needed for visa",
            "Migration registration is not ready",
            "The international students office does not reply",
            "visa extension problem",
            "passport issue with university office",
            "medical tests were rejected",
            "I need housing as an international student",
            "dormitory confirmation is missing",
        ],
        "mixed": [
            "не могу extend visa",
            "passport данные неправильные",
            "medical tests не приняли",
            "нужна help with dormitory",
            "migration card проблема",
            "registration для foreign student не готова",
            "не могу получить insurance",
        ],
    },

    "Преподаватели": {
        "ru": [
            "Преподаватель не отвечает на сообщения",
            "Проблема с преподавателем",
            "Не согласен с оценкой преподавателя",
            "Конфликт с преподавателем",
            "Преподаватель отменил занятие",
            "Не могу связаться с преподавателем",
            "Преподаватель не загрузил материалы",
            "Несправедливая оценка",
            "Жалоба на преподавателя",
            "Преподаватель игнорирует сообщения",
            "Преподаватель не проверяет задания",
            "Лектор не пришел на занятие",
            "Преподаватель поставил неправильную оценку",
            "Не могу получить обратную связь",
            "Преподаватель грубо отвечает",
            "препод не отвечает",
            "препод игнорит",
            "училка не проверила работу",
            "лектор отменил пару",
        ],
        "en": [
            "The teacher does not reply to messages",
            "I have a problem with a teacher",
            "I disagree with the teacher's grade",
            "There is a conflict with a teacher",
            "The teacher canceled the class",
            "I cannot contact the teacher",
            "The teacher did not upload the materials",
            "The grade is unfair",
            "I want to complain about a teacher",
            "The teacher is ignoring my messages",
            "The teacher does not check assignments",
            "The lecturer did not come to class",
            "The teacher gave me the wrong grade",
            "I cannot get feedback from the teacher",
            "The teacher replies rudely",
            "professor ignores messages",
            "teacher not checking homework",
            "lecturer canceled the class",
        ],
        "mixed": [
            "препод не отвечает in chat",
            "teacher игнорит сообщения",
            "не могу contact преподавателя",
        ],
    },

    "Расписание": {
        "ru": [
            "Ошибка в расписании",
            "Не отображается расписание",
            "Изменилось время занятий",
            "Конфликт в расписании занятий",
            "Не могу найти аудиторию",
            "Расписание отображается неправильно",
            "Занятие перенесено без уведомления",
            "Отсутствует информация о паре",
            "Проблема с онлайн расписанием",
            "Неверно указано время занятия",
            "В расписании нет моей группы",
            "Пара исчезла из расписания",
            "Аудитория указана неверно",
            "Не совпадает расписание в системе",
            "Пара стоит в неправильный день",
            "расписание кривое",
            "не вижу пару",
            "аудитория не та",
        ],
        "en": [
            "There is an error in the schedule",
            "The schedule is not displayed",
            "The class time has changed",
            "There is a conflict in the class schedule",
            "I cannot find the classroom",
            "The schedule is displayed incorrectly",
            "The class was moved without notification",
            "Information about the class is missing",
            "There is a problem with the online schedule",
            "The class time is incorrect",
            "My group is missing from the schedule",
            "The class disappeared from the schedule",
            "The classroom is incorrect",
            "The schedule in the system does not match",
            "The class is shown on the wrong day",
            "schedule is wrong",
            "I cannot see my class",
            "wrong classroom in schedule",
        ],
        "mixed": [
            "расписание shows wrong classroom",
            "class time неверное",
            "не вижу schedule на сегодня",
        ],
    },

    "Регистрация": {
        "ru": [
            "Не могу зарегистрироваться на курс",
            "Ошибка при регистрации на предмет",
            "Проблема с регистрацией",
            "Не отображается регистрация на экзамен",
            "Не получается завершить регистрацию",
            "Система не позволяет зарегистрироваться",
            "Возникла ошибка регистрации",
            "Не могу выбрать дисциплину",
            "Регистрация была отменена автоматически",
            "Проблема при выборе учебной программы",
            "Не могу записаться на предмет",
            "Не могу зарегистрироваться на семестр",
            "Курс недоступен для регистрации",
            "Система не дает выбрать группу",
            "Не открывается запись на экзамен",
            "ошибка регестрации",
            "не могу записаться",
            "регистрация слетела",
            "не дает выбрать курс",
        ],
        "en": [
            "I cannot register for a course",
            "Error while registering for a subject",
            "There is a registration problem",
            "Exam registration is not displayed",
            "I cannot complete the registration",
            "The system does not allow me to register",
            "A registration error occurred",
            "I cannot choose a discipline",
            "The registration was canceled automatically",
            "There is a problem choosing the study program",
            "I cannot enroll in a subject",
            "I cannot register for the semester",
            "The course is not available for registration",
            "The system does not allow me to choose a group",
            "Exam enrollment is not opening",
            "registration error",
            "can't enroll in course",
            "course registration failed",
        ],
        "mixed": [
            "не могу register на курс",
            "registration на экзамен не работает",
            "не дает enroll в предмет",
        ],
    },

    "Финансы": {
        "ru": [
            "Не могу оплатить обучение",
            "Ошибка оплаты",
            "Проблема с платежом",
            "Платеж не проходит",
            "Система отклоняет оплату",
            "Не отображается информация об оплате",
            "Ошибка при оплате через портал",
            "Не могу получить квитанцию",
            "Деньги списаны, но платеж не подтвержден",
            "Проблема с оплатой общежития",
            "Не пришла квитанция об оплате",
            "Счет за обучение отображается неверно",
            "Не могу оплатить семестр",
            "Оплата зависла в системе",
            "Платеж прошел два раза",
            "аплата не проходит",
            "деньги сняли а статус unpaid",
            "квитанция не появилась",
            "не могу оплатить общагу",
        ],
        "en": [
            "I cannot pay my tuition fee",
            "Payment error",
            "There is a problem with the payment",
            "The payment does not go through",
            "The system rejects the payment",
            "Payment information is not displayed",
            "Error while paying through the portal",
            "I cannot get a receipt",
            "The money was charged but the payment was not confirmed",
            "There is a problem paying for the dormitory",
            "The payment receipt did not arrive",
            "The tuition invoice is displayed incorrectly",
            "I cannot pay for the semester",
            "The payment is stuck in the system",
            "The payment was charged twice",
            "tuition payment problem",
            "money charged but still unpaid",
            "receipt is missing",
            "dorm payment issue",
        ],
        "mixed": [
            "payment прошел но квитанции нет",
            "не могу pay tuition",
            "деньги charged but статус unpaid",
        ],
    },

    "Экзамены": {
        "ru": [
            "Не отображаются результаты экзамена",
            "Ошибка в оценках",
            "Проблема с экзаменационными результатами",
            "Неверно указана оценка",
            "Не могу посмотреть результаты",
            "Оценка отсутствует в системе",
            "Экзаменационные данные недоступны",
            "Ошибка при просмотре оценок",
            "Результаты появились с ошибкой",
            "Нет доступа к информации об экзамене",
            "Не получил зачет",
            "Не отображается допуск к экзамену",
            "Неправильно стоит оценка за тест",
            "Не могу открыть экзаменационный лист",
            "Нет результата зачета",
            "не вижу оценки",
            "зачет не поставили",
            "экзамен не отображается",
            "резы экзамена пропали",
        ],
        "en": [
            "Exam results are not displayed",
            "There is an error in my grades",
            "There is a problem with exam results",
            "The grade is incorrect",
            "I cannot view my results",
            "The grade is missing in the system",
            "Exam data is not available",
            "Error while viewing grades",
            "The results appeared with an error",
            "I do not have access to exam information",
            "I did not receive credit for the exam",
            "Exam admission is not displayed",
            "The test grade is incorrect",
            "I cannot open the exam sheet",
            "The pass result is missing",
            "my grades are missing",
            "wrong exam grade",
            "exam results disappeared",
        ],
        "mixed": [
            "не вижу exam results",
            "grade неправильный",
            "зачет missing in system",
        ],
    },
}


def add_typos(text: str, language: str) -> str:
    ru_typos = {
        "о": "а",
        "е": "и",
        "и": "е",
        "а": "о",
        "т": "тт",
        "н": "нн",
    }

    en_typos = {
        "a": "e",
        "e": "a",
        "i": "e",
        "o": "0",
        "s": "z",
    }

    chars = list(text)
    typo_map = ru_typos if language == "ru" else en_typos

    for i in range(len(chars)):
        lower_char = chars[i].lower()

        if lower_char in typo_map and random.random() < 0.035:
            chars[i] = typo_map[lower_char]

    if len(chars) > 6 and random.random() < 0.15:
        remove_index = random.randint(1, len(chars) - 2)
        if chars[remove_index] != " ":
            chars.pop(remove_index)

    return "".join(chars)


def add_context(text: str, language: str) -> str:
    ru_prefixes = [
        "Здравствуйте, ",
        "Добрый день, ",
        "У меня проблема: ",
        "Подскажите пожалуйста, ",
        "Помогите, ",
        "",
    ]

    en_prefixes = [
        "Hello, ",
        "Good afternoon, ",
        "I have a problem: ",
        "Could you please help me, ",
        "Please help, ",
        "",
    ]

    ru_suffixes = [
        "",
        ". Помогите пожалуйста.",
        ". Это очень важно.",
        ". Я не знаю, что делать.",
        ". Уже несколько дней не могу решить проблему.",
        ". Срочно нужна помощь.",
    ]

    en_suffixes = [
        "",
        ". Please help me.",
        ". This is very important.",
        ". I do not know what to do.",
        ". I have been trying to solve this for several days.",
        ". I need urgent help.",
    ]

    if language == "ru":
        return random.choice(ru_prefixes) + text + random.choice(ru_suffixes)

    return random.choice(en_prefixes) + text + random.choice(en_suffixes)


def generate_dataset(samples_per_class_per_language: int = 300) -> pd.DataFrame:
    rows = []

    for label, language_groups in DATA.items():
        for language in ["ru", "en"]:
            examples = language_groups[language]

            for _ in range(samples_per_class_per_language):
                text = random.choice(examples)

                if random.random() < 0.55:
                    text = add_context(text, language)

                if random.random() < 0.30:
                    text = add_typos(text, language)

                rows.append({
                    "text": text,
                    "label": label,
                    "language": language,
                })

        mixed_examples = language_groups.get("mixed", [])

        for _ in range(int(samples_per_class_per_language * 0.25)):
            text = random.choice(mixed_examples)

            if random.random() < 0.35:
                text = add_context(text, "ru")

            if random.random() < 0.25:
                text = add_typos(text, "ru")

            rows.append({
                "text": text,
                "label": label,
                "language": "mixed",
            })

    df = pd.DataFrame(rows)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    return df


if __name__ == "__main__":
    df = generate_dataset(samples_per_class_per_language=300)

    df.to_csv("data/dataset.csv", index=False, encoding="utf-8-sig")

    print("Dataset created successfully!")
    print("Shape:", df.shape)
    print(df.head())

    print("\nClass distribution:")
    print(df["label"].value_counts())

    print("\nLanguage distribution:")
    print(df["language"].value_counts())