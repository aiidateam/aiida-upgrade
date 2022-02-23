"""Main entry-point for CLI."""
import sys

import click


@click.command(context_settings={"help_option_names": ["--help"]})
def main():
    """The command line interface of aiida-upgrade."""


if __name__ == "__main__":
    sys.exit(main())
