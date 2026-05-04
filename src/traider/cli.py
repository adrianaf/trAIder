"""Command-line entrypoint for trAIder."""

from traider import __version__


def main() -> None:
    print(f"trAIder {__version__}")
