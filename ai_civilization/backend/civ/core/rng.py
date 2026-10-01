"""Seeded, named RNG streams so every subsystem is deterministic and independent."""
import hashlib
import random


class RNG:
    def __init__(self, seed: int, stream: str = "root"):
        digest = hashlib.sha256(f"{seed}:{stream}".encode()).digest()
        self._r = random.Random(int.from_bytes(digest[:8], "big"))
        self.seed = seed
        self.stream = stream

    def child(self, name: str) -> "RNG":
        return RNG(self.seed, f"{self.stream}/{name}")

    def random(self) -> float:
        return self._r.random()

    def uniform(self, a: float, b: float) -> float:
        return self._r.uniform(a, b)

    def choice(self, seq):
        return seq[self._r.randrange(len(seq))]

    def chance(self, p: float) -> bool:
        return self._r.random() < p

    def gauss(self, mu: float, sigma: float) -> float:
        return self._r.gauss(mu, sigma)
