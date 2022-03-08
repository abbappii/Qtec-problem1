from django.contrib import admin
from .models import  *
# Register your models here.

admin.site.register(Room)
admin.site.register(Keyword)
@admin.register(Keywordsearch)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ['user', 'keyword', 'total_search', 'created', ]
