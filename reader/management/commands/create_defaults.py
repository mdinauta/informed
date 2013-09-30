from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.contrib.auth.models import User

from reader.models import feed

class Command(BaseCommand):

	def handle(self, *args, **kwargs):
		default_user = User.objects.get(id=2)
		insert = feed.objects.create(user=default_user, topic='technology', feed_url='http://feeds.feedburner.com/TechCrunch/')
		insert.save()

		# self.stdout.write('Successfully created defaults')
