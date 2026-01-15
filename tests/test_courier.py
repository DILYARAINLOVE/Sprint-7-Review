import allure
import pytest
import requests
from constants import BASE_URL, COURIER_CREATE, COURIER_LOGIN
from helper import generate_courier_payload, create_courier, login_courier
from data import ORDER_DATA  # импортируем для примера структуры

class TestCreateCourier:
    @allure.title("Тест на успешное создание курьера")
    def test_create_courier_success(self, courier_cleanup):
        """Проверка успешного создания курьера"""
        payload = generate_courier_payload()
        
        response = create_courier(payload)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        # Получаем ID для очистки
        login_response = login_courier(payload["login"], payload["password"])
        if login_response.status_code == 200:
            courier_id = login_response.json()['id']
            courier_cleanup(courier_id)

    @allure.title("Тест на создание дубликата курьера")
    def test_create_duplicate_courier_fails(self, setup_courier):
        """Проверка, что нельзя создать двух одинаковых курьеров"""
        courier_data = setup_courier
        
        # Пытаемся создать курьера с такими же данными
        response = create_courier(courier_data["payload"])
        
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]

    @allure.title("Тест на создание курьера без логина")
    def test_create_courier_without_login_fails(self):
        """Проверка создания курьера без логина"""
        payload = generate_courier_payload()
        del payload["login"]
        
        response = create_courier(payload)
        
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    @allure.title("Тест на создание курьера без пароля")
    def test_create_courier_without_password_fails(self):
        """Проверка создания курьера без пароля"""
        payload = generate_courier_payload()
        del payload["password"]
        
        response = create_courier(payload)
        
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

class TestLoginCourier:
    @allure.title("Тест на успешную авторизацию курьера")
    def test_login_courier_success(self, setup_courier):
        """Проверка успешной авторизации курьера"""
        courier_data = setup_courier
        
        response = login_courier(courier_data["login"], courier_data["password"])
        
        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()['id'], int)

    @allure.title("Тест на авторизацию с неверным паролем")
    def test_login_courier_wrong_password_fails(self, setup_courier):
        """Проверка авторизации с неверным паролем"""
        courier_data = setup_courier
        
        response = login_courier(courier_data["login"], "wrong_password")
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    @allure.title("Тест на авторизацию с несуществующим логином")
    def test_login_courier_non_existent_fails(self):
        """Проверка авторизации с несуществующим логином"""
        response = login_courier("nonexistent_user_12345", "password123")
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    @allure.title("Тест на авторизацию без логина")
    def test_login_courier_without_login_fails(self, setup_courier):
        """Проверка авторизации без логина"""
        courier_data = setup_courier
        
        response = requests.post(f'{BASE_URL}{COURIER_LOGIN}', data={"password": courier_data["password"]})
        
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    @allure.title("Тест на авторизацию без пароля")
    def test_login_courier_without_password_fails(self, setup_courier):
        """Проверка авторизации без пароля"""
        courier_data = setup_courier
        
        response = requests.post(f'{BASE_URL}{COURIER_LOGIN}', data={"login": courier_data["login"]})
        
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]
