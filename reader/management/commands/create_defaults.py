from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.contrib.auth.models import User

from reader.models import feed


class Command(BaseCommand):

	def handle(self, *args, **kwargs):

		default_user = User.objects.get(username='demo')
		feed_dicts = [
					{'topic': 'technology', 'feed_url': 'http://feeds.feedburner.com/TechCrunch/'},
					{'topic': 'technology', 'feed_url': 'http://feeds.feedburner.com/hacker-news-feed-50?format=xml'},
					{'topic': 'pop culture', 'feed_url': 'http://feeds.gawker.com/gawker/full'},
					{'topic': 'news', 'feed_url': 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'},
					{'topic': 'programming', 'feed_url': 'http://www.reddit.com/r/django/.rss'},
					{'topic': 'programming', 'feed_url': 'http://www.reddit.com/r/programming/.rss'},
					{'topic': 'music', 'feed_url': 'http://feeds.theonion.com/avclub/music/'},
					{'topic': 'pop culture', 'feed_url': 'http://feeds.theonion.com/avclub/newswire/'},
					{'topic': 'movies', 'feed_url': 'http://www.rottentomatoes.com/syndication/rss/in_theaters.xml'},
					{'topic': 'programming', 'feed_url': 'http://feeds.feedburner.com/nettuts'},
					{'topic': 'programming', 'feed_url': 'http://www.reddit.com/r/python/.rss'},
					{'topic': 'statistics', 'feed_url': 'http://feeds.feedburner.com/SimplyStatistics'},
					{'topic': 'statistics', 'feed_url': 'http://mathbabe.org/feed/'},
					{'topic': 'music', 'feed_url': 'http://www.okayplayer.com/news/feed/'},
					{'topic': 'statistics', 'feed_url': 'http://blog.priceonomics.com/'},	
					{'topic': 'statistics', 'feed_url': 'http://www.dataists.com/feed/'},
					{'topic': 'statistics', 'feed_url': 'http://flowingdata.com/feed/'},
					{'topic': 'san francisco', 'feed_url': 'http://smashingreader.com/The_Bold_Italic_s28463'},
					{'topic': 'san francisco', 'feed_url': 'http://www.reddit.com/r/sanfrancisco/.rss'},
					]
		for a in feed_dicts:
			already_exists = feed.objects.filter(topic=a['topic'], feed_url=a['feed_url'])
			if len(already_exists) == 0:
				insert = feed.objects.create(user=default_user, topic=a['topic'], 
											feed_url=a['feed_url'])
				insert.save()
			else:
				pass

		self.stdout.write('Successfully created defaults')
