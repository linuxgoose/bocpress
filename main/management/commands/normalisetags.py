# main/management/commands/normalize_tags.py
from django.core.management.base import BaseCommand
from main.models import Post

class Command(BaseCommand):
    help = "Normalize tags on all posts"

    def handle(self, *args, **options):
        posts = Post.objects.all()
        for post in posts:
            if post.tags:
                cleaned_tags = [t.strip() for t in post.tags.split(",") if t.strip()]
                post.tags = ",".join(cleaned_tags)
                post.save()
        self.stdout.write(self.style.SUCCESS("All posts tags normalised."))
