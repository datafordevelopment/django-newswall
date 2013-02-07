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
        length = len(stories)
        # cache source for template.
        for source in sources:
            l=source.stories.active()[:source.show_min]
            for s in l:
                s.source = source
            stories.extend(l)
        if length < self.num_stories:
            others = Story.objects.active().select_related('source')[:self.num_stories]
            # fill up the list with remaining new stories.
            for story in others:
                if length < self.num_stories:
                    if story not in stories:
                        stories.append(story)
                else:
                    break

        if len(stories) > self.num_stories:
            stories = stories[:self.num_stories]

        context = {
            'stories': stories
        }
        return render_to_string([
            'content/newswall/{0}_default.html'.format(self.region),
            'content/newswall/default.html'
        ], context, context_instance=RequestContext(request))
