"""Export a simulation run as JSON for the observer viewer:  python -m civ.cli.export_viz --days 14 --seed 1 --out run.json"""
import argparse
import json

from civ.core.clock import DAY, MINUTE
from civ.core.engine import START_TIME, Engine

STATES = ["sleep", "eat", "buy", "work", "socialize", "forage", "idle", "travel"]
SAMPLE_EVERY = 10 * MINUTE


def position(eng: Engine, a, t: float) -> tuple[float, float, int]:
    locs = eng.world.locations
    if a.state == "travel" and a.step:
        f, to = locs[a.step.meta["from"]], locs[a.step.meta["to"]]
        k = min(1.0, max(0.0, (t - a.step_started) / a.step.duration))
        return f.x + (to.x - f.x) * k, f.y + (to.y - f.y) * k, list(locs).index(a.step.meta["to"])
    loc = a.location if a.location in locs else a.home
    return locs[loc].x, locs[loc].y, -1


def export(seed: int, days: float) -> dict:
    eng = Engine(seed=seed)
    loc_ids = list(eng.world.locations)
    agents = sorted(eng.agents.values(), key=lambda a: a.id)
    samples, t = [], START_TIME
    end = START_TIME + days * DAY
    while t <= end:
        eng.run_until(t)
        row = [round(t - START_TIME, 1)]
        for a in agents:
            x, y, dest = position(eng, a, t)
            row += [round(x, 2), round(y, 2), STATES.index(a.state if a.state in STATES else "idle"), dest,
                    round(a.needs.value("hunger", t), 1), round(a.needs.value("energy", t), 1),
                    round(a.needs.value("social", t), 1), eng.ledger.balance(a.account), a.pantry]
        samples.append(row)
        t += SAMPLE_EVERY
    events = []
    for ev in eng.log.query(types=("conversation", "wage", "purchase", "activity")):
        if ev.time > end:
            break
        loc = loc_ids.index(ev.location) if ev.location in loc_ids else -1
        p = ev.payload
        if ev.type == "conversation":
            events.append([round(ev.time - START_TIME, 1), "conversation", list(ev.actors), loc, [p["topic"], p["affinity"], p["familiarity"]]])
        elif ev.type == "wage":
            events.append([round(ev.time - START_TIME, 1), "wage", list(ev.actors), loc, p["amount"]])
        elif ev.type == "purchase":
            events.append([round(ev.time - START_TIME, 1), "purchase", list(ev.actors), loc, p["qty"]])
        elif p.get("kind") in ("eat", "sleep", "work", "forage"):
            events.append([round(ev.time - START_TIME, 1), "activity", list(ev.actors), loc, p["kind"]])
    return {
        "seed": seed, "days": days, "start_hour": START_TIME / 3600, "step": SAMPLE_EVERY,
        "states": STATES,
        "locations": [{"id": k, "name": v.name, "kind": v.kind, "x": v.x, "y": v.y} for k, v in eng.world.locations.items()],
        "agents": [{"id": a.id, "name": a.name, "sex": a.sex} for a in agents],
        "samples": samples, "events": events,
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
    print(f"{len(data['samples'])} samples, {len(data['events'])} events -> {args.out}")
