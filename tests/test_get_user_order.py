import allure
from data import ResponseErrorMessage


class TestGetUserOrder:

    @allure.title('Проверка получения заказов пользователя с авторизацией')
    def test_get_user_order(self, new_user):
        new_user.get_user_order()

        assert new_user.response.status_code == 200
        assert new_user.response.json()['success'] == True
        assert 0 <= len(new_user.response.json()['orders']) <= 50
        assert type(new_user.response.json()['total']) == int
        assert type(new_user.response.json()['totalToday']) == int

    @allure.title('Проверка получения заказов пользователя без авторизации')
    def test_get_user_order_without_login_error(self, new_user):
        new_user.get_user_order(authorization=False)

        assert new_user.response.status_code == 401
        assert new_user.response.json()['success'] == False
        assert new_user.response.json()['message'] == ResponseErrorMessage.GET_USER_ORDER_WITHOUT_LOGIN_401
