import pytest
from pytest_django.asserts import assertRedirects
from http import HTTPStatus

from django.urls import reverse


@pytest.mark.parametrize(
    'endpoint, args',
    (
        ('news:home', None),
        ('news:detail', (pytest.lazy_fixture('news_id'))),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    )
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, endpoint, args):
    url = reverse(endpoint, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'endpoint',
    ('news:edit', 'news:delete')
)
def test_pages_availability_for_different_users(
        parametrized_client, endpoint, comment, expected_status
):
    url = reverse(endpoint, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'endpoint',
    ('news:edit', 'news:delete')
)
@pytest.mark.django_db
def test_redirects(client, endpoint, comment):
    login_url = reverse('users:login')
    url = reverse(endpoint, args=(comment.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
