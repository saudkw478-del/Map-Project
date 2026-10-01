"""L1 decision layer: pure code, personality-weighted utility. No LLM involved."""
from civ.agents.agent import Agent, Step
from civ.core.clock import HOUR, MINUTE, day_index, hour_of_day

FOOD_PRICE, PASTRY_PRICE, COFFEE_PRICE, GIFT_PRICE = 5, 6, 8, 5
EAT_RESTORE = 60.0
CHATTY = ("socialize", "coffee")


def urgency(v: float) -> float:
    return ((100.0 - v) / 100.0) ** 2


def score_options(agent: Agent, eng, t: float) -> dict[str, float]:
    h, day = hour_of_day(t), day_index(t)
    v = {n: agent.needs.value(n, t) for n in agent.needs.values}
    money = eng.ledger.balance(agent.account)
    tr = agent.traits
    s: dict[str, float] = {}

    night = (h >= 22 or h < agent.wake_hour) and v["energy"] < 99
    s["sleep"] = urgency(v["energy"]) + (0.5 if night else 0.0)

    if agent.pantry > 0 and v["hunger"] < 60:
        s["eat"] = urgency(v["hunger"]) * 1.3
    if money >= FOOD_PRICE and (agent.pantry == 0 or (agent.pantry < 2 and money >= 3 * FOOD_PRICE)):
        s["buy"] = max(urgency(v["hunger"]) if agent.pantry == 0 else 0.0, 0.3 if agent.pantry == 0 else 0.12)
    if v["hunger"] < 55 and money >= PASTRY_PRICE and 6 <= h < 20:
        s["pastry"] = urgency(v["hunger"]) * (0.5 + tr["sweet"]) * 0.9
    if agent.pantry == 0 and money < FOOD_PRICE:
        s["forage"] = 0.2 + urgency(v["hunger"]) * 0.8

    if agent.shift_start <= h < agent.shift_start + 2 and agent.last_work_day != day:
        s["work"] = 0.8 * (0.5 + tr["diligence"])

    if 7 <= h < 22 and eng.other_alive(agent):
        s["socialize"] = urgency(v["social"]) * (0.3 + tr["sociability"])
    if 7 <= h < 21 and money >= COFFEE_PRICE and eng.other_alive(agent):
        s["coffee"] = (urgency(v["social"]) * 0.6 + urgency(v["fun"]) * 0.5) * (0.3 + tr["sociability"]) * (1.2 - 0.6 * tr["thrift"])
    if 9 <= h < 19:
        s["read"] = urgency(v["fun"]) * (0.3 + tr["curiosity"]) * 1.1
    if 9 <= h < 20 and money >= GIFT_PRICE and tr["thrift"] < 0.8:
        s["browse"] = urgency(v["fun"]) * 0.95 * (0.3 + (1 - tr["thrift"]))
    if 7 <= h < 21:
        s["stroll"] = 0.06 + urgency(v["fun"]) * 0.25

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

    def at(dest: str, kind: str, dur: float) -> list[Step]:
        return go(dest) + [Step(kind, dest, dur)]

    if choice == "sleep":
        h = hour_of_day(t)
        if h >= 22 or h < agent.wake_hour:  # night sleep: until the personal wake-up hour
            hours = (agent.wake_hour + 24 - h) % 24 if h >= 22 else agent.wake_hour - h
            hours = max(1.0, min(10.0, hours))
        else:  # nap
            hours = max(1.0, min(4.0, (100.0 - agent.needs.value("energy", t)) / 12.5))
        return at(agent.home, "sleep", hours * HOUR)
    if choice == "eat":
        return at(agent.home, "eat", 30 * MINUTE)
    if choice == "buy":
        return at("market", "buy", 15 * MINUTE)
    if choice == "pastry":
        return at("bakery", "pastry", 20 * MINUTE)
    if choice == "forage":
        return at("park", "forage", 1 * HOUR)
    if choice == "work":
        return at(agent.workplace, "work", 8 * HOUR)
    if choice == "socialize":
        return at("park", "socialize", 1 * HOUR)
    if choice == "coffee":
        return at("cafe", "coffee", 50 * MINUTE)
    if choice == "read":
        return at("library", "read", 90 * MINUTE)
    if choice == "browse":
        return at("gift", "browse", 30 * MINUTE)
    if choice == "stroll":
        return at("park", "stroll", 40 * MINUTE)
    return [Step("idle", agent.location, 30 * MINUTE)]


def decide(agent: Agent, eng, t: float) -> tuple[str, dict[str, float], list[Step]]:
    scores = score_options(agent, eng, t)
    choice = max(sorted(scores), key=lambda k: scores[k])
    return choice, scores, plan_for(agent, choice, eng, t)
