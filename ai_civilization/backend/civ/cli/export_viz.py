"""Export a simulation run as JSON for the observer viewer:  python -m civ.cli.export_viz --days 14 --seed 1 --out run.json"""
import argparse
import json

from civ.core.clock import DAY, MINUTE
from civ.core.engine import START_TIME, Engine

KINDS = ["sleep", "eat", "buy", "work", "socialize", "forage", "idle", "travel"]
SAMPLE_EVERY = 10 * MINUTE


def export(seed: int, days: float) -> dict:
    eng = Engine(seed=seed)
    loc_ids = list(eng.world.locations)
    agents = sorted(eng.agents.values(), key=lambda a: a.id)
    end = START_TIME + days * DAY
    needs, t = [], START_TIME
    while t <= end:
        eng.run_until(t)
        row = [round(t - START_TIME, 1)]
        for a in agents:
            row += [round(a.needs.value("hunger", t), 1), round(a.needs.value("energy", t), 1),
                    round(a.needs.value("social", t), 1), eng.ledger.balance(a.account), a.pantry]
        needs.append(row)
        t += SAMPLE_EVERY

    rel = lambda x: round(x - START_TIME, 1)
    timeline, events = {a.id: [] for a in agents}, []
    for ev in eng.log.query(types=("activity", "travel", "conversation", "wage", "purchase")):
        if ev.time > end:
            break
        loc = loc_ids.index(ev.location) if ev.location in loc_ids else -1
        p = ev.payload
        if ev.type == "travel":
            timeline[ev.actors[0]].append([rel(p["start"]), rel(ev.time), KINDS.index("travel"), loc_ids.index(p["from"]), loc])
        elif ev.type == "activity":
            timeline[ev.actors[0]].append([rel(p["start"]), rel(ev.time), KINDS.index(p["kind"]), loc, loc])
            if p["kind"] in ("eat", "sleep", "work", "forage"):
                events.append([rel(ev.time), "activity", list(ev.actors), loc, p["kind"]])
        elif ev.type == "conversation":
            events.append([rel(ev.time), "conversation", list(ev.actors), loc, [p["topic"], p["affinity"], p["familiarity"]]])
        elif ev.type == "wage":
            events.append([rel(ev.time), "wage", list(ev.actors), loc, p["amount"]])
        elif ev.type == "purchase":
            events.append([rel(ev.time), "purchase", list(ev.actors), loc, p["qty"]])
    for a in agents:
        timeline[a.id].sort(key=lambda s: s[0])
    return {
        "seed": seed, "days": days, "start_hour": START_TIME / 3600, "step": SAMPLE_EVERY, "kinds": KINDS,
        "locations": loc_ids,
        "agents": [{"id": a.id, "name": a.name, "sex": a.sex} for a in agents],
        "timeline": [timeline[a.id] for a in agents], "needs": needs, "events": events,
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=float, default=14)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--out", default="run.json")
    args = p.parse_args()
    data = export(args.seed, args.days)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(data['needs'])} samples, {sum(map(len, data['timeline']))} segments, {len(data['events'])} events -> {args.out}")
