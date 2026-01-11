from decimal import Decimal
from typing import Literal

from fluent_compiler.types import FluentType
from typing_extensions import TypeAlias

PossibleValue: TypeAlias = str | int | float | Decimal | bool | FluentType

class TranslatorRunner:
    def get(self, path: str, **kwargs: PossibleValue) -> str: ...
    button: Button

    @staticmethod
    def start() -> Literal["""&lt;b&gt;👋 Привет!&lt;/b&gt;"""]: ...

class Button:
    @staticmethod
    def description() -> Literal["""📔 Узнать об обучении"""]: ...
    @staticmethod
    def guides() -> Literal["""🆓 Бесплатные инструкции"""]: ...
    @staticmethod
    def subscribe() -> Literal["""💲 Подписаться"""]: ...
