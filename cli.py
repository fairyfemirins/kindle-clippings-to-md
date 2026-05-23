"""
CLI for Kindle Clippings to Markdown.
Usage: python cli.py convert <input_file> [--output <output_file>]
"""

import click
from kindle_parser import parse_clippings

@click.group()
def cli():
    """Kindle Clippings to Markdown CLI."""
    pass

@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), default="highlights.md")
def convert(input_file, output):
    """Convert Kindle clippings to Markdown."""
    parse_clippings(input_file, output)
    click.echo(f"Highlights saved to {output}")

if __name__ == "__main__":
    cli()