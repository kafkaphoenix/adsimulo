from dataclasses import dataclass


@dataclass
class Star:
    name: str = "Aurora"
    symbol: str = "☉"
    age: int = 0
