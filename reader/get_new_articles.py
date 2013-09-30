from datetime import datetime
from time import mktime
from operator import itemgetter

import feedparser
from django.db import models
from django.contrib.auth.models import User

from .models import feed, Article

def get_articles(feeds):

    parsed_feeds = []
    for feed in feeds:
        parsed_feed = []
        parsed_feed.append(feed[0]) # id of feed (foreign key)
        parsed_feed.append(feedparser.parse(feed[1])) # article data
        parsed_feeds.append(parsed_feed)

    feed_id = []
    feed_title = []
    article_titles = []
    article_links = []
    article_dates = []
    article_descriptions = []

    for feed in parsed_feeds:
        for entry in feed[1].entries:
            feed_id.append(feed[0])
            feed_title.append(feed[1].channel.title.encode('ascii', 'xmlcharrefreplace'))
            article_links.append(entry.link.encode('ascii', 'xmlcharrefreplace'))
            article_titles.append(entry.title.encode('ascii', 'xmlcharrefreplace'))
            date = datetime.fromtimestamp(mktime(entry.published_parsed))
            article_dates.append(date)

    articles_temp = zip(feed_id, feed_title, article_links, article_titles, article_dates)

    articles_temp_sorted = sorted(articles_temp, key=itemgetter(3), reverse=True)

    articles = []
    for feed_id, feed_title, link, title, date in articles_temp_sorted:
        article = [feed_id, feed_title, link, title, date]
        articles.append(article)

    return articles

def run():
    from .models import feed, Article
    all_feeds = feed.objects.all().values('topic', 'id', 'feed_url')

    feeds = []
    for q in all_feeds:
        feed_data = []
        feed_data.append(q['id'])
        feed_data.append(q['feed_url'])
        feeds.append(feed_data)

    articles = get_articles(feeds)

    for article in articles:
        id = article[0]
        u = feed.objects.filter(id=id).values('user')
        user_id = u[0]['user']
        user_object = User.objects.get(id=user_id)

        a = Article.objects.filter(url=article[2], user=user_id)
        # print "checking...."
        if len(a) == 0:
            # print "new article"
            a = Article(feed_id=article[0], user=user_object, feed_title=article[1], url=article[2], title=article[3], published_date=article[4])
            a.save()
        else:
            # print "already in db"
            pass