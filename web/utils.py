import markdown

from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def markdown_to_text(text):
    return markdown.markdown(text)
