"""Main endpoint for the fools project."""

import typer

import fools.finance.commands as finance_commands

app = typer.Typer()

app.add_typer(finance_commands.app, name="finance")


if __name__ == "__main__":
    app()
