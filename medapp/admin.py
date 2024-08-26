from django.contrib import admin
from medapp.models import Tag, Category, Blog, BlogSection

class BlogModelInline(admin.StackedInline):  
    model = BlogSection
    extra = 0

class BlogModelAdmin(admin.ModelAdmin):
    inlines = [BlogModelInline]

admin.site.register(Blog,BlogModelAdmin)
admin.site.register(Tag)
admin.site.register(Category)



