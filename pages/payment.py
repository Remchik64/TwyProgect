import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from tinydb import TinyDB, Query

# Проверка аутентификации
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    switch_page("registr")

st.set_page_config(page_title="Оплата", layout="wide")

# Инициализация базы данных пользователей
user_db = TinyDB('user_database.json')

# Получение данных пользователя
User = Query()
user_data = user_db.search(User.username == st.session_state.username)[0]

# Инициализация атрибутов, если они не существуют
if "tokens_to_buy" not in st.session_state:
    st.session_state.tokens_to_buy = 0

if "rubles_to_pay" not in st.session_state:
    st.session_state.rubles_to_pay = 0

st.title("Страница оплаты")

# Отображение баланса
st.header("Баланс")
user_data['balance'] = 0  # Установка баланса на ноль
st.write(f"Ваш баланс: {round(user_data['balance'], 2)} рублей")

# Зона для покупки токенов
st.header("Покупка токенов")
tokens_to_buy = st.number_input("Количество токенов для покупки", min_value=1000, step=1000, key="tokens_to_buy_1")

# Конвертация токенов в рубли
def tokens_to_rubles(tokens):
    return tokens / 1500  # 1500 токенов = 1 рубль

rubles_to_pay = tokens_to_rubles(tokens_to_buy)

st.write(f"Сумма к оплате: {rubles_to_pay:.2f} рублей")

if st.button("Купить токены"):
    current_balance = user_data.get('balance', 0)
    if current_balance <= 0:  # Проверка на нулевой баланс
        st.error("Ваш баланс равен нулю. Пожалуйста, пополните баланс перед покупкой токенов.")
    else:
        if rubles_to_pay <= 0:
            st.error("Сумма к оплате должна быть больше нуля.")
        elif current_balance < rubles_to_pay:
            st.error("Недостаточно средств на балансе.")
        else:
            # Обновление баланса
            new_balance = current_balance - rubles_to_pay
            user_db.update({'balance': new_balance}, User.username == st.session_state.username)
            
            # Обновление количества токенов на счету пользователя
            current_tokens = user_data.get('tokens', 0)
            new_tokens = current_tokens + tokens_to_buy
            user_db.update({'tokens': new_tokens}, User.username == st.session_state.username)
            
            # Обновление user_data для корректного отображения
            user_data = user_db.search(User.username == st.session_state.username)[0]
            
            st.success("Оплата прошла успешно! Токены добавлены на ваш счет.")

# Зона для пополнения баланса
st.header("Пополнение баланса")
amount_to_add = st.number_input("Сумма для пополнения", min_value=0.0, step=10.0, key="amount_to_add_1")
if st.button("Пополнить баланс"):
    current_balance = user_data.get('balance', 0)
    new_balance = current_balance + amount_to_add
    user_db.update({'balance': new_balance}, User.username == st.session_state.username)
    st.success(f"Баланс успешно пополнен на {amount_to_add} рублей. Новый баланс: {new_balance} рублей.")
