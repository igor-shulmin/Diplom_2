import allure
from helpers import Generate
from data import ResponseErrorMessage
import pytest


class TestCreateUser:

    @allure.title('Проверка создания аккаунта пользователя')
    def test_create_user(self, new_user):

        assert len(new_user.register_new_user_and_return_login_password()) == 3
        assert new_user.response.status_code == 200
        assert new_user.response.json()['success'] == True
        assert len(new_user.response.json()['user']) == 2
        assert bool(new_user.response.json()['accessToken']) == True
        assert bool(new_user.response.json()['refreshToken']) == True

    @allure.title('Проверка невозможности создания одинаковых аккаунтов пользователя')
    def test_create_two_same_user_error(self, new_user):
        email, password, name = new_user.register_new_user_and_return_login_password()
        new_user.register_new_user_with_data(email, password, name)

        assert new_user.response.status_code == 403
        assert new_user.response.json()['success'] == False
        assert new_user.response.json()['message'] == ResponseErrorMessage.CREATE_TWO_SAME_USER_403

    @allure.title('Проверка невозможности создания аккаунта курьера без заполнения обязательного поля')
    @pytest.mark.parametrize('email, password, name', [[None, Generate.generate_random_string(), Generate.generate_random_string()],
                                                       [Generate.generate_mail(), None, Generate.generate_random_string()],
                                                       [Generate.generate_mail(), Generate.generate_random_string(), None]])
    def test_create_user_without_required_field_error(self, new_user, email, password, name):
        new_user.register_new_user_with_data(email=email, password=password, name=name)

        assert new_user.response.status_code == 403
        assert new_user.response.json()['success'] == False
        assert new_user.response.json()['message'] == ResponseErrorMessage.CREATE_USER_WITHOUT_REQUIRED_FIELD_403
