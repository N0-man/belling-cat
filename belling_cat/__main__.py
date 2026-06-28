"""Entry point for running Belling Cat as a module."""

import sys

from belling_cat.cli import run_app


def main() -> None:
    """Main entry point for the application."""
    # Check for --version flag
    if "--version" in sys.argv:
        print("Belling Cat v0.1.0")
        sys.exit(0)

    # Run the application
    try:
        run_app()
    except KeyboardInterrupt:
        print("\nExiting Belling Cat...")
        sys.exit(0)


if __name__ == "__main__":
    main()
