{% extends "full.tpl" %}

{% block ipywidgets %}
{%- if "widgets" in nb.metadata -%}
<script>{{ include_template("nbconvert_templates/static/app.js") }}</script>
{%- endif -%}
{% endblock ipywidgets %}
