from datetime import timedelta
from django.utils import timezone

import difflib

from newswall.models import Story

VERIFY_CROSSPOST_DAYS = 2

class ProviderBase(object):
    def __init__(self, source, config):
        self.source = source
        self.config = config

    def update(self):
        raise NotImplementedError

    def create_story(self, object_url, **kwargs):
        force_update = kwargs.get('force_update', False)
        try:
            story = Story.objects.get(object_url=object_url)
        except Story.DoesNotExist:
            pass
        else:
            if not force_update:
                return story
            else:
                story.delete()

        defaults = {'source': self.source }
        defaults.update(kwargs)

        if defaults.get('title'):
            recent_stories = Story.objects.filter(is_active=True,
                              timestamp__gte=timezone.now()
                            - timedelta(days=VERIFY_CROSSPOST_DAYS))
            # check if the titles are similar
            for story in recent_stories:
                match = difflib.SequenceMatcher(None,
                                                defaults['title'], story.title)
                if match.ratio() > 0.6:
                    # the two stories are similar:
                    if self.source.priority <= story.source.priority:
                        defaults['is_active'] = False
                    else:
                        # deactivate the other story
                        story.deactivate()

        return Story.objects.get_or_create(object_url=object_url,
                                           defaults=defaults)

