import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from tinydb import TinyDB, Query

# Проверка аутентификации
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Пожалуйста, войдите в систему.")
    switch_page("registr")

st.set_page_config(page_title="Личный кабинет", layout="wide")

# Инициализация базы данных пользователей
user_db = TinyDB('user_database.json')

# Получение данных пользователя
User = Query()
user_data = user_db.search(User.username == st.session_state.username)[0]

st.title(f"Личный кабинет {user_data['username']}")

# Отображение информации о пользователе
st.header("Личная информация")
st.write(f"Email: {user_data['email']}")

# Зона для обновления данных
st.header("Обновление данных")
new_email = st.text_input("Новый email", value=user_data['email'])
new_password = st.text_input("Новый пароль", type="password")
confirm_password = st.text_input("Подтвердите новый пароль", type="password")

if st.button("Обновить данные"):
    if new_password != confirm_password:
        st.error("Пароли не совпадают")
    else:
        user_db.update({'email': new_email, 'password': new_password}, User.username == st.session_state.username)
        st.success("Данные успешно обновлены")

# Зона для выхода из аккаунта
if st.button("Выйти"):
    st.session_state.authenticated = False
    st.session_state.username = None
    switch_page("registr")  # Измените на существующую страницу

# Зона для перехода в чат
if st.button("Перейти в чат"):
    switch_page("app")
