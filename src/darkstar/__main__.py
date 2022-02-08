import click
from pathlib import Path
from starlette.routing import compile_path


@click.group("cli")
@click.pass_context
def cli(ctx):
    """Dark Star - a web framework based on Starlette"""
    pass


@cli.command("create-app")
@click.argument("directory", type=click.Path())
def create_app(directory):
    path = Path(directory)

    routes_dir = path / "routes"
    print(f"Creating {routes_dir}")
    routes_dir.mkdir(exist_ok=True, parents=True)

    static_dir = path / "static"
    print(f"Creating {static_dir}")
    static_dir.mkdir(exist_ok=True, parents=True)

    index_path = path / "routes" / "index.html"
    if not index_path.exists():
        print(f"Creating {index_path}")
        index_path.write_text(
            """\
<html>
  <head>
  <title>Dark Star</title>
  </head>
  <body>
    {% block content %}
    {% endblock content %}
  </body>
</html>
"""
        )
    app_file = path / "app.py"
    if not app_file.exists():
        print(f"Creating {app_file}")
        app_file.write_text(
            """\
from darkstar.applications import DarkStar

app = DarkStar()
"""
        )


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
        route_path.write_text(
            f'''\
{param_text}
"""
{{% extends 'index.html' %}}
{{% block content %}}
{{% endblock %}}
"""
'''
        )


def main():
    cli(prog_name="cli")


if __name__ == "__main__":
    main()
