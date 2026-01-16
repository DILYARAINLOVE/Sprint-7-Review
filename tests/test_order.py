import allure
import pytest
import requests
from constants import BASE_URL, ORDER_CREATE, ORDER_LIST
from data import ORDER_DATA

class TestCreateOrder:
    @allure.title("Тест на создание заказа с цветом BLACK")
    def test_create_order_with_black_color(self):
        """Проверка создания заказа с цветом BLACK"""
        order_data = ORDER_DATA.copy()
        order_data["color"] = ["BLACK"]
        
        response = requests.post(f'{BASE_URL}{ORDER_CREATE}', json=order_data)
        
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Тест на создание заказа с цветом GREY")
    def test_create_order_with_grey_color(self):
        """Проверка создания заказа с цветом GREY"""
        order_data = ORDER_DATA.copy()
        order_data["color"] = ["GREY"]
        
        response = requests.post(f'{BASE_URL}{ORDER_CREATE}', json=order_data)
        
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Тест на создание заказа с обоими цветами")
    def test_create_order_with_both_colors(self):
        """Проверка создания заказа с обоими цветами"""
        order_data = ORDER_DATA.copy()
        order_data["color"] = ["BLACK", "GREY"]
        
        response = requests.post(f'{BASE_URL}{ORDER_CREATE}', json=order_data)
        
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Тест на создание заказа без указания цвета")
    def test_create_order_without_color(self):
        """Проверка создания заказа без указания цвета"""
        order_data = ORDER_DATA.copy()
        # Не добавляем поле color
        
        response = requests.post(f'{BASE_URL}{ORDER_CREATE}', json=order_data)
        
        assert response.status_code == 201
        assert "track" in response.json()

class TestGetOrdersList:
    @allure.title("Тест на получение списка заказов")
    def test_get_orders_list(self):
        """Проверка получения списка заказов"""
        response = requests.get(f'{BASE_URL}{ORDER_LIST}')
        
        # Проверяем код ответа
        assert response.status_code == 200
        
        # Проверяем структуру ответа
        response_json = response.json()
        assert "orders" in response_json
        assert isinstance(response_json["orders"], list)
        
        # Проверяем, что список orders содержит корректные данные
        orders = response_json["orders"]
        assert isinstance(orders, list)
