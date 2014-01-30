# informed.io is deployed to Heroku. Heroku's free database tier allows for 10k rows. 
# Since the app has no users as of 11/2/2013, I want to keep it free, so I'm going to 
# use this to delete some demo articles when the number approaches ~9k

import operator

from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

from reader.models import feed, Article

#get number of articles under demo user

class Command(BaseCommand):

	def handle(self, *args, **kwargs):

		demo_user = User.objects.get(username='demo')
		demo_articles_count = Article.objects.filter(user=demo_user).count()
		
		# if the count is > 8,000, delete 1,000 of the oldest articles
		if demo_articles_count > 8000:
			# will order ascending (oldest > newest)
			demo_articles = Article.objects.filter(user=demo_user).order_by('published_date')
			for article in demo_articles[:1000]:
				Article.delete(article)
		else:
			pass
