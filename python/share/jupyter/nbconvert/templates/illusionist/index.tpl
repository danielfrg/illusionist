{%- extends "full.tpl" -%}

{%- block ipywidgets -%}
{%- if "widgets" in nb.metadata -%}
<link rel="stylesheet" href="https://unpkg.com/font-awesome@4.7.0/css/font-awesome.min.css" type="text/css" />
{%- endif -%}
{%- endblock ipywidgets -%}

{%- block footer %}

{%- if "widgets" in nb.metadata %}

  {%- set mimetype = 'application/vnd.jupyter.widget-state+json'-%}
  {%- if mimetype in nb.metadata.get("widgets", {}) %}
  <script type="{{ mimetype }}">
  {{ nb.metadata.widgets[mimetype] | json_dumps }}
  </script>
  {%- endif -%}

  {%- set mimetype = "application/vnd.illusionist.widget-onchange+json" -%}
  {%- if mimetype in nb.metadata.get("widgets", {}) %}
  <script type="{{ mimetype }}">
  {{ nb.metadata.widgets[mimetype] | json_dumps }}
  </script>
  {%- endif %}

  {%- if resources.illusionist_devmode %}
  <script src="./static/dist/illusionist.js"></script>
  {%- else -%}
  <script>{{ include_template("./static/dist/illusionist.js") }}</script>
  <script>
      let widgetManager;

      async function init() {
          widgetManager = new IllusionistWidgetManager();
          await widgetManager.loadState();
          await widgetManager.renderAllWidgets();
      }

      if (document.readyState === "complete") {
          init();
      } else {
          window.addEventListener("load", init);
      }
  </script>
  {%- endif %}

{%- endif %}

</html>
{%- endblock footer-%}
