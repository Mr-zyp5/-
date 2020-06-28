from django import template
from myadmin import models
register = template.Library()
from django.utils.html import format_html
@register.simple_tag
def nav():
    cates1 = models.Cates.objects.filter(upid=0)
    str1 = ''
    for i in cates1:
        str1 += '''
            <li class='layout-header-nav-item'><a href="/static/myhome/list.html" class="layout-header-nav-link">{name}</a></li>
        '''.format(name=i.name)
    return  format_html(str1)