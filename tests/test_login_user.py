import allure
import pytest
from data import ResponseErrorMessage


class TestLoginUser:

    @allure.title('Проверка авторизации пользователя')
    def test_login_user(self, new_user):
        new_user.login_user()

        assert new_user.response.status_code == 200
        assert new_user.response.json()['success'] == True
        assert len(new_user.response.json()['user']) == 2
        assert bool(new_user.response.json()['accessToken']) == True
        assert bool(new_user.response.json()['refreshToken']) == True

    @allure.title('Проверка невозможности авторизации пользователя при некорректных данных')
    @pytest.mark.parametrize('email_string, password_string',[['abc', ''], ['', 'abc']])
    def test_login_user_uncorrect_data_error(self, new_user, email_string, password_string):
        email, password, name = new_user.register_new_user_and_return_login_password()
        new_user.login_user_with_data(email=email+email_string, password=password+password_string)

        assert new_user.response.status_code == 401
        assert new_user.response.json()['success'] == False
        assert new_user.response.json()['message'] == ResponseErrorMessage.LOGIN_USER_UNCORRECT_DATA_401

    @allure.title('Проверка невозможности авторизации пользователя при незаполненном обязательном поле')
    @pytest.mark.parametrize('email_slice, password_slice', [[0, 10], [19, 0]])
    def test_login_user_empty_field_error(self, new_user, email_slice, password_slice):
        email, password, name = new_user.register_new_user_and_return_login_password()
        new_user.login_user_with_data(email=email[:email_slice], password=password[:password_slice])

        assert new_user.response.status_code == 401
        assert new_user.response.json()['success'] == False
        assert new_user.response.json()['message'] == ResponseErrorMessage.LOGIN_USER_EMPTY_FIELD_401
