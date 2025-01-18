from enum import Enum
from typing import Any


class LabeledEnum(Enum):
    """ Enum の基底クラス"""
    def __init__(self, value: Any, label: str):
        self._value = value
        self._label = label

    @property
    def value(self):
        return self._value

    @property
    def label(self):
        return self._label

    @classmethod
    def value_of(cls, value: str):
        for enum_member in cls:
            if enum_member.value == value:
                return enum_member
        return None
