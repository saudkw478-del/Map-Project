"""Discrete-event simulation engine (Phase 0): needs, routines, work, money, meetings. No LLM."""
from civ.agents.agent import Agent, Step
from civ.agents.needs import Needs
from civ.core.clock import DAY, HOUR, SimClock, day_index
from civ.core.events import EventLog
from civ.core.ledger import Ledger
from civ.core.rng import RNG
from civ.core.scheduler import Scheduler
from civ.decision.utility import CHATTY, COFFEE_PRICE, EAT_RESTORE, FOOD_PRICE, GIFT_PRICE, PASTRY_PRICE, decide
from civ.world.world import default_world

WAGE = 40
TREASURY_START = 20_000
BILLS = 10                 # daily household cost paid to the town treasury
SHOP_ACCOUNTS = ("market", "bakery", "cafe", "shop")
START_MONEY = 120
START_TIME = 6 * HOUR  # 06:00 on day 0

MALE_NAMES = ["خالد", "أحمد", "سلمان", "يوسف", "عبدالله", "فهد", "ناصر", "ماجد"]
FEMALE_NAMES = ["ليلى", "سارة", "نورة", "مريم", "هند", "فاطمة", "دانة", "ريم"]
TOPICS = ["work", "food", "weather", "plans", "each_other", "health", "books", "coffee", "town"]
# (workplace location id, title, possible shift start hours)
JOBS = [("market", "shopkeeper", (8, 9)), ("cafe", "barista", (7, 8)), ("library", "librarian", (9, 10)), ("farm", "farmer", (7, 8)),
        ("bakery", "baker", (6, 7)), ("gift", "clerk", (9, 10)), ("farm", "farmer", (8, 9)), ("farm", "farmer", (7, 8))]
SHOP_OF = {"buy": "market", "pastry": "bakery", "coffee": "cafe", "browse": "shop"}


class Engine:
    def __init__(self, seed: int = 1, db: str = ":memory:", n_agents: int = 8):
        self.seed = seed
        self.rng = RNG(seed)
        self.clock = SimClock(START_TIME)
        self.log = EventLog(db)
        self.n_agents = n_agents
        self.world = default_world(n_agents)
        self.ledger = Ledger()
        self.sched = Scheduler()
        self.agents: dict[int, Agent] = {}
        self.relations: dict[tuple[int, int], dict] = {}
        self.last_talk: dict[tuple[int, int], float] = {}
        self.ledger.open("treasury", TREASURY_START)
        for acc in SHOP_ACCOUNTS:
            self.ledger.open(acc, 0)
        self._bootstrap()

    # ---------- setup ----------
    def _bootstrap(self) -> None:
        r = self.rng.child("bootstrap")
        males, females = list(MALE_NAMES), list(FEMALE_NAMES)
        for aid in range(1, self.n_agents + 1):
            sex = "M" if aid % 2 == 1 else "F"
            pool = males if sex == "M" else females
            name = pool.pop(int(r.random() * len(pool)))
            ar = self.rng.child(f"agent{aid}")
            traits = {k: round(min(0.95, max(0.15, r.gauss(0.55, 0.22))), 3) for k in ("diligence", "sociability", "thrift", "curiosity", "sweet")}
            place, title, shifts = JOBS[(aid - 1) % len(JOBS)]
            home = f"home_{aid}"
            a = Agent(
                id=aid, name=name, sex=sex, birth_time=-int(r.uniform(22, 50)) * 365 * DAY, home=home, workplace=place, job_title=title,
                traits=traits, needs=Needs({"hunger": r.uniform(60, 90), "energy": r.uniform(75, 100), "social": r.uniform(40, 80), "fun": r.uniform(40, 80)}, START_TIME),
                rng=ar, location=home, shift_start=r.choice(list(shifts)), wake_hour=r.choice([5, 6, 7]), pantry=3,
            )
            self.agents[aid] = a
            self.ledger.open(a.account, 0)
            self.ledger.transfer("treasury", a.account, START_MONEY)
            self.log.append(START_TIME, "agent_created", (aid,), home, {"name": a.name, "sex": sex, "job": title, "traits": traits})
            self.sched.push(START_TIME + aid * 60, "decide", {"id": aid})
        self.sched.push((day_index(START_TIME) + 1) * DAY, "daily", {})

    # ---------- helpers ----------
    def other_alive(self, agent: Agent) -> bool:
        return any(o.alive for o in self.agents.values() if o.id != agent.id)

    def _emit(self, type: str, actors, location, payload=None):
        return self.log.append(self.clock.now, type, actors, location, payload)

    # ---------- main loop ----------
    def run_until(self, t_end: float) -> None:
        while self.sched.peek_time() is not None and self.sched.peek_time() <= t_end:
            item = self.sched.pop()
            self.clock.set(item.time)
            getattr(self, f"_on_{item.kind}")(item.data)
        self.log.flush()

    def run_days(self, days: float) -> None:
        self.run_until(START_TIME + days * DAY)

    # ---------- handlers ----------
    def _on_decide(self, data: dict) -> None:
        a = self.agents[data["id"]]
        if not a.alive:
            return
        t = self.clock.now
        choice, scores, plan = decide(a, self, t)
        self._emit("decision", (a.id,), a.location, {"choice": choice, "scores": {k: round(v, 3) for k, v in sorted(scores.items())}})
        a.plan = plan
        self._next_step(a)

    def _next_step(self, a: Agent) -> None:
        if not a.plan:
            self.sched.push(self.clock.now, "decide", {"id": a.id})
            return
        step = a.plan.pop(0)
        t = self.clock.now
        a.needs.settle(t)
        a.needs.set_activity(step.kind)
        a.state, a.step, a.step_started, a.talked_this_step = step.kind, step, t, False
        a.token += 1
        if step.kind == "travel":
            a.location = "transit"
        else:
            a.location = step.location
            if step.kind in CHATTY:
                self._try_meet(a)
        self.sched.push(t + step.duration, "step_end", {"id": a.id, "token": a.token})

    def _on_step_end(self, data: dict) -> None:
        a = self.agents[data["id"]]
        if not a.alive or data["token"] != a.token:
            return
        t, step = self.clock.now, a.step
        a.needs.settle(t)
        if step.kind == "travel":
            a.location = step.meta["to"]
            self._emit("travel", (a.id,), a.location, {"from": step.meta["from"], "start": round(a.step_started, 3)})
        else:
            self._finish_activity(a, step, t)
        self._next_step(a)

    def _pay(self, a: Agent, shop_kind: str, price: int, item: str, qty: int, loc) -> bool:
        if self.ledger.transfer(a.account, SHOP_OF[shop_kind], price):
            self._emit("purchase", (a.id,), loc, {"item": item, "qty": qty, "cost": price})
            return True
        return False

    def _finish_activity(self, a: Agent, step: Step, t: float) -> None:
        k = step.kind
        payload = {"kind": k, "start": round(a.step_started, 3)}
        if k == "eat":
            a.pantry -= 1
            a.needs.add("hunger", EAT_RESTORE)
        elif k == "buy":
            qty = min(3, self.ledger.balance(a.account) // FOOD_PRICE)
            if qty and self._pay(a, "buy", qty * FOOD_PRICE, "food", qty, step.location):
                a.pantry += qty
        elif k == "pastry":
            if self._pay(a, "pastry", PASTRY_PRICE, "pastry", 1, step.location):
                a.needs.add("hunger", 35.0)
                a.needs.add("fun", 5.0)
        elif k == "coffee":
            if self._pay(a, "coffee", COFFEE_PRICE, "coffee", 1, step.location):
                a.needs.add("hunger", 8.0)
                a.needs.add("fun", 12.0)
            if not a.talked_this_step:
                a.needs.add("social", 6.0)
        elif k == "browse":
            if self._pay(a, "browse", GIFT_PRICE, "gift", 1, step.location):
                a.needs.add("fun", 22.0)
            else:
                a.needs.add("fun", 6.0)
        elif k == "read":
            a.needs.add("fun", 30.0)
        elif k == "stroll":
            a.needs.add("fun", 10.0)
            a.needs.add("social", 3.0)
        elif k == "forage":
            if a.rng.chance(0.7):
                a.pantry += 1
                payload["found"] = 1
        elif k == "work":
            a.last_work_day = day_index(a.step_started)
            paid = WAGE if self.ledger.transfer("treasury", a.account, WAGE) else 0
            self._emit("wage", (a.id,), step.location, {"amount": paid, "job": a.job_title})
        elif k == "socialize" and not a.talked_this_step:
            a.needs.add("social", 5.0)
        self._emit("activity", (a.id,), step.location, payload)

    def _try_meet(self, a: Agent) -> None:
        t = self.clock.now
        for o in self.agents.values():
            if o.id == a.id or not o.alive or o.state not in CHATTY or o.location != a.location:
                continue
            key = (min(a.id, o.id), max(a.id, o.id))
            if t - self.last_talk.get(key, -1e18) < 2 * HOUR:
                continue
            self.last_talk[key] = t
            rel = self.relations.setdefault(key, {"familiarity": 0, "affinity": 0.0})
            compat = 1.0 - abs(a.traits["sociability"] - o.traits["sociability"])
            rel["familiarity"] += 1
            rel["affinity"] = round(rel["affinity"] + 2.0 * compat - 0.6 + a.rng.uniform(-0.5, 0.5), 3)
            topic = a.rng.choice(TOPICS)
            for p in (a, o):
                p.needs.settle(t)
                p.needs.add("social", 35.0)
                p.talked_this_step = True
            # text is NOT generated here: outcome is decided by rules, dialogue text is rendered lazily later
            self._emit("conversation", key, a.location, {"topic": topic, "affinity": rel["affinity"], "familiarity": rel["familiarity"]})

    def _on_daily(self, data: dict) -> None:
        t = self.clock.now
        for acc in SHOP_ACCOUNTS:
            bal = self.ledger.balance(acc)
            if bal > 0:
                self.ledger.transfer(acc, "treasury", bal)
                self._emit("market_remit", (), acc, {"amount": bal})
        for a in sorted(self.agents.values(), key=lambda x: x.id):
            if not a.alive:
                continue
            self.ledger.transfer(a.account, "treasury", min(BILLS, self.ledger.balance(a.account)))
            a.needs.settle(t)
            n = a.needs.values
            if n["hunger"] <= 5:
                a.health -= 10
            elif n["energy"] <= 5:
                a.health -= 5
            else:
                a.health = min(100.0, a.health + 2)
            if a.health <= 0:
                a.alive, a.state = False, "dead"
                a.token += 1
                self._emit("death", (a.id,), a.location, {"cause": "neglect"})
        self.sched.push(t + DAY, "daily", {})

    # ---------- reporting ----------
    def summary(self) -> dict:
        t = self.clock.now
        out = {"time_days": round((t - START_TIME) / DAY, 2), "digest": self.log.digest(), "money_total": self.ledger.total(), "agents": {}}
        for a in self.agents.values():
            out["agents"][a.id] = {
                "name": a.name, "alive": a.alive, "health": round(a.health, 1), "money": self.ledger.balance(a.account),
                "pantry": a.pantry, "job": a.job_title, "needs": {n: round(a.needs.value(n, t), 1) for n in a.needs.values},
            }
        out["relations"] = {f"{k[0]}-{k[1]}": v for k, v in self.relations.items()}
        return out
