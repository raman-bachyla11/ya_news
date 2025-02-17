from django.urls import reverse
import pytest
from django.conf import settings
from django.test.client import Client
from news.models import Comment, News
from datetime import datetime, timedelta
from django.utils import timezone


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
    single_news = News.objects.create(
        title='Заголовок',
        text='Текст'
    )
    return single_news


@pytest.fixture
def bulk_news():
    today = datetime.today()
    bulk_news = News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return bulk_news


@pytest.fixture
def news_id(single_news):
    return (single_news.id,)


@pytest.fixture
def comment(single_news, author):
    comment = Comment.objects.create(
        news=single_news,
        author=author,
        text='Comment test'
    )
    return comment


@pytest.fixture
def bulk_comments(single_news, author):
    now = timezone.now()
    bulk_comments = Comment.objects.bulk_create(
        Comment(
            news=single_news,
            author=author,
            text=f'Tекст комментария{index}',
            created=now + timedelta(days=index)
        )
        for index in range(10)
    )
    return bulk_comments


@pytest.fixture
def comment_form_data(single_news):
    return {
        'news': single_news,
        'text': 'Updated comment'
    }


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
