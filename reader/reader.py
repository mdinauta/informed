from datetime import datetime
import time
from time import mktime
from operator import itemgetter

import feedparser
import sqlite3

def get_articles(feeds):

    parsed_feeds = []
    for feed in feeds:
        parsed_feed = []
        parsed_feed.append(feed[0])
        parsed_feed.append(feedparser.parse(feed[1]))
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
    connect = sqlite3.connect("../informed/informed.db")
    cursor = connect.cursor()
    # select = "PRAGMA table_info([reader_Article])"
    # select = "select name from sqlite_master where type = 'table';"
    select = "SELECT * FROM reader_feed"
    cursor.execute(select)
    data = cursor.fetchall()
    cursor.close()
    connect.close()
    # for r in data:
    #     print r

    feeds = []
    for topic, user, feed_id, url in data:
        feed = []
        feed.append(feed_id)
        feed.append(url)
        feeds.append(feed)

    connect = sqlite3.connect("../informed/informed.db")
    cursor = connect.cursor()
    articles = get_articles(feeds)
    for article in articles:
        select = "SELECT * FROM reader_Article WHERE url = \"" + str(article[2]) + "\""
        cursor.execute(select)
        data = cursor.fetchall()
        if data == []:
            insert = "INSERT INTO reader_Article (feed_id, feed_title, url, title, pusblished_date) VALUES (" + str(article[0]) + ",\"" + article[1] + "\",\"" + article[2] + "\",\"" + article[3] + "\",\"" + str(article[4]) + "\");"
            print insert
            try:
                cursor.execute(insert)
                connect.commit()
            except:
                print "caught error"
                continue
            print "inserted to db"
        else:
            print "already in db"
            pass

# run()

# connect = sqlite3.connect("../informed/informed.db")
# cursor = connect.cursor()
# select = "SELECT * FROM reader_Article"
# cursor.execute(select)
# data = cursor.fetchall()

# for r in data:
#     print r


