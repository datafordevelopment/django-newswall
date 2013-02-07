from django.core.management.base import BaseCommand
from optparse import make_option

from newswall.models import Source, Story


class Command(BaseCommand):
    args = '<num>'
    help = 'Removes old entries. Requires amount of messages to keep'
    option_list = BaseCommand.option_list + (
        make_option('--dry-run', '-d',
            action='store_true',
            dest='dry_run',
            default=False,
            help="Dry run - Don't delete anything"),
        )


    def handle(self, *args, **options):
        num = int(args[0]);
        dry_run = options['dry_run']

        for source in Source.objects.filter(is_active=True):
            stories = source.stories.order_by('timestamp')
            length = len(stories)
            if length > num:
                stories = stories[:(length-num)]

                if dry_run:
                    print ("Stories that will be deleted: ")
                    for s in stories:
                        print "%s: %s\n" % (s.timestamp, s.title)
                else:
                    Story.objects.filter(pk__in=[s.pk for s in stories]).delete()
                    print "%s stories from source %s deleted." % (
                                length-num, source.name)
