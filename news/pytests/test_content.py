import pytest
from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


HOME_URL = reverse('news:home')


@pytest.mark.django_db
def test_news_count(author_client, bulk_news):
    response = author_client.get(HOME_URL)
    news_list = response.context['object_list']
    assert news_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(author_client, bulk_news):
    response = author_client.get(HOME_URL)
    news_list = response.context['object_list']
    all_dates = [news.date for news in news_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comment_order(bulk_comments):
    all_timestamps = [comment.created for comment in bulk_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, news_id):
    url = reverse('news:detail', args=news_id)
    response = author_client.get(url)
    assert ('form' in response.context) is True
    assert isinstance(response.context['form'], CommentForm)


@pytest.mark.django_db
def test_unauthorized_client_hasnt_form(client, news_id):
    url = reverse('news:detail', args=news_id)
    response = client.get(url)
    assert ('form' in response.context) is False
