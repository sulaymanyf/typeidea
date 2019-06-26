from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from blog.adminforms import PostAdminForm
from blog.models import Category, Tag, Post
from django.contrib.admin.models import LogEntry

# 要在分类页面直接编辑文章
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site


class PostInline(admin.TabularInline):  # StackedInline样式不同
    fields = ('title', 'desc')
    extra = 1  # 默认有几个
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    # inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    # 要在分类页面直接编辑文章
    inlines = [PostInline, ]

    # 为了使当前登录用户为新建属性的作者,需要重写这里
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        print("------------request----------------")
        print(request)
        print("------------request----------------")
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')
    ''' request 是请求对象  obj 是当前要保存的对象, form是页面提交过来的表单对象  change是用于标志本次保存的数据是新增还是更新'''

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        print(request.user)
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset

    # 自定义过滤器只展示当前用户的分类
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')


@admin.register(Post, site=custom_site)
# @admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    # 配置列表页面展示哪些字段
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator',
    ]

    # 水平
    # filter_horizontal = ('tag',)
    # 垂直
    filter_vertical = ('tag',)
    # 配置那些字段可以作为链接, 点击 可以进入到编辑页面
    list_display_links = []

    # 配置页面过滤器 需要通过那些字段过滤列表页,
    # list_filter = ['category', ]
    # 使用自定义的过滤器
    list_filter = [CategoryOwnerFilter]
    # 配置搜索字段
    search_fields = ['title', 'category__name']

    # 保存 编辑, 新建按钮是否展示在顶部
    save_on_top = True

    # 动作相关配置, 是否展示在顶部
    actions_on_top = True

    # 动作相关配置, 是否展示在底部
    actions_on_bottom = True

    # 编辑页面是否展示在顶部
    save_on_top = True

    # 对于字段是否展示以及展示顺序的需求，可以通过 fields 或者 fieldset 来配置
    # 配置有两个作用, 1 是限定要展示的字段 2 配置展示字段的顺序
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    # fieldsets 用来控制布局，要求的格式是有两个元素的元组的list
    fieldsets = (
        ('基础信息', {
            "description": '基础信息配置',
            'fields': (
                ('title', "category"),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            )
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        }),

    )

    #  指定哪些字段是不展示的
    exclude = ['owner']

    # form_layout = (
    #     Fieldset(
    #         '基础信息',
    #         Row("title", "category"),
    #         'status',
    #         'tag',
    #     ),
    #     Fieldset(
    #         '内容信息',
    #         'desc',
    #         'is_md',
    #         'content_ck',
    #         'content_md',
    #         'content',
    #     )
    # )

    # 自定义list_display 中要展示的字段
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    # 指定表头的展示文案
    operator.short_description = '操作'

    # def post_count(self, obj):
    #     return obj.post_set.count()
    #
    # post_count.short_description = '文章数量'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    # 当前登录的用户在列表页中只能看到自己创建的文章
    # 数据过滤的关键在于找到数据源在哪里, 也就是queryset最终在哪里生产,就在那里进行过滤就行
    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    class Media:
        css = {
            'all': ("https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",),
        }
        js = ("https://code.jquery.com/jquery-3.3.1.slim.min.js",
              "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js",
              "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js")


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        'object_repr', 'object_id', 'action_flag',
        'user', 'change_message'
    ]
