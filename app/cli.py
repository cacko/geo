import typer
from rich import print
from app.geo.geocoder import Coders


cli = typer.Typer()


@cli.command()
def address(
    query: list[str],
    coder: Coders = typer.Option(default=Coders.HERE)
):
    try:
        res = coder.coder.from_name(" ".join(query)).model_dump()
        print(res)
    except AssertionError:
        raise RuntimeError


@cli.command(context_settings=dict(
    ignore_unknown_options=True,
))
def gps(
    query: tuple[float, float],
    coder: Coders = typer.Option(default=Coders.HERE)
):
    try:
        res = coder.coder.from_gps(*query).model_dump()
        print(res)
    except AssertionError:
        raise RuntimeError


def run():
    cli()
