import allure
import requests
import random
import string
from constants import BASE_URL, COURIER_CREATE, COURIER_LOGIN, COURIER_DELETE

def generate_random_string(length):
    """Генерирует случайную строку из строчных букв"""
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def generate_courier_payload():
    """Генерирует payload для создания курьера"""
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

@allure.step('Создание курьера')
def create_courier(payload):
    """Создает нового курьера"""
    response = requests.post(f'{BASE_URL}{COURIER_CREATE}', data=payload)
    return response

@allure.step('Логин курьера')
def login_courier(login, password):
    """Авторизует курьера"""
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(f'{BASE_URL}{COURIER_LOGIN}', data=payload)
    return response

@allure.step('Удаление курьера')
def delete_courier(courier_id):
    """Удаляет курьера по ID"""
    response = requests.delete(f'{BASE_URL}{COURIER_DELETE.format(courier_id=courier_id)}')
    return response

@allure.step('Регистрация нового курьера для тестов')
def register_new_courier():
    """Создает курьера и возвращает его данные"""
    payload = generate_courier_payload()
    response = create_courier(payload)
    
    if response.status_code == 201:
        return {
            "login": payload["login"],
            "password": payload["password"],
            "first_name": payload["firstName"],
            "payload": payload
        }
    return None
