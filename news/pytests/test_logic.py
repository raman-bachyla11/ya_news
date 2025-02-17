from http import HTTPStatus
from pytest_django.asserts import assertRedirects, assertFormError
from django.urls import reverse
import pytest
from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
        client, comment_form_data, news_detail_url):
    response = client.post(news_detail_url, data=comment_form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={news_detail_url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_authorized_user_can_create_comment(
        author_client, comment_form_data, news_detail_url):
    response = author_client.post(news_detail_url, data=comment_form_data)
    assertRedirects(response, f'{news_detail_url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == comment_form_data['text']


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client, news_detail_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(news_detail_url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


@pytest.mark.parametrize(
    'parametrized_client, expected_status, comment_count',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND, 1),
        (pytest.lazy_fixture('author_client'), HTTPStatus.FOUND, 0)
    ),
)
def test_parametrized_users_delete_comment(
        parametrized_client,
        expected_status,
        comment_count,
        comment_delete_url):
    response = parametrized_client.delete(comment_delete_url)
    assert response.status_code == expected_status
    assert Comment.objects.count() == comment_count


@pytest.mark.parametrize(
    'parametrized_user, expected_status, should_update',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.FOUND, True),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND, False)
    ),
)
@pytest.mark.django_db
def test_parametrized_users_edit_comment(
        parametrized_user,
        expected_status,
        should_update,
        comment,
        comment_form_data,
        comment_edit_url):
    original_text = comment.text
    response = parametrized_user.post(comment_edit_url, data=comment_form_data)
    comment.refresh_from_db()
    assert response.status_code == expected_status
    if should_update:
        assert comment.text == comment_form_data['text']
    else:
        assert comment.text == original_text
