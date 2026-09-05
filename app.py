import pandas as pd
import plotly.express as px
import streamlit as st

from src.inference import predict_complaint


st.set_page_config(
    page_title="AI Student Request Classification System",
    page_icon="🎓",
    layout="wide"
)


TEXT = {
    "en": {
        "title": "🎓 AI Student Request Classification System",
        "subtitle": "AI-based system for classifying student requests",
        "description": (
            "This system classifies student requests in Russian and English "
            "using a multilingual AI model."
        ),
        "sidebar_title": "⚙️ System Information",
        "model_info": """
        **Model:** Multilingual DistilBERT  
        **Task:** Multi-class text classification  
        **Languages:** Russian + English  
        **Output:** Category, department, priority, recommendation
        """,
        "project_title": """
        **Project title:**  
        Разработка системы классификации обращений студентов на основе моделей ИИ
        """,
        "input_label": "Enter student request:",
        "placeholder": "Example: I cannot log in to my student account",
        "button": "🔍 Classify Request",
        "examples_title": "Examples:",
        "examples": """
        - I cannot log in to my student account  
        - I cannot pay my tuition fee  
        - My exam results are not visible  
        - My migration documents were rejected
        """,
        "warning": "Please enter a request first.",
        "spinner": "Analyzing request...",
        "result_header": "📌 Classification Result",
        "category": "Category",
        "confidence": "Confidence",
        "priority": "Priority",
        "time": "Processing Time",
        "department": "🏢 Responsible Department",
        "recommendation": "💡 Recommendation",
        "top3": "📊 Top-3 Predictions",
        "input_text": "📝 Input Text",
        "chart_title": "Top-3 Classification Probabilities",
        "chart_x": "Category",
        "chart_y": "Confidence (%)",
    },
    "ru": {
        "title": "🎓 Система классификации обращений студентов",
        "subtitle": "Система классификации обращений студентов на основе моделей ИИ",
        "description": (
            "Система классифицирует обращения студентов на русском и английском "
            "языках с использованием многоязычной модели ИИ."
        ),
        "sidebar_title": "⚙️ Информация о системе",
        "model_info": """
        **Модель:** Multilingual DistilBERT  
        **Задача:** Многоклассовая классификация текста  
        **Языки:** русский + английский  
        **Результат:** категория, отдел, приоритет, рекомендация
        """,
        "project_title": """
        **Тема проекта:**  
        Разработка системы классификации обращений студентов на основе моделей ИИ
        """,
        "input_label": "Введите обращение студента:",
        "placeholder": "Пример: Не могу оплатить обучение",
        "button": "🔍 Классифицировать обращение",
        "examples_title": "Примеры:",
        "examples": """
        - Не могу оплатить обучение  
        - Не могу войти в личный кабинет  
        - Не отображаются результаты экзамена  
        - Не могу продлить визу
        """,
        "warning": "Пожалуйста, сначала введите обращение.",
        "spinner": "Анализ обращения...",
        "result_header": "📌 Результат классификации",
        "category": "Категория",
        "confidence": "Уверенность",
        "priority": "Приоритет",
        "time": "Время обработки",
        "department": "🏢 Ответственный отдел",
        "recommendation": "💡 Рекомендация",
        "top3": "📊 Топ-3 вероятных категорий",
        "input_text": "📝 Текст обращения",
        "chart_title": "Топ-3 вероятных категорий",
        "chart_x": "Категория",
        "chart_y": "Уверенность (%)",
    }
}


# =========================
# Sidebar language selector
# =========================

st.sidebar.title("🌐 Language / Язык")

interface_language = st.sidebar.selectbox(
    "Choose interface language:",
    ["English", "Русский"]
)

lang = "en" if interface_language == "English" else "ru"
t = TEXT[lang]


# =========================
# Header
# =========================

st.title(t["title"])
st.subheader(t["subtitle"])
st.write(t["description"])

st.markdown("---")


# =========================
# Sidebar info
# =========================

st.sidebar.title(t["sidebar_title"])
st.sidebar.markdown(t["model_info"])
st.sidebar.markdown("---")
st.sidebar.markdown(t["project_title"])


# =========================
# Main input
# =========================

col1, col2 = st.columns([2, 1])

with col1:
    user_text = st.text_area(
        t["input_label"],
        height=180,
        placeholder=t["placeholder"]
    )

    classify_button = st.button(t["button"])

with col2:
    st.info(f"**{t['examples_title']}**\n\n{t['examples']}")


# =========================
# Prediction
# =========================

if classify_button:
    if not user_text.strip():
        st.warning(t["warning"])
    else:
        with st.spinner(t["spinner"]):
            result = predict_complaint(user_text)

        category_value = (
            result["category_en"]
            if lang == "en"
            else result["category_ru"]
        )

        department_value = result["department"][lang]
        recommendation_value = result["recommendation"][lang]
        priority_value = result["priority"][lang]

        st.markdown("---")
        st.header(t["result_header"])

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                label=t["category"],
                value=category_value
            )

        with c2:
            st.metric(
                label=t["confidence"],
                value=f"{result['confidence'] * 100:.2f}%"
            )

        with c3:
            st.metric(
                label=t["priority"],
                value=priority_value
            )

        with c4:
            st.metric(
                label=t["time"],
                value=f"{result['execution_time']:.3f} sec"
            )

        st.markdown(f"### {t['department']}")
        st.success(department_value)

        st.markdown(f"### {t['recommendation']}")
        st.write(recommendation_value)

        st.markdown(f"### {t['top3']}")

        top_df = pd.DataFrame(result["top_3"])
        top_df["confidence_percent"] = top_df["confidence"] * 100

        if lang == "en":
            top_df["category"] = top_df["category_en"]
        else:
            top_df["category"] = top_df["category_ru"]

        fig = px.bar(
            top_df,
            x="category",
            y="confidence_percent",
            text="confidence_percent",
            labels={
                "category": t["chart_x"],
                "confidence_percent": t["chart_y"]
            },
            title=t["chart_title"]
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        fig.update_layout(
            yaxis_range=[0, 100]
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"### {t['input_text']}")
        st.code(result["text"], language="text")