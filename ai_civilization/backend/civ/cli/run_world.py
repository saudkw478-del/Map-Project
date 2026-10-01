"""Run the world headless:  python -m civ.cli.run_world --days 30 --seed 1 [--timeline 1 --day 3]"""
import argparse
import json
from collections import Counter

from civ.core.clock import DAY, fmt
from civ.core.engine import START_TIME, Engine


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=float, default=30)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--db", default=":memory:")
    p.add_argument("--timeline", type=int, help="agent id to print a day-timeline for")
    p.add_argument("--day", type=int, default=2)
    args = p.parse_args()

    eng = Engine(seed=args.seed, db=args.db)
    eng.run_days(args.days)
    s = eng.summary()
    counts = Counter(e.type for e in eng.log.query())
    print(json.dumps({"summary": s, "event_counts": dict(counts)}, ensure_ascii=False, indent=2))

    if args.timeline:
        d0 = START_TIME // DAY * DAY + args.day * DAY
        print(f"\n--- Timeline of agent {args.timeline}, day {args.day} ---")
        for e in eng.log.query(actor=args.timeline, since=d0, until=d0 + DAY, types=("activity", "travel", "conversation", "purchase", "wage", "death")):
            detail = e.payload.get("kind") or e.payload.get("topic") or e.payload.get("item") or ""
            print(f"{fmt(e.time)}  {e.type:<12} {detail:<10} @ {e.location}")


if __name__ == "__main__":
    main()
