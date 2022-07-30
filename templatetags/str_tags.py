from django import template

register = template.Library() # Djangoのテンプレートタグライブラリ

# カスタムタグとして登録する
@register.simple_tag
def concat_str(value1, value2):
    return str(value1) + str(value2)