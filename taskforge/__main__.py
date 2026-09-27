"""Allow ``python -m taskforge`` execution."""

from .cli import main


if __name__ == "__main__":
    # TODO: Add a profiling switch for slow command investigations.
    raise SystemExit(main())
