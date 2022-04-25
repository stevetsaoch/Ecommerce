from django.template import Library

register = Library()

@register.filter(name="authorsin3")
def authorsin3(value):
    value_list = list(value)
    if len(value) >= 3:
        author_list = value_list[0:3]
    elif len(value) < 3:
        author_list = value_list
        while len(author_list) != 3:
            author_list.append("")
    return author_list


