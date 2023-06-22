from decimal import Decimal

import attrs
from rich.console import Console
from rich.table import Table

from src.schemas.errors import Error


def pink(c):
    return f"[bold bright_magenta]{c}[/]"


def blue(c):
    return f"[bold bright_cyan]{c}[/]"


def yellow(c):
    return f"[bold bright_yellow]{c}[/]"


def report_result(result, HappyClass=None):
    """
    Prints out different tables based on the result.
    """
    console = Console()
    match result:
        case Error():
            console.print(attrs_to_rich_table(Error, [result]))
        case _:
            if HappyClass:
                console.print(attrs_to_rich_table(HappyClass, [result]))
            else:
                console.print("No `HappyClass` supplied!")


def attrs_to_rich_table(row_type, rows):
    fields = attrs.fields(row_type)  # type: ignore

    table = Table(title=f"{row_type.__name__}")
    for field in fields:
        formatting = field.metadata["print"] if "print" in field.metadata else dict()
        table.add_column(
            field.metadata["alias"] if "alias" in field.metadata else field.name,
            justify="right" if field.type in [int, float, Decimal] else "left",
            **formatting,
        )

    for row in rows:
        row_items = []
        for field, value in attrs.asdict(row, recurse=False).items():
            if attrs.has(value):
                value = attrs_to_rich_table(value.__class__, [value])
            else:
                value = str(value)
            row_items.append(value)
        table.add_row(*row_items)
    return table
