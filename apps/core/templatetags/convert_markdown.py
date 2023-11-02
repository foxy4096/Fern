import markdown
import bleach
from django import template
from django.template.defaultfilters import stringfilter
from apps.polls.templatetags.md_to_poll import PollExtension

register = template.Library()

# List of Markdown extensions to use
extensions = [
    "markdown.extensions.admonition",
    "pymdownx.extra",
    "pymdownx.tasklist",
    "pymdownx.magiclink",
    "pymdownx.emoji",
    "pymdownx.details",
    "pymdownx.superfences",
    "markdown.extensions.toc",
    "pymdownx.tabbed",
    "pymdownx.tilde",
    "pymdownx.snippets",
]

# Configuration options for specific extensions
extension_configs = {
    "pymdownx.tasklist": {
        "custom_checkbox": True,
    },
}

linkify_options = {
    "pymdownx.magiclink": {
        "hide_protocol": True,
        "social_url_shorthand": True,
        "social_url_shortener": True,
        "repo_url_shortener": True,
        "normalize_issue_symbols": True,
        "repo_url_shorthand": True,
    },
}


@register.filter(name="convert_markdown", is_safe=False)
@stringfilter
def convert_markdown(value, linkify=True):
    """
    Filter to convert Markdown text to HTML using specified extensions and configs.

    Args:
        value (str): The Markdown text to convert.
        user: User-related data (not used in this function).

    Returns:
        str: The converted HTML.
    """
    extension_conf = {**extension_configs}
    if linkify:
        extension_conf = {**extension_configs, **linkify_options}
    return markdown.markdown(
        text=bleach.clean(value).replace("&gt;", ">"),
        extensions=extensions,
        extension_configs=extension_conf,
    )
