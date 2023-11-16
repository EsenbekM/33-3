from django.contrib import admin
from django.http.request import HttpRequest
from news.models import News, Comments, Category, Tag


# admin.site.register(News)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active', 'view_count', 'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_filter = ('category', 'tag')
    list_editable = ('is_active', 'view_count')
    list_per_page = 10

    def has_add_permission(self, request: HttpRequest) -> bool:
        if request.user.is_superuser:
            return True
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False



admin.site.register(Comments)
admin.site.register(Category)
admin.site.register(Tag)
