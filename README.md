# Fools

A collection of fun tools.

## Setup

You will need uv to set up the project. You can install it manually or use mise
to automatically set things up via `mise install`.

After installing uv, run `uv sync --frozen` to install the required dependencies.

## Tooling

Mypy is used to enforce strict type checking (reduce chances of bugs).

Testing is done using pytest, and linting with ruff, basedpyright and mypy.

## Structure

The main endpoint file imports all commands from other modules into a
centralised location so all the commands can be run from one built executable.

### Finance

There is a finance module that includes all finance-related tools such as
compounding investment and debt calculators. These functions can be found in
the calculator file.
This module also contains a commands file that contains all the CLI commands.
