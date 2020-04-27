from django.contrib import admin
from .models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ["title","pub_date",'slug']
    list_display_links = ["pub_date"]
    list_filter = ["pub_date"]
    search_fields = ["title","content"]
    list_editable = ["title"]
    #prepopulated_fields = {'slug':('title',)}

    class Meta:
        model=Post

admin.site.register(Post,PostAdmin)