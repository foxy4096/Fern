from django import template

register = template.Library()

@register.filter
def is_image(filename):
    return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
