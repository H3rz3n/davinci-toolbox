from __future__ import annotations

import argparse
import sys
from importlib.metadata import PackageNotFoundError, version


def get_version() -> str:
    try:
        return version("davinci-helper")
    except PackageNotFoundError:
        return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(prog="davinci-helper")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}",
    )
    parser.parse_args()

    # Import GTK only after argument parsing,
    # so --version can exit cleanly in headless environments.
    from davinci_helper.main import main as app_main

    return app_main()


if __name__ == "__main__": 
    raise SystemExit(main())