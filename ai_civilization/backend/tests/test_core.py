from civ.agents.needs import Needs
from civ.core.clock import DAY, HOUR
from civ.core.engine import START_TIME, TREASURY_START, Engine
from civ.core.events import EventLog
from civ.core.rng import RNG


def test_rng_streams_deterministic_and_independent():
    a1, a2 = RNG(7).child("a"), RNG(7).child("a")
    b = RNG(7).child("b")
    seq = lambda r: [r.random() for _ in range(5)]
    assert seq(a1) == seq(a2)
    assert seq(RNG(7).child("a")) != seq(b)


def test_needs_are_lazy_and_clamped():
    n = Needs({"hunger": 80, "energy": 90, "social": 70, "fun": 60}, 0)
    assert n.value("hunger", 5 * HOUR) == 80 - 4 * 5
    assert n.value("hunger", 1000 * HOUR) == 0.0
    n.settle(2 * HOUR)                       # energy: 90 - 2*5 = 80
    assert n.values["energy"] == 80.0
    n.set_activity("sleep")                  # +12.5/h
    assert n.value("energy", 3 * HOUR) == 92.5
    assert n.value("energy", 4 * HOUR) == 100.0   # clamped
    n.set_activity("idle")
    assert n.time_to("hunger", 40, 2 * HOUR) == (72 - 40) / 4 * HOUR
    assert n.time_to("hunger", 90, 2 * HOUR) is None  # already below threshold and falling


def test_same_seed_same_world_different_seed_differs():
    a, b, c = Engine(seed=3), Engine(seed=3), Engine(seed=4)
    for e in (a, b, c):
        e.run_days(20)
    assert a.log.digest() == b.log.digest()
    assert a.log.digest() != c.log.digest()


def test_invariants_over_60_days():
    e = Engine(seed=11)
    for _ in range(60):
        e.run_until(e.clock.now + DAY)
        assert e.ledger.total() == TREASURY_START
        for a in e.agents.values():
            for n in a.needs.values:
                assert 0.0 <= a.needs.value(n, e.clock.now) <= 100.0
            assert a.pantry >= 0 and e.ledger.balance(a.account) >= 0
    times = [ev.time for ev in e.log.query()]
    assert times == sorted(times)
    assert all(a.alive for a in e.agents.values()), e.summary()


def test_no_activity_after_death():
    e = Engine(seed=2)
    e.run_days(5)
    a = e.agents[1]
    a.alive, a.state = False, "dead"
    a.token += 1
    e.log.append(e.clock.now, "death", (1,), a.location, {})
    t_death = e.clock.now
    e.run_days(10)
    after = [ev for ev in e.log.query(actor=1, since=t_death + 1) if ev.type in ("activity", "decision", "travel")]
    assert after == []


def test_town_is_alive_and_varied():
    e = Engine(seed=5)
    e.run_days(30)
    kinds = {ev.payload["kind"] for ev in e.log.query(types=("activity",))}
    assert {"sleep", "eat", "work", "coffee", "read", "socialize", "stroll"} <= kinds
    assert e.log.count("conversation") >= 50
    assert max(r["familiarity"] for r in e.relations.values()) >= 5
    # every resident goes to their own workplace and gets paid
    assert len({ev.actors[0] for ev in e.log.query(types=("wage",))}) == e.n_agents


def test_two_agent_world_still_works():
    e = Engine(seed=5, n_agents=2)
    e.run_days(30)
    assert e.log.count("conversation") >= 5 and all(a.alive for a in e.agents.values())


def test_event_log_persists_to_disk(tmp_path):
    path = str(tmp_path / "w.db")
    e = Engine(seed=9, db=path)
    e.run_days(3)
    n = e.log.count()
    assert n > 0
    assert EventLog(path).count() == n
