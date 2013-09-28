from django.contrib import admin
from models import feed, Article

# class ArticleAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("name",)}

admin.site.register(feed)
admin.site.register(Article)
