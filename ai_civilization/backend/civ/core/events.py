"""Append-only event log (source of truth) backed by SQLite, with a running digest for replay checks."""
import hashlib
import json
import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    seq: int
    time: float
    type: str
    actors: tuple
    location: str | None
    payload: dict


class EventLog:
    def __init__(self, path: str = ":memory:"):
        self.db = sqlite3.connect(path)
        self.db.execute("PRAGMA journal_mode=WAL" if path != ":memory:" else "PRAGMA journal_mode=MEMORY")
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS events("
            "seq INTEGER PRIMARY KEY, sim_time REAL, type TEXT, actors TEXT, location TEXT, payload TEXT)"
        )
        row = self.db.execute("SELECT COALESCE(MAX(seq),0) FROM events").fetchone()
        self._seq = row[0]
        self._hash = hashlib.sha256()
        self._subs = []
        self._pending = []

    def subscribe(self, fn) -> None:
        self._subs.append(fn)

    def append(self, time: float, type: str, actors=(), location=None, payload=None) -> Event:
        self._seq += 1
        payload = payload or {}
        ev = Event(self._seq, round(time, 3), type, tuple(actors), location, payload)
        pj = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        actors_s = "," + ",".join(str(a) for a in ev.actors) + ","
        self._hash.update(f"{ev.seq}|{ev.time}|{type}|{actors_s}|{location}|{pj}\n".encode())
        self._pending.append((ev.seq, ev.time, type, actors_s, location, pj))
        for fn in self._subs:
            fn(ev)
        return ev

    def flush(self) -> None:
        if self._pending:
            self.db.executemany("INSERT INTO events VALUES (?,?,?,?,?,?)", self._pending)
            self.db.commit()
            self._pending.clear()

    def digest(self) -> str:
        return self._hash.hexdigest()

    def count(self, type: str | None = None) -> int:
        self.flush()
        if type:
            return self.db.execute("SELECT COUNT(*) FROM events WHERE type=?", (type,)).fetchone()[0]
        return self.db.execute("SELECT COUNT(*) FROM events").fetchone()[0]

    def query(self, actor=None, since=None, until=None, types=None) -> list[Event]:
        self.flush()
        sql, args = "SELECT seq,sim_time,type,actors,location,payload FROM events WHERE 1=1", []
        if actor is not None:
            sql += " AND actors LIKE ?"
            args.append(f"%,{actor},%")
        if since is not None:
            sql += " AND sim_time>=?"
            args.append(since)
        if until is not None:
            sql += " AND sim_time<?"
            args.append(until)
        if types:
            sql += " AND type IN (%s)" % ",".join("?" * len(types))
            args += list(types)
        rows = self.db.execute(sql + " ORDER BY seq", args).fetchall()
        return [
            Event(r[0], r[1], r[2], tuple(int(x) for x in r[3].strip(",").split(",") if x), r[4], json.loads(r[5]))
            for r in rows
        ]
