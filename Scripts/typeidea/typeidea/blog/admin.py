from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post,Category,Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


class PostInline(admin.TabularInline):
    fields = ('title','desc')
    extra = 1
    model = Post


# Register your models here.
@admin.register(Category,site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name','status','is_nav','created_time','post_count')
    fields = ('name','status','is_nav','owner')
    inlines = [PostInline,]
    def save_model(self,request,obj,form,change):
        obj.owner = request.user
        return super(CategoryAdmin,self).save_model(request,obj,form,change)  #save_model为父类admin.ModelAdmin里的save_model方法（父类里有同名的方法，真实存在），不是这里的方法。

    def post_count(self,obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'
@admin.register(Tag,site=custom_site)
class TagAdmin(BaseOwnerAdmin):
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

@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title','category','status',
        'created_time','owner',
        'operator'
    ]
    list_display_links = ['status']
    list_filter = [CategoryOwnerFileter]
    search_fields = ['title','category_name']

    actions_on_top = True
    actions_on_bottom = True

    #编辑页面
    #save_on_top = True
    exclude = ('owner',)

    fieldsets = (
        ('基础配置',{
            'description':'基础配置描述',
            'fields':(
                ('title','category'),
                'status',
            ),
        }),
        ('内容',{
            'fields':(
                'desc','content',
            ),
        }),
        ('额外信息',{
            'classes':('collapse',),
            'fields':('tag',),
        })
    )

    filter_horizontal = ('tag',)

    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change',args=(obj.id,))
        )
    operator.short_description = '操作'

    

    #自定义静态资源引入
    '''class Media:
        css={
            'all':('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )'''

