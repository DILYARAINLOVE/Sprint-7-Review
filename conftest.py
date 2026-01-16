import pytest
from helper import register_new_courier, login_courier, delete_courier

@pytest.fixture
def setup_courier():
    """Фикстура для создания и удаления курьера"""
    courier_data = register_new_courier()
    
    if not courier_data:
        pytest.skip("Не удалось создать курьера для теста")
    
    # Получаем ID курьера для удаления
    login_response = login_courier(courier_data["login"], courier_data["password"])
    courier_id = login_response.json().get("id") if login_response.status_code == 200 else None
    
    yield courier_data
    
    # Постусловие: удаляем курьера
    if courier_id:
        delete_courier(courier_id)

@pytest.fixture
def courier_cleanup():
    """Фикстура для очистки БД после тестов"""
    courier_ids = []
    
    def add_courier_id(courier_id):
        courier_ids.append(courier_id)
    
    yield add_courier_id
    
    # Удаляем всех созданных курьеров
    for courier_id in courier_ids:
        if courier_id:
            delete_courier(courier_id)
