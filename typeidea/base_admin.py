from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    抽出来的公告处理
    1. 用来处理文章、分类、标签、侧边栏、友链这些model的owner字段自动补充
    2. 用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner',)

    def get_list_queryset(self):
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(owner=request.user)

    # def save_models(self):
    #     self.new_obj.owner = self.request.user
    #     return super().save_models()
    # 当前登录的用户在列表页中只能看到自己创建的文章
    # 数据过滤的关键在于找到数据源在哪里, 也就是queryset最终在哪里生产,就在那里进行过滤就行
    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    #  吧当前用户保存到作者中
    def save_models(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_models(request, obj, form, change)
