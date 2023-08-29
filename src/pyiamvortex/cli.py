import typer
from pyiamvortex.vortex import Vortex
import json

main = typer.Typer()


@main.command()
def get_aws_actions(aws_service: str = typer.Argument(None)):
    vortex: Vortex = Vortex()
    aws_actions: list[str] = vortex.get_aws_actions(aws_service=aws_service)
    typer.echo(json.dumps(aws_actions, indent=4))


@main.command()
def get_aws_services():
    vortex: Vortex = Vortex()
    aws_services: list[str] = vortex.get_aws_services()
    typer.echo(json.dumps(aws_services, indent=4))


@main.command()
def expand_aws_wildcard(aws_wildcard: str):
    vortex: Vortex = Vortex()
    aws_actions_expanded: list[str] = vortex.expand_aws_wildcard(
        aws_action=aws_wildcard
    )
    typer.echo(json.dumps(aws_actions_expanded, indent=4))


if __name__ == "__main__":
    main()
