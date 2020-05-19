{% extends "full.tpl" %}

{% block ipywidgets %}
{%- if "widgets" in nb.metadata -%}
<script>{{ include_template("nbconvert_templates/static/app.js") }}</script>
illusionist_resource
{%- endif -%}
{% endblock ipywidgets %}
