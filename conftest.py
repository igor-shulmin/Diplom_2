import pytest
from api_requests import ApiRequestsUserOrder


@pytest.fixture
def new_user():
    new_user = ApiRequestsUserOrder()

    yield new_user

    new_user.delete_user()
