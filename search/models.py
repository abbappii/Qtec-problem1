from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')
    search_keyword = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.search_keyword


class Keyword(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'


class Keywordsearch(models.Model):
    # foreign key
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_keywords')
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='search_keyword_users')

    total_search = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Keyword Search'
        verbose_name_plural = 'Keywords Search'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'keyword'],
                name='user_keyword_unique'
            )
        ]

    def __str__(self):
        return f'{self.keyword}'
