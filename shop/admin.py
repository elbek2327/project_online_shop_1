from django.contrib import admin
from django.contrib.auth.models import Group
from shop.models import Product, Category, Comment
from adminsortable2.admin import SortableAdminMixin

from import_export import resources
from django.utils.html import format_html




admin.site.unregister(Group)


@admin.register(Category)
class CategoryModelAdmin(SortableAdminMixin, admin.ModelAdmin):

    list_display = ['id','title','my_order']
    search_fields = ['title']
    list_filter = ['updated_at']
    ordering = ('my_order',)



class ProductResource(resources.ModelResource):
    class Meta:
        model = Product








@admin.register(Product)
class ProductModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    resource_class = ProductResource
    list_display = ['id','name','price','image_tag','my_order']
    search_fields = ['name','description']
    list_filter = ['updated_at', 'category']
    ordering = ('my_order',)

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width: 50px; max-height:50px" /> '.format(obj.image.url))
    image_tag.short_description = 'Image'





@admin.register(Comment)
class CommentModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    resource_class = ProductResource
    list_display = ['id','commenter_name','comment','product','date_added', ]
    search_fields = ['commenter_name','date_added']
    list_filter = ['date_added']
    ordering = ('my_order',)



