from django.utils.translation import ugettext_lazy as _, ugettext

from .common import *

class NewswallDateNavigationExtension(NavigationExtension):
    """
    Navigation extension for FeinCMS which shows a year and month Breakdown:
    2012
        April
        March
        February
        January
    2011
    2010
    """
    name = _('Newswall date')

    def children(self, page, **kwargs):
        for year, months in date_tree():
            yield PagePretender(
                title=u'%s' % year,
                url='%s%s/' % (page.get_absolute_url(), year),
                tree_id=page.tree_id, # pretty funny tree hack
                lft=0,
                rght=len(months)+1,
                level=page.level+1,
                slug='%s' % year,
                )
            for month in months:
                yield PagePretender(
                    title=u'%s' % ugettext(all_months[month-1].strftime('%B')),
                    url='%s%04d/%02d/' % (page.get_absolute_url(), year, month),
                    tree_id=page.tree_id, # pretty funny tree hack
                    lft=0,
                    rght=0,
                    level=page.level+2,
                    slug='%04d/%02d' % (year, month),
                )
