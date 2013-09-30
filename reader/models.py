import datetime

from django.db import models
from django.contrib.auth.models import User


class feed(models.Model):
    user = models.ForeignKey(User)
    topic = models.CharField(default="news", max_length=1000)
    feed_url = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.feed_url

    def name(self):
        return self.name


class Article(models.Model):
    feed = models.ForeignKey(feed)
    user = models.ForeignKey(User)
    feed_title = models.CharField(default="Feed title not available",max_length=5000)
    url = models.CharField(max_length=5000)
    title = models.CharField(default="Article title not available",max_length=5000)
    published_date = models.DateTimeField()
    starred = models.BooleanField()

    def __unicode__(self):
        return self.title