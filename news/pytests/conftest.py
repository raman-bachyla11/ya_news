from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def single_news():
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def bulk_news():
    today = datetime.today()
    return News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment(single_news, author):
    return Comment.objects.create(
        news=single_news,
        author=author,
        text='Comment test'
    )


@pytest.fixture
def bulk_comments(single_news, author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=single_news,
            text=f'Comment text {index}',
            author=author,
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def news_detail_url(single_news):
    return reverse('news:detail', args=(single_news.id,))


@pytest.fixture
def comment_delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def comment_edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def home_page_url():
    return reverse('news:home')


@pytest.fixture
def login_page_url():
    return reverse('users:login')


@pytest.fixture
def logout_page_url():
    return reverse('users:logout')


@pytest.fixture
def signup_page_url():
    return reverse('users:signup')


@pytest.fixture
def login_to_news_detail_url(login_page_url, news_detail_url):
    return f'{login_page_url}?next={news_detail_url}'


@pytest.fixture
def single_news_comment_url(news_detail_url):
    return f'{news_detail_url}#comments'


@pytest.fixture
def login_to_comment_edit_url(login_page_url, comment_edit_url):
    return f'{login_page_url}?next={comment_edit_url}'


@pytest.fixture
def login_to_comment_delete_url(login_page_url, comment_delete_url):
    return f'{login_page_url}?next={comment_delete_url}'
