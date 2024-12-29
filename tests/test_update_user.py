import allure
import pytest
from helpers import Generate
from data import ResponseErrorMessage


class TestUpdateUser:

    @allure.title('Проверка изменения данных пользователя с авторизацией')
    @pytest.mark.parametrize('email, password, name',
                             [[Generate.generate_mail(), None, None], [None, Generate.generate_random_string(), None],
                              [None, None, Generate.generate_random_string()]])
    def test_update_user(self, new_user, email, password, name):
        new_user.update_user_data(email, password, name)

        assert new_user.response.status_code == 200
        assert new_user.response.json()['success'] == True
        assert len(new_user.response.json()['user']) == 2

    @allure.title('Проверка изменения почты пользователя на уже существующую в базе данных')
    def test_update_user_mail_in_db_error(self, new_user):
        email, password, name = new_user.register_new_user_and_return_login_password()
        new_user.register_new_user_and_return_login_password()
        new_user.update_user_data(email=email)

        assert new_user.response.status_code == 403
        assert new_user.response.json()['success'] == False
        assert new_user.response.json()['message'] == ResponseErrorMessage.UPDATE_USER_MAIL_IN_DB_403

    @allure.title('Проверка изменения данных пользователя без авторизации')
    @pytest.mark.parametrize('email, password, name',
                             [[Generate.generate_mail(), None, None], [None, Generate.generate_random_string(), None],
                              [None, None, Generate.generate_random_string()]])
    def test_update_user_without_login_error(self, new_user, email, password, name):
        new_user.update_user_data_without_login(email, password, name)

        assert new_user.response.status_code == 401
        assert new_user.response.json()['success'] == False
        assert new_user.response.json()['message'] == ResponseErrorMessage.UPDATE_USER_WITHOUT_LOGIN_401
