from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = '我的地盘'
    site_title = '管理后台'
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')
