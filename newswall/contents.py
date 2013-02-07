from django.db import models
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from newswall.models import Story


class NewswallContent(models.Model):
    class Meta:
        abstract =  True
        verbose_name = _('Newswall')
        verbose_name_plural = _('Newswalls')

    def render(self, request, **kwargs):
        context = {
            'stories': Story.objects.active()[:3]
        }
        return render_to_string([
            'content/newswall/{0}_default.html'.format(self.region),
            'content/newswall/default.html'
        ], context, context_instance=RequestContext(request))
