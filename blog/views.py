from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def post_list(request, category_id=None, tag_id=None):
    return render(request, 'blog/list.html', context={'name': 'post_list'})


def post_detail(request, post_id):
    return render(request, 'blog/detail.html', context={'name': 'post_detail'})


'''def render(request, template_name, context=None, content_type=None, status=None, using=None): 
        request: 封装了 HTTP 请求的 request 对象
        template_name: 模板名称，可以像前面的代码那样带上路径
        context: 字典数据，它会传递到模板中
        content_type: 页面编码类型，默认值是 text/html
        status:：状态码，默认值是200
        using:使用了哪种模板引擎解析，这可以在settings 中配置，默认使用 django 自带的模板
'''
