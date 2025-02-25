import pytest
from django.conf import settings

from news.forms import CommentForm


pytestmark = pytest.mark.django_db


def test_news_count(author_client, bulk_news, home_page_url):
    assert author_client.get(
        home_page_url
    ).context['object_list'].count() == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(author_client, bulk_news, home_page_url):
    news_list = author_client.get(home_page_url).context['object_list']
    all_dates = [news.date for news in news_list]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comment_order(bulk_comments, news_detail_url, author_client):
    comments = list(
        author_client.get(news_detail_url).context['object'].comment_set.all()
    )
    all_timestamps = [comment.created for comment in comments]
    assert all_timestamps == sorted(all_timestamps)


def test_authorized_client_has_form(author_client, news_detail_url):
    assert isinstance(
        author_client.get(news_detail_url).context['form'], CommentForm
    )


def test_unauthorized_client_hasnt_form(client, news_detail_url):
    assert 'form' not in client.get(news_detail_url).context
