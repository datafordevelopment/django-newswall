"""
RSS Feed Provider
=================

Required configuration keys::

    {
    "provider": "newswall.providers.feed",
    "source": "http://twitter.com/statuses/user_timeline/feinheit.rss"
    }
"""
from datetime import datetime
from django.utils import timezone
from django.conf import settings
import feedparser
import time

from newswall.providers.base import ProviderBase


class Provider(ProviderBase):
    def update(self):
        feed = feedparser.parse(self.config['source'])
        for entry in feed['entries']:
            if hasattr(entry, 'date_parsed'):
                timestamp = datetime.fromtimestamp(
                    time.mktime(entry.date_parsed))
                if getattr(settings, 'USE_TZ', False):
                    timestamp = timezone.make_aware(timestamp, timezone.utc)
            elif hasattr(entry, 'published_parsed'):
                timestamp = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                if getattr(settings, 'USE_TZ', False):
                    timestamp = timezone.make_aware(timestamp, timezone.utc)
            else:
                timestamp = timezone.now()
            self.create_story(entry.link,
                title=entry.title,
                body=entry.description,
                timestamp=timestamp,
            )
