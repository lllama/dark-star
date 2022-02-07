import click


@click.group("cli")
@click.pass_context
def cli(ctx):
    """Dark Star - a web framework based on Starlette"""
    pass


@cli.command("create-app")
def create_app():
    print("Creating app")


@cli.command("new-route")
def new_route():
    print("Adding new route")


def main():
    cli(prog_name="cli")
