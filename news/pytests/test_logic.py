from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


pytestmark = pytest.mark.django_db


COMMENT_FORM_DATA = {
    'text': 'Updated comment',
}
BAD_WORDS_CHECK = 'Какой-то текст, {word}, еще текст'
BAD_WORDS_DATA = [
    {'text': BAD_WORDS_CHECK.format(word=word)} for word in BAD_WORDS
]


def test_anonymous_user_cant_create_comment(
        client, news_detail_url, login_to_news_detail_url):
    response = client.post(news_detail_url, data=COMMENT_FORM_DATA)
    assertRedirects(response, login_to_news_detail_url)
    assert Comment.objects.count() == 0


def test_authorized_user_can_create_comment(
        author_client,
        news_detail_url,
        single_news_comment_url,
        author,
        single_news):
    response = author_client.post(news_detail_url, data=COMMENT_FORM_DATA)
    assertRedirects(response, single_news_comment_url)
    assert Comment.objects.count() == 1

    new_comment = Comment.objects.get()
    assert new_comment.text == COMMENT_FORM_DATA['text']
    assert new_comment.author == author
    assert new_comment.news == single_news


@pytest.mark.parametrize('data', BAD_WORDS_DATA)
def test_user_cant_use_bad_words(author_client, news_detail_url, data):
    response = author_client.post(news_detail_url, data=data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_non_author_cannot_delete_comment(
        not_author_client, comment_delete_url):
    comments_before = list(
        Comment.objects.values_list('id', 'author_id', 'news_id', 'text')
    )
    assert not_author_client.delete(
        comment_delete_url).status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == len(comments_before)
    comments_after = list(
        Comment.objects.values_list('id', 'author_id', 'news_id', 'text')
    )
    assert comments_before == comments_after


def test_author_can_delete_comment(author_client, comment_delete_url):
    response = author_client.delete(comment_delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(author_client, comment, comment_edit_url):
    response = author_client.post(comment_edit_url, data=COMMENT_FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == COMMENT_FORM_DATA['text']
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


def test_non_author_cannot_edit_comment(not_author_client, comment_edit_url):
    comments_before = list(
        Comment.objects.values_list('id', 'author_id', 'news_id', 'text')
    )
    assert not_author_client.post(
        comment_edit_url,
        data=COMMENT_FORM_DATA
    ).status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == len(comments_before)
    comments_after = list(
        Comment.objects.values_list('id', 'author_id', 'news_id', 'text')
    )
    assert comments_before == comments_after
