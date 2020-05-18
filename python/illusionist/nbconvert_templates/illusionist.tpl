{% extends "full.tpl" %}


{% block html_head_js %}
    {%- block html_head_js_jquery -%}
        <script>{{ include_template("nbconvert_tempaltes/static/jquery.min.js") }}</script>
    {%- endblock html_head_js_jquery -%}

    {%- block html_head_js_requirejs -%}
        <script>{{ include_template("nbconvert_tempaltes/static/require.min.js") }}</script>
    {%- endblock html_head_js_requirejs -%}

    {%- block html_head_js_embed_amd -%}
        <script>{{ include_template("nbconvert_tempaltes/static/embed-amd.js") }}</script>
    {%- endblock html_head_js_embed_amd -%}

{%- endblock html_head_js -%}


