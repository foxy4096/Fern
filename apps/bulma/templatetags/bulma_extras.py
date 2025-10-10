from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def render_file_widget(field, css_class="file-input"):
    """Manually render a file input widget with custom attrs (e.g., for Bulma)."""
    widget = field.field.widget
    attrs = {
        "id": field.auto_id,
        "class": css_class,
    }
    return mark_safe(widget.render(name=field.html_name, value=None, attrs=attrs))
