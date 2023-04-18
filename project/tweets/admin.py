from django.contrib import admin
from .models import Tag, Page, Tweet, Comment

admin.site.register(Tag)
admin.site.register(Page)
admin.site.register(Tweet)
admin.site.register(Comment)
