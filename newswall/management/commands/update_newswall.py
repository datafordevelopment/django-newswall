from django.core.management.base import NoArgsCommand
from django.utils import importlib
import json

from newswall.models import Source


class Command(NoArgsCommand):
    help = 'Updates all active sources'

    def handle_noargs(self, **options):
        for source in Source.objects.filter(is_active=True):
            try:
                config = json.loads(source.data)
            except ValueError as e:
                raise ValueError("Malformed JSON data in configuration for %s" % source)
            provider = importlib.import_module(config['provider']).Provider(source, config)
            provider.update()
