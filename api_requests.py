import random
import requests
from helpers import Generate
from data import UrlApi
import allure


class ApiRequests:

    def __init__(self):
        self.response = None


class ApiRequestsUserOrder(ApiRequests):

    @allure.step('Регистрируем нового пользователя')
    def register_new_user_and_return_login_password(self):
        login_pass = []

        email = Generate.generate_mail()
        password = Generate.generate_random_string()
        name = Generate.generate_random_string()

        payload = {
            'email': email,
            'password': password,
            'name': name
        }

        self.response = requests.post(f'{UrlApi.BASE_URL}/{UrlApi.API_REGISTER}', data=payload)

        if self.response.status_code == 200:
            login_pass.append(email)
            login_pass.append(password)
            login_pass.append(name)

            return login_pass

    @allure.step('Регистрируем нового пользователя с произвольными данными')
    def register_new_user_with_data(self, email=None, password=None, name=None):
        payload = {
            'email': email,
            'password': password,
            "name": name
        }

        self.response = requests.post(f'{UrlApi.BASE_URL}/{UrlApi.API_REGISTER}', data=payload)

    @allure.step('Авторизуем пользователя')
    def login_user(self):
        email, password, name = self.register_new_user_and_return_login_password()
        payload = {
            'email': email,
            'password': password
        }
        self.response = requests.post(f'{UrlApi.BASE_URL}/{UrlApi.API_LOGIN}', data=payload)

        return self.response.json()['accessToken']

    @allure.step('Авторизуем пользователя с произвольными данными')
    def login_user_with_data(self, email=None, password=None):
        payload = {
            'email': email,
            'password': password
        }
        self.response = requests.post(f'{UrlApi.BASE_URL}/{UrlApi.API_LOGIN}', data=payload)

    @allure.step('Изменяем данные пользователя с авторизацией')
    def update_user_data(self, email=None, password=None, name=None):
        payload = {
            'email': email,
            'password': password,
            'name': name
        }
        headers = {'Authorization': self.login_user()}
        self.response = requests.patch(f'{UrlApi.BASE_URL}/{UrlApi.API_USER}', data=payload, headers=headers)

    @allure.step('Изменяем данные пользователя без авторизации')
    def update_user_data_without_login(self, email, password, name):
        payload = {
            'email': email,
            'password': password,
            'name': name
        }
        self.response = requests.patch(f'{UrlApi.BASE_URL}/{UrlApi.API_USER}', data=payload)


    @allure.step('Создаём новый заказ')
    def create_new_order(self, authorization=True):
        self.response = requests.get(f'{UrlApi.BASE_URL}/{UrlApi.API_INGREDIENTS}')
        ingredients = [i['_id'] for i in self.response.json()['data']]
        random_ingredients = random.sample(ingredients, 2)

        payload = {
            'ingredients': random_ingredients
        }
        if authorization:
            headers = {'Authorization': self.login_user()}
            self.response = requests.post(f'{UrlApi.BASE_URL}/{UrlApi.API_ORDER}', data=payload, headers=headers)
        else:
            self.response = requests.post(f'{UrlApi.BASE_URL}/{UrlApi.API_ORDER}', data=payload)

    @allure.step('Создаём новый заказ с произвольными данными')
    def create_new_order_with_data(self, ingredients, authorization=True):
        payload = {
            'ingredients': ingredients
        }
        if authorization:
            headers = {'Authorization': self.login_user()}
            self.response = requests.post(f'{UrlApi.BASE_URL}/{UrlApi.API_ORDER}', data=payload, headers=headers)
        else:
            self.response = requests.post(f'{UrlApi.BASE_URL}/{UrlApi.API_ORDER}', data=payload)

    @allure.step('Получаем заказы конкретного пользователя')
    def get_user_order(self, authorization=True):
        if authorization:
            headers = {'Authorization': self.login_user()}
            self.response = requests.get(f'{UrlApi.BASE_URL}/{UrlApi.API_ORDER}', headers=headers)
        else:
            self.response = requests.get(f'{UrlApi.BASE_URL}/{UrlApi.API_ORDER}')

    @allure.step('Удаляем аккаунт пользователя')
    def delete_user(self):
        headers = {'Authorization': self.login_user()}
        self.response = requests.delete(f'{UrlApi.BASE_URL}/{UrlApi.API_USER}', headers=headers)
