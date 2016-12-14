from django import template
from django.core.urlresolvers import reverse, resolve, Resolver404

register = template.Library()

@register.simple_tag
def navactive(request, view_name):
    path = resolve(request.path_info)
    # if request.path in ( reverse(url) for url in urls.split() ):
    # print(request.path)
    try:
        return "pure-menu-selected" if path.url_name == view_name else ""
    except Resolver404:
        return ""