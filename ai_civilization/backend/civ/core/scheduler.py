"""Discrete-event priority queue. Ties are broken by insertion order => deterministic."""
import heapq
from dataclasses import dataclass, field


@dataclass(order=True)
class Item:
    time: float
    seq: int
    kind: str = field(compare=False)
    data: dict = field(compare=False, default_factory=dict)


class Scheduler:
    def __init__(self):
        self._heap: list[Item] = []
        self._seq = 0

    def push(self, time: float, kind: str, data: dict | None = None) -> None:
        self._seq += 1
        heapq.heappush(self._heap, Item(time, self._seq, kind, data or {}))

    def peek_time(self) -> float | None:
        return self._heap[0].time if self._heap else None

    def pop(self) -> Item:
        return heapq.heappop(self._heap)

    def __len__(self) -> int:
        return len(self._heap)
