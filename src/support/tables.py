from typing import TypeVar, Type, Iterable, Any
from decimal import Decimal
import attrs
from rich.table import Table

from src.schemas.errors import Error

X = TypeVar("X")


def report_result(result, HappyClass: Any, console):
    """
    Prints out different tables based on the result.
    """
    match result:
        case Error():
            console.print(attrs_to_rich_table(Error, [result]))
        case HappyClass():
            console.print(attrs_to_rich_table(HappyClass, [result]))


def attrs_to_rich_table(row_type: Type[X], rows: Iterable[X]) -> Table:
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
        table.add_row(*(str(item) for item in attrs.astuple(row)))

    return table
