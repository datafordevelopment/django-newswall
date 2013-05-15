from django import template
from datetime import date
from newswall.models import Source, Story
from django.utils.datastructures import SortedDict
import re

register = template.Library()


@register.assignment_tag
def newswall_sources():
    return Source.objects.active()


@register.assignment_tag
def newswall_archive_months():
    return Story.objects.active().dates('timestamp', 'month', 'DESC')


YEAR_RE = re.compile(r'/(\d{4})/')

@register.assignment_tag
def newswall_archive(path):
    """
    {% newswall_archive request.path as archive %}
    {% with base="/{{ LANGUAGE_CODE }}/blog/" %}
    <ul class="toc">
        <li class="title"><a href="{{ base }}">Archiv</a></li>
        {% for year, months in archive.items %}
            <li><a href="{{ base }}{{ year }}/">{{ year }}</a></li>
            {% for month in months %}
                <li><a href="{{ base }}{{ month|date:"Y/m/" }}">&nbsp; &nbsp; {{ month|date:"F" }}</a></li>
            {% endfor %}
        {% endfor %}
    </ul>
    {% endwith %}
    :param path: request.path
    :return: SortedDict containing the dates which contain entries.
    """
    match = YEAR_RE.search(path)
    if match:
        year = int(match.group(1))
    else:
        year = date.today().year

    archive = SortedDict()
    for month in Story.objects.active().dates('timestamp', 'month', 'DESC'):
        archive.setdefault(month.year, [])
        if month.year == year:
            archive.setdefault(month.year, []).append(month)
    return archive