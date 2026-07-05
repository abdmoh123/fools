"""Main endpoint for the fools project."""

import typer

app = typer.Typer()


@app.command()
def main(name: str) -> None:
    """Main command.

    Args:
        name: The name to say hello to.
    """
    print(f"Hello, {name}")


if __name__ == "__main__":
    app()
