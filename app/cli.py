import typer
from rich import print
from app.geo.geocoder import Coders
from app.geo.maxmind import MaxMind
import validators
from app.geo.models import GeoInfo


cli = typer.Typer()


@cli.command()
def ip(
    query: str,
    coder: Coders = typer.Option(default=Coders.HERE)
):
    try:
        assert validators.ip_address.ipv4(query)
        res = MaxMind.lookup(query)
        if res.location:
            coder_res = coder.coder.from_gps(*res.location)
            res = GeoInfo(**{**res.model_dump(), **coder_res.model_dump()})
        print(res.model_dump())
    except AssertionError:
        raise RuntimeError


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
