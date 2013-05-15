""" optimized for use with the feincms_nav and recursetree template tag. """
from django.utils.translation import ugettext_lazy as _, ugettext

from .common import *


class RNewswallDateNavigationExtension(NavigationExtension):
    """
    Special version optimized for recursetree template tag
    """
    name = _('Newswall date')

    def children(self, page, **kwargs):

        for year, months in date_tree():
            def return_months():
                for month in months:
                    yield PagePretender(
                        title=u'%s' % ugettext(all_months[month-1].strftime('%B')),
                        url='%s%04d/%02d/' % (page.get_absolute_url(), year, month),
                        tree_id=page.tree_id, # pretty funny tree hack
                        level=page.level+2,
                        language=getattr(page, 'language', settings.LANGUAGE_CODE),
                        slug='%04d/%02d' % (year, month),
                    )
            yield PagePretender(
                title=u'%s' % year,
                url='%s%s/' % (page.get_absolute_url(), year),
                tree_id=page.tree_id, # pretty funny tree hack
                language=getattr(page, 'language', settings.LANGUAGE_CODE),
                level=page.level+1,
                slug='%s' % year,
                parent=page,
                get_children=return_months,
                )
