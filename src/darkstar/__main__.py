from pathlib import Path

import click
from jinja2 import Template
from starlette.routing import compile_path

APP_TEMPLATE = """\
from darkstar.applications import DarkStar

app = DarkStar()
"""

INDEX_TEMPLATE = '''
"""
<html data-theme="dark">
  <head>
    <title>Dark Star</title>
    {%- if htmx %}
    <script src="https://unpkg.com/htmx.org@latest"></script>
    <script src="https://unpkg.com/hyperscript.org@latest"></script>{% endif %}
    <link rel="stylesheet" href="https://classless.de/classless.css">
    <link rel="stylesheet" href="https://classless.de/addons/themes.css">
  </head>
  <body>
  {%- raw %}
    {% block content %}
    <h1>Welcome to Dark Star</h1>
    <p>Use the <code>new-route</code> command to create your first route</p>
    <p>See <a href="https://lllama.github.io/dark-star">the docs</a> for more information.</p>
    {% endblock %}
  {% endraw -%}
  </body>
</html>
"""
'''

TEMPLATE_TEMPLATE = '''\
{{param_text}}
"""
{% raw %}
{% extends 'index.py' %}
{% block content %}
{% endblock %}
{% endraw %}
"""
'''


@click.group("cli")
@click.pass_context
def cli(ctx):
    """Dark Star - a web framework based on Starlette"""
    pass


@cli.command("create-app")
@click.argument("directory", type=click.Path())
@click.option("--htmx/--no-htmx", help="Include htmx script in index.py", default=False)
def create_app(directory, htmx):
    path = Path(directory)

    routes_dir = path / "routes"
    print(f"Creating {routes_dir}")
    routes_dir.mkdir(exist_ok=True, parents=True)

    static_dir = path / "static"
    print(f"Creating {static_dir}")
    static_dir.mkdir(exist_ok=True, parents=True)

    index_path = path / "routes" / "index.py"
    if not index_path.exists():
        print(f"Creating {index_path}")
        index_path.write_text(Template(INDEX_TEMPLATE).render(htmx=htmx))
    app_file = path / "app.py"
    if not app_file.exists():
        print(f"Creating {app_file}")
        app_file.write_text(Template(APP_TEMPLATE).render())


@cli.command("new-route")
@click.argument("path", type=click.Path())
def new_route(path):

    route_path = Path("routes") / path.lstrip("/").rstrip("/")
    route_path = route_path.with_suffix(".py")
    if not route_path.exists():
        print(f"Adding new route {route_path}")
        route_path.parent.mkdir(parents=True, exist_ok=True)
        *_, params = compile_path(str(route_path))
        param_text = "\n".join(
            f'{key} = request.path_params["{key}"]' for key in params.keys()
        ).strip()
        route_path.write_text(Template(TEMPLATE_TEMPLATE).render(param_text=param_text))


def main():
    cli(prog_name="cli")


if __name__ == "__main__":
    main()
