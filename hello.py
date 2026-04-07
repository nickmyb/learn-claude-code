"""A simple Hello, World! module."""


def greet(name: str = "World") -> str:
    """Return a greeting string for the given name.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        A greeting string in the format "Hello, <name>!".
    """
    return f"Hello, {name}!"


def main() -> None:
    """Entry point: print a greeting to standard output."""
    print(greet())


if __name__ == "__main__":
    main()
