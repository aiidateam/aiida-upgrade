"""Main entry-point for CLI."""
import sys
from pathlib import Path

import click

from .migrate import migrate_path


@click.command(context_settings={"help_option_names": ["--help"]})
@click.argument("path", type=click.Path(exists=True))
def main(path):
    """The command line interface of aiida-upgrade."""

    migrate_path(Path(path))


if __name__ == "__main__":
    sys.exit(main())
