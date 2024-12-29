import allure
from data import ResponseErrorMessage
import pytest


class TestCreateOrder:

    @allure.title('Проверка создания заказа с авторизацией')
    def test_create_order(self, new_user):
        new_user.create_new_order()

        assert new_user.response.status_code == 200
        assert new_user.response.json()['success'] == True
        assert len(new_user.response.json()['order']) == 9
        assert bool(new_user.response.json()['order']['owner']) == True
        assert new_user.response.json()['order']['status'] == 'done'

    @allure.title('Проверка создания заказа без авторизации')
    def test_create_order_without_login(self, new_user):
        new_user.create_new_order(authorization=False)

        assert new_user.response.status_code == 200
        assert new_user.response.json()['success'] == True
        assert len(new_user.response.json()['order']) == 1
        assert 'owner' not in new_user.response.json()['order']
        assert 'status' not in new_user.response.json()['order']

    @allure.title('Проверка создания заказа c некорректными данными')
    @pytest.mark.parametrize('authorization', [True, False])
    def test_create_order_uncorrect_data_error(self, new_user, authorization):
        new_user.create_new_order_with_data(ingredients=['123abc', '456def'], authorization=authorization)

        assert new_user.response.status_code == 500

    @allure.title('Проверка создания заказа без ингредиентов')
    @pytest.mark.parametrize('authorization', [True, False])
    def test_create_order_empty_data_error(self, new_user, authorization):
        new_user.create_new_order_with_data(ingredients=[], authorization=authorization)

        assert new_user.response.status_code == 400
        assert new_user.response.json()['success'] == False
        assert new_user.response.json()['message'] == ResponseErrorMessage.CREATE_ORDER_EMPTY_DATA_400
