"""Simulation time. Unit = simulated second."""
MINUTE = 60
HOUR = 3600
DAY = 86400
YEAR_DAYS = 365


def day_index(t: float) -> int:
    return int(t // DAY)


def hour_of_day(t: float) -> float:
    return (t % DAY) / HOUR


def fmt(t: float) -> str:
    d = day_index(t)
    return f"Y{d // YEAR_DAYS + 1} D{d % YEAR_DAYS + 1:03d} {int(hour_of_day(t)):02d}:{int((t % HOUR) // MINUTE):02d}"


class SimClock:
    def __init__(self, start: float = 0.0):
        self.now = float(start)

    def set(self, t: float) -> None:
        if t < self.now:
            raise ValueError(f"time went backwards: {t} < {self.now}")
        self.now = float(t)
