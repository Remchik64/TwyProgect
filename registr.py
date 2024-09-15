import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from tinydb import TinyDB, Query

st.set_page_config(page_title="Вход/Регистрация", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

# Инициализация базы данных пользователей
user_db = TinyDB('user_database.json')

# Функция для регистрации пользователя
def register_user(username, email, password):
    User = Query()
    if user_db.search(User.username == username):
        return False, "Пользователь с таким именем уже существует"
    if user_db.search(User.email == email):
        return False, "Пользователь с таким email уже существует"
    user_db.insert({'username': username, 'email': email, 'password': password})
    return True, "Регистрация успешна"

# Функция для входа в систему
def login(username, password):
    User = Query()
    user = user_db.search((User.username == username) & (User.password == password))
    return bool(user)

# Заголовок
st.title("Вход в систему")

# Форма для входа
username = st.text_input("Имя пользователя")
password = st.text_input("Пароль", type="password")

# Кнопки для входа и регистрации
if st.button("Login"):
    if username and password:  # Проверка на пустые поля
        if login(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("Вы вошли в систему")
            switch_page("app")  # Перенаправление в основное приложение
        else:
            st.error("Неправильный логин или пароль.")
    else:
        st.error("Пожалуйста, введите имя пользователя и пароль.")

# Кнопка для регистрации
if not st.session_state.get("authenticated", False):
    if st.button("Зарегистрироваться"):
        st.session_state.show_registration_form = True

# Проверка состояния для отображения формы регистрации
if "show_registration_form" not in st.session_state:
    st.session_state.show_registration_form = False

if st.session_state.show_registration_form:
    with st.form("registration_form"):
        reg_username = st.text_input("Имя пользователя для регистрации")
        reg_email = st.text_input("Email")
        reg_password = st.text_input("Пароль", type="password")
        reg_confirm_password = st.text_input("Подтвердите пароль", type="password")
        submit_button = st.form_submit_button("Зарегистрироваться")

        if submit_button:
            if not reg_username or not reg_email or not reg_password or not reg_confirm_password:
                st.error("Пожалуйста, заполните все поля.")
            elif reg_password != reg_confirm_password:
                st.error("Пароли не совпадают")
            else:
                success, message = register_user(reg_username, reg_email, reg_password)
                if success:
                    st.success(message)
                    st.session_state.username = reg_username
                    st.session_state.authenticated = True
                    switch_page("app")
                else:
                    st.error(message)

# Добавление CSS для кнопок
st.markdown(
    """
    <style>
    .stButton {
        margin-left: 0px;  /* Установите отрицательный отступ для сдвига влево */
        margin-right: 0px;  /* Установите положительный отступ для сдвига вправо */
    }
    </style>
    """,
    unsafe_allow_html=True
)