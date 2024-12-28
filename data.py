class UrlApi:

    BASE_URL = 'https://stellarburgers.nomoreparties.site/'

    API_REGISTER = 'api/auth/register'
    API_LOGIN = 'api/auth/login'
    API_USER = 'api/auth/user'
    API_INGREDIENTS = 'api/ingredients'
    API_ORDER = 'api/orders'


class ResponseErrorMessage:

    CREATE_TWO_SAME_USER_403 = 'User already exists'
    CREATE_USER_WITHOUT_REQUIRED_FIELD_403 = 'Email, password and name are required fields'
    LOGIN_USER_UNCORRECT_DATA_401 = 'email or password are incorrect'
    LOGIN_USER_EMPTY_FIELD_401 = 'email or password are incorrect'
    UPDATE_USER_WITHOUT_LOGIN_401 = 'You should be authorised'
    UPDATE_USER_MAIL_IN_DB_403 = 'User with such email already exists'
    CREATE_ORDER_EMPTY_DATA_400 = 'Ingredient ids must be provided'
    GET_USER_ORDER_WITHOUT_LOGIN_401 = 'You should be authorised'
