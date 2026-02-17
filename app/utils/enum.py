from typing import Type
from enum import Enum

def enum_values(enum_cls: Type[Enum]) -> list[str]:
    return [e.value for e in enum_cls]