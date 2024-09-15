import streamlit as st
import requests
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from tinydb import TinyDB, Query

from streamlit_extras.switch_page_button import switch_page

# Проверка аутентификации
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    switch_page("registr")

st.set_page_config(page_title="Чат-бот", layout="wide")

API_URL = "https://flowise-renataraev64.amvera.io/api/v1/prediction/4a4a3f5c-9ebf-4243-8d4f-b3b69dd57313"

# Инициализируем базы данных
chat_db = TinyDB('chat_history.json')
user_db = TinyDB('user_database.json')

@st.cache_data(ttl=3600)  # Кэшируем данные на 1 час
def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

# Инициализируем историю сообщений
history = StreamlitChatMessageHistory(key="chat_messages")

# Используйте session_state для хранения состояния
if "chat_cleared" not in st.session_state:
    st.session_state.chat_cleared = False

# Инициализируем контейнер для вывода ответов
response_container = st.empty()

def display_response(response):
    response_container.empty()
    response_container.write(response)

def clear_chat():
    chat_db.truncate()  # Очищаем базу данных
    history.clear()  # Очищаем историю сообщений
    st.session_state.user_input = ""  # Очищаем поле ввода
    st.session_state.messages = []  # Очищаем сообщения в сессии
    st.success("Чат очищен!")  # Уведомление об успешной очистке
    st.session_state.chat_cleared = True  # Устанавливаем флаг очистки чата

# Кнопка очистки чата
clear_chat_button = st.sidebar.button("Очистить чат", on_click=clear_chat)

# Проверяем, был ли чат очищен, и обновляем страницу только в этом случае
if st.session_state.chat_cleared:
    st.session_state.chat_cleared = False  # Сбрасываем флаг
    st.rerun()  # Обновляем страницу

# Создаем кнопки в боковой панели


# Скрываем кнопку "registr" для аутентифицированных пользователей
if not st.session_state.get("authenticated", False):
    if st.button("Регистрация"):
        switch_page("registr")

# Основной контент приложения
st.title("Стартовая страница")
st.text("Добро пожаловать в мой чат-бот!")

# Загружаем историю сообщений из базы данных
chat_history = chat_db.all()
for msg in chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

def submit_question():
    user_input = st.session_state.user_input
    payload = {"question": user_input}
    output = query(payload)
    response_text = output.get('text', '')
    display_response(response_text)

    # Сохраняем сообщения в историю
    history.add_user_message(user_input)
    history.add_ai_message(response_text)

    # Сохраняем сообщения в базу данных
    chat_db.insert({"role": "user", "content": user_input})
    chat_db.insert({"role": "assistant", "content": response_text})

    # Очищаем поле ввода
    st.session_state.user_input = ""

st.text_input("Введите ваш вопрос", key="user_input", on_change=submit_question)