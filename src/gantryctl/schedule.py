"""Berth-window scheduling across a gantry fleet."""

from dataclasses import dataclass, field


@dataclass
class Move:
    container: str
    gantry: str
    minutes: int


@dataclass
class Berth:
    name: str
    moves: list[Move] = field(default_factory=list)

    def add(self, move: Move) -> None:
        self.moves.append(move)

    def gantry_minutes(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for m in self.moves:
            out[m.gantry] = out.get(m.gantry, 0) + m.minutes
        return out

    def critical_path_minutes(self) -> int:
        """The berth is done when its busiest gantry is done."""
        load = self.gantry_minutes()
        return max(load.values()) if load else 0

    def balance_score(self) -> float:
        """0.0 = perfectly balanced, 1.0 = everything on one gantry."""
        load = self.gantry_minutes()
        if len(load) < 2:
            return 1.0 if load else 0.0
        total = sum(load.values())
        peak = max(load.values())
        ideal = total / len(load)
        return round((peak - ideal) / (total - ideal), 4)
