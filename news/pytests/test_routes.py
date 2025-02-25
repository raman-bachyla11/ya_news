from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db

CLIENT = pytest.lazy_fixture('client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')

HOME_PAGE_URL = pytest.lazy_fixture('home_page_url')
NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail_url')
LOGIN_PAGE_URL = pytest.lazy_fixture('login_page_url')
LOGOUT_PAGE_URL = pytest.lazy_fixture('logout_page_url')
SIGNUP_PAGE_URL = pytest.lazy_fixture('signup_page_url')

COMMENT_EDIT_URL = pytest.lazy_fixture('comment_edit_url')
COMMENT_DELETE_URL = pytest.lazy_fixture('comment_delete_url')
LOGIN_TO_COMMENT_EDIT_URL = pytest.lazy_fixture('login_to_comment_edit_url')
LOGIN_TO_COMMENT_DELETE_URL = pytest.lazy_fixture(
    'login_to_comment_delete_url')


@pytest.mark.parametrize(
    'client_fixture, url, expected_status',
    (
        # Public endpoints
        (CLIENT, HOME_PAGE_URL, HTTPStatus.OK),
        (CLIENT, NEWS_DETAIL_URL, HTTPStatus.OK),
        (CLIENT, LOGIN_PAGE_URL, HTTPStatus.OK),
        (CLIENT, LOGOUT_PAGE_URL, HTTPStatus.OK),
        (CLIENT, SIGNUP_PAGE_URL, HTTPStatus.OK),
        # Protected endpoints
        (AUTHOR_CLIENT, COMMENT_EDIT_URL, HTTPStatus.OK),
        (NOT_AUTHOR_CLIENT, COMMENT_EDIT_URL, HTTPStatus.NOT_FOUND),
        (CLIENT, COMMENT_EDIT_URL, HTTPStatus.FOUND),
        (AUTHOR_CLIENT, COMMENT_DELETE_URL, HTTPStatus.OK),
        (NOT_AUTHOR_CLIENT, COMMENT_DELETE_URL, HTTPStatus.NOT_FOUND),
        (CLIENT, COMMENT_DELETE_URL, HTTPStatus.FOUND),
    )
)
def test_status_codes(client_fixture, url, expected_status):
    assert client_fixture.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_url',
    [
        (COMMENT_EDIT_URL, LOGIN_TO_COMMENT_EDIT_URL),
        (COMMENT_DELETE_URL, LOGIN_TO_COMMENT_DELETE_URL),
    ]
)
def test_redirects(client, url, expected_url):
    assertRedirects(client.get(url), expected_url)
