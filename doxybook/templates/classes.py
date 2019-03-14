TEMPLATE = """
# Class Index

{% for letter, children in dictionary.items() %}
## {{letter}}

{% for node in children -%}
* [**{{node.name_short}}**]({{node.url}})
{%- if node.parent.is_language %}
 ([**{{node.parent.name_long}}**]({{node.parent.url}}))
{%- endif -%}
{% endfor %}
{% endfor %}
"""
