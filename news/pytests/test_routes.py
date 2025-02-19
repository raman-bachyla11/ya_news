from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "client_fixture, url, expected_status",
    (
        # Public endpoints
        (
            pytest.lazy_fixture("client"),
            pytest.lazy_fixture("home_page_url"),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture("client"),
            pytest.lazy_fixture("news_detail_url"),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture("client"),
            pytest.lazy_fixture("login_page_url"),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture("client"),
            pytest.lazy_fixture("logout_page_url"),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture("client"),
            pytest.lazy_fixture("signup_page_url"),
            HTTPStatus.OK
        ),
        # Protected endpoints
        (
            pytest.lazy_fixture("author_client"),
            pytest.lazy_fixture("comment_edit_url"),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture("not_author_client"),
            pytest.lazy_fixture("comment_edit_url"),
            HTTPStatus.NOT_FOUND
        ),
        (
            pytest.lazy_fixture("author_client"),
            pytest.lazy_fixture("comment_delete_url"),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture("not_author_client"),
            pytest.lazy_fixture("comment_delete_url"),
            HTTPStatus.NOT_FOUND
        ),
    ),
)
def test_status_codes(client_fixture, url, expected_status):
    response = client_fixture.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "url, expected_url",
    (
        (
            pytest.lazy_fixture("comment_edit_url"),
            pytest.lazy_fixture("login_to_comment_edit_url")
        ),
        (
            pytest.lazy_fixture("comment_delete_url"),
            pytest.lazy_fixture("login_to_comment_delete_url")
        ),
    ),
)
def test_redirects(client, url, expected_url):
    response = client.get(url)
    assertRedirects(response, expected_url)
