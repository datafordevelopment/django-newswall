"""
Facebook Graph Feed API Provider
================================

This provider needs `offline_access` permission.

See here how to get an access token with all permissions:
http://liquid9.tv/blog/2011/may/12/obtaining-permanent-facebook-oauth-access-token/

Required configuration keys::

    {
    "provider": "newswall.providers.fb_graph_feed",
    "object": "FEINHEIT",
    "from_id": "239846135569",
    "access_token": "..."
    }
"""

import urllib

from datetime import datetime
from django.utils import timezone
from django.conf import settings


import json

from newswall.providers.base import ProviderBase


class Provider(ProviderBase):
    def update(self):
        args = {'access_token' : self.config['access_token']}
        query = "https://graph.facebook.com/%s/feed?%s" % (self.config['object'], urllib.urlencode(args))
        file = urllib.urlopen(query)
        raw = file.read()
        response = json.loads(raw)

        from_id = self.config.get('from_id', None)

        for entry in response['data']:
            if from_id and entry['from']['id'] != from_id:
                continue

            if 'to' in entry: # messages
                continue

            link = 'https://facebook.com/%s' % entry['id'].replace('_', '/posts/')
            timestamp = datetime.strptime(entry['created_time'],
                                            '%Y-%m-%dT%H:%M:%S+0000')
            if getattr(settings, 'USE_TZ', False):
                timestamp = timezone.make_aware(timestamp, timezone.utc)

            kwargs = {
                'object_url': link,
                'title': entry.get('name') or entry.get('message') or entry.get('story', u''),
                'body': entry.get('message', u''),
                'image_url': entry.get('picture', u''),
                'timestamp': timestamp
            }
            if kwargs['title'] == kwargs['body']:
                kwargs['body'] = u''


            self.create_story(**kwargs)
