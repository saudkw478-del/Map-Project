"""Lazy needs: values are computed from (value0, rate, t0) on demand, never ticked per frame.
Scale 0..100 where 100 = fully satisfied."""
from civ.core.clock import HOUR

NEED_NAMES = ("hunger", "energy", "social")

# per simulated hour, by activity
DEFAULT_RATES = {"hunger": -4.0, "energy": -5.0, "social": -2.0}
ACTIVITY_RATES = {
    "sleep": {"hunger": -2.0, "energy": +12.5, "social": -1.0},
    "work": {"hunger": -4.5, "energy": -6.0, "social": -2.0},
    "travel": {"hunger": -4.0, "energy": -5.5, "social": -2.0},
}


def clamp(v: float) -> float:
    return max(0.0, min(100.0, v))


class Needs:
    def __init__(self, values: dict[str, float], t0: float):
        self.values = dict(values)
        self.rates = dict(DEFAULT_RATES)
        self.t0 = t0

    def value(self, name: str, t: float) -> float:
        return clamp(self.values[name] + self.rates[name] * (t - self.t0) / HOUR)

    def settle(self, t: float) -> None:
        for n in NEED_NAMES:
            self.values[n] = self.value(n, t)
        self.t0 = t

    def add(self, name: str, delta: float) -> None:
        self.values[name] = clamp(self.values[name] + delta)

    def set_activity(self, kind: str) -> None:
        self.rates = dict(ACTIVITY_RATES.get(kind, DEFAULT_RATES))

    def time_to(self, name: str, threshold: float, t: float) -> float | None:
        """Seconds until `name` crosses `threshold` at the current rate (None if never)."""
        v, r = self.value(name, t), self.rates[name]
        if r == 0 or (v - threshold) * r > 0:
            return None
        return abs((threshold - v) / r) * HOUR
