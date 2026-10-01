"""L1 decision layer: pure code, personality-weighted utility. No LLM involved."""
from civ.agents.agent import Agent, Step
from civ.core.clock import HOUR, MINUTE, day_index, hour_of_day

FOOD_PRICE = 5
EAT_RESTORE = 60.0


def urgency(v: float) -> float:
    return ((100.0 - v) / 100.0) ** 2


def score_options(agent: Agent, eng, t: float) -> dict[str, float]:
    h = hour_of_day(t)
    day = day_index(t)
    v = {n: agent.needs.value(n, t) for n in agent.needs.values}
    money = eng.ledger.balance(agent.account)
    s: dict[str, float] = {}

    night = (h >= 22 or h < agent.wake_hour) and v["energy"] < 99
    s["sleep"] = urgency(v["energy"]) + (0.5 if night else 0.0)

    if agent.pantry > 0 and v["hunger"] < 60:
        s["eat"] = urgency(v["hunger"]) * 1.3
    if money >= FOOD_PRICE and (agent.pantry == 0 or (agent.pantry < 2 and money >= 3 * FOOD_PRICE)):
        s["buy"] = max(urgency(v["hunger"]) if agent.pantry == 0 else 0.0, 0.3 if agent.pantry == 0 else 0.12)
    if agent.pantry == 0 and money < FOOD_PRICE:
        s["forage"] = 0.2 + urgency(v["hunger"]) * 0.8

    in_window = agent.shift_start <= h < agent.shift_start + 2
    if in_window and agent.last_work_day != day:
        s["work"] = 0.8 * (0.5 + agent.traits["diligence"])

    if eng.other_alive(agent) and 7 <= h < 22:
        s["socialize"] = urgency(v["social"]) * (0.3 + agent.traits["sociability"])

    s["idle"] = 0.05
    for k in s:
        s[k] += agent.rng.uniform(0.0, 0.02)  # deterministic tie-breaking noise
    return s


def plan_for(agent: Agent, choice: str, eng, t: float) -> list[Step]:
    w = eng.world

    def go(dest: str) -> list[Step]:
        if agent.location == dest:
            return []
        return [Step("travel", None, w.travel_time(agent.location, dest), {"to": dest, "from": agent.location})]

    v = agent.needs.value("energy", t)
    if choice == "sleep":
        h = hour_of_day(t)
        if h >= 22 or h < agent.wake_hour:  # night sleep: until the personal wake-up hour
            hours = (agent.wake_hour + 24 - h) % 24 if h >= 22 else agent.wake_hour - h
            hours = max(1.0, min(10.0, hours))
        else:  # nap: until energy is restored
            hours = max(1.0, min(4.0, (100.0 - v) / 12.5))
        return go(agent.home) + [Step("sleep", agent.home, hours * HOUR)]
    if choice == "eat":
        return go(agent.home) + [Step("eat", agent.home, 30 * MINUTE)]
    if choice == "buy":
        return go("market") + [Step("buy", "market", 15 * MINUTE)]
    if choice == "forage":
        return go("meadow") + [Step("forage", "meadow", 1 * HOUR)]
    if choice == "work":
        return go(agent.workplace) + [Step("work", agent.workplace, 8 * HOUR)]
    if choice == "socialize":
        return go("park") + [Step("socialize", "park", 1 * HOUR)]
    return [Step("idle", agent.location, 30 * MINUTE)]


def decide(agent: Agent, eng, t: float) -> tuple[str, dict[str, float], list[Step]]:
    scores = score_options(agent, eng, t)
    choice = max(sorted(scores), key=lambda k: scores[k])
    return choice, scores, plan_for(agent, choice, eng, t)
