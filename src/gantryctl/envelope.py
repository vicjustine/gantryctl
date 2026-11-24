"""Load-envelope checks for ship-to-shore gantry cranes.

A gantry's safe working load falls off as the trolley moves outboard.
The envelope is a piecewise-linear derate curve keyed on outreach.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Gantry:
    name: str
    max_swl_t: float
    max_outreach_m: float
    derate_start_m: float
    derate_per_m: float

    def swl_at(self, outreach_m: float) -> float:
        """Safe working load in tonnes at a given outreach."""
        if outreach_m < 0:
            raise ValueError("outreach cannot be negative")
        if outreach_m > self.max_outreach_m:
            raise ValueError(
                f"{outreach_m}m exceeds {self.name} max outreach "
                f"{self.max_outreach_m}m"
            )
        if outreach_m <= self.derate_start_m:
            return self.max_swl_t
        over = outreach_m - self.derate_start_m
        return round(self.max_swl_t - over * self.derate_per_m, 2)


FLEET = {
    "panamax": Gantry("panamax", 40.0, 38.0, 24.0, 0.45),
    "postpanamax": Gantry("postpanamax", 65.0, 52.0, 32.0, 0.60),
    "neopanamax": Gantry("neopanamax", 80.0, 65.0, 40.0, 0.75),
}


def check_lift(gantry: str, outreach_m: float, load_t: float) -> dict:
    """Return a verdict dict for one planned lift."""
    if gantry not in FLEET:
        raise KeyError(f"unknown gantry {gantry!r}")
    g = FLEET[gantry]
    swl = g.swl_at(outreach_m)
    margin = round(swl - load_t, 2)
    return {
        "gantry": gantry,
        "outreach_m": outreach_m,
        "load_t": load_t,
        "swl_t": swl,
        "margin_t": margin,
        "safe": margin >= 0,
    }
