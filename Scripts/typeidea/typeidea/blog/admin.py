from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post,Category,Tag

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','status','is_nav','created_time','post_count')
    fields = ('name','status','is_nav','owner')

    def save_model(self,request,obj,form,change):
        obj.owner = request.user
        return super(CategoryAdmin,self).save_model(request,obj,form,change)  #save_model为父类admin.ModelAdmin里的save_model方法（父类里有同名的方法，真实存在），不是这里的方法。

    def post_count(self,obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status','owner')

    def save_model(self,request,obj,form,change):
        obj.owner = request.user
        return super(TagAdmin,self).save_model(request,obj,form,change)   #save_model为父类admin.ModelAdmin里的save_model方法（父类里有同名的方法，真实存在），不是这里的方法。

class CategoryOwnerFileter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""

    title = '分类过滤器'
    parameter_name =  'owner_category'

    def lookups(self,request,model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self,request,queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id = self.value())
        return queryset

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','category','status','created_time','owner','operator']
    list_display_links = ['status']
    list_filter = [CategoryOwnerFileter]
    search_fields = ['title','category_name']

    actions_on_top = True
    actions_on_bottom = True

    #编辑页面
    #save_on_top = True

    fields =(
        'title',
        'desc',
        'content',
        ('category','status','tag')
    )

    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change',args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self,request,obj,form,change):
        obj.owner = request.user
        return super(PostAdmin,self).save_model(request,obj,form,change)