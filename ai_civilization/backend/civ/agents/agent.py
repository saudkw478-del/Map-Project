from dataclasses import dataclass, field

from civ.agents.needs import Needs
from civ.core.rng import RNG


@dataclass
class Step:
    kind: str
    location: str | None
    duration: float
    meta: dict = field(default_factory=dict)


@dataclass
class Agent:
    id: int
    name: str
    sex: str
    birth_time: float
    home: str
    workplace: str
    traits: dict
    needs: Needs
    rng: RNG
    location: str
    shift_start: int = 9
    wake_hour: int = 6
    pantry: int = 0
    health: float = 100.0
    alive: bool = True
    state: str = "idle"
    step: Step | None = None
    step_started: float = 0.0
    plan: list = field(default_factory=list)
    token: int = 0               # invalidates stale scheduled step-ends
    last_work_day: int = -1
    talked_this_step: bool = False

    @property
    def account(self) -> str:
        return f"agent:{self.id}"
