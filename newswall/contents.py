from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.template.loader import render_to_string

from .models import Story, Source

class NewswallContent(models.Model):
    num_stories = models.PositiveSmallIntegerField(_('stories'), default=3)

    class Meta:
        abstract =  True
        verbose_name = _('Newswall')
        verbose_name_plural = _('Newswalls')

    def render(self, request, **kwargs):
        stories = []
        sources = Source.objects.select_related('stories').filter(show_min__gt=0)
        # no sanity check here for performance reasons
        for source in sources:
            stories.extend(source.stories.active()[:source.show_min])
        others = Story.objects.active()[:self.num_stories]
        # fill up the list with remaining new stories.
        for story in others:
            if len(stories) < self.num_stories:
                if story not in stories:
                    stories.append(story)
            else:
                break

        context = {
            'stories': stories[:self.num_stories]
        }
        return render_to_string([
            'content/newswall/{0}_default.html'.format(self.region),
            'content/newswall/default.html'
        ], context, context_instance=RequestContext(request))
