"""C12 durable multi-actor continuation store (SQLite, append-only).

Every branch owns an append-only episode/world-event/perception/checkpoint
history. UPDATE and DELETE are refused by triggers. A fork copies only rows at
or before the fork clock, preserving their exact hashes; post-fork divergence is
branch-local. This is a TEST_ONLY technical store, not native C12.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .canon import assert_no_forbidden, canonical, digest, seal, valid

STORE_SCHEMA = "BP4_C12_STORE@1"
GRADE = "TEST_ONLY_SOURCEFREE_C12_TECHNICAL_NOT_NATIVE"


class StoreRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def _append_only_triggers(conn: sqlite3.Connection, table: str) -> None:
    conn.execute(
        f"CREATE TRIGGER IF NOT EXISTS {table}_no_update BEFORE UPDATE ON {table} "
        f"BEGIN SELECT RAISE(ABORT, 'APPEND_ONLY_UPDATE_REFUSED'); END"
    )
    conn.execute(
        f"CREATE TRIGGER IF NOT EXISTS {table}_no_delete BEFORE DELETE ON {table} "
        f"BEGIN SELECT RAISE(ABORT, 'APPEND_ONLY_DELETE_REFUSED'); END"
    )


class C12Store:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(self.path), isolation_level=None)
        self.db.executescript(
            """
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS branch (
                branch_id TEXT PRIMARY KEY,
                parent_branch_id TEXT,
                fork_clock INTEGER,
                root_hash TEXT,
                root_counts TEXT,
                created_clock INTEGER NOT NULL,
                actor_ids TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS episode (
                branch_id TEXT NOT NULL, seq INTEGER NOT NULL, episode_id TEXT NOT NULL,
                actor_id TEXT NOT NULL, kind TEXT NOT NULL, clock INTEGER NOT NULL,
                body TEXT NOT NULL, hash TEXT NOT NULL,
                PRIMARY KEY (branch_id, seq), UNIQUE (branch_id, episode_id),
                FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
            );
            CREATE TABLE IF NOT EXISTS world_event (
                branch_id TEXT NOT NULL, seq INTEGER NOT NULL, event_id TEXT NOT NULL,
                clock INTEGER NOT NULL, body TEXT NOT NULL, hash TEXT NOT NULL,
                PRIMARY KEY (branch_id, seq), UNIQUE (branch_id, event_id),
                FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
            );
            CREATE TABLE IF NOT EXISTS perception (
                branch_id TEXT NOT NULL, seq INTEGER NOT NULL, actor_id TEXT NOT NULL,
                event_id TEXT NOT NULL, clock INTEGER NOT NULL, channel TEXT NOT NULL,
                PRIMARY KEY (branch_id, seq), UNIQUE (branch_id, actor_id, event_id),
                FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
            );
            CREATE TABLE IF NOT EXISTS checkpoint (
                branch_id TEXT NOT NULL, seq INTEGER NOT NULL, clock INTEGER NOT NULL,
                state TEXT NOT NULL, hash TEXT NOT NULL,
                PRIMARY KEY (branch_id, seq),
                FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
            );
            """
        )
        for table in ("episode", "world_event", "perception", "checkpoint"):
            _append_only_triggers(self.db, table)
        self.db.execute(
            "INSERT OR IGNORE INTO meta VALUES ('schema', ?)", (STORE_SCHEMA,)
        )

    def close(self) -> None:
        self.db.close()

    def __enter__(self) -> "C12Store":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # ---------------- branch creation ----------------
    def create_root(self, branch_id: str, *, clock: int, actor_ids: list[str],
                    state: dict) -> dict:
        if self._branch(branch_id) is not None:
            raise StoreRefusal("BRANCH_EXISTS")
        self.db.execute(
            "INSERT INTO branch VALUES (?,?,?,?,?,?,?)",
            (branch_id, None, None, "", canonical({}), int(clock),
             canonical(sorted(actor_ids))),
        )
        self.checkpoint(branch_id, clock, state)
        return self.branch(branch_id)

    def _branch(self, branch_id: str) -> dict | None:
        row = self.db.execute(
            "SELECT branch_id,parent_branch_id,fork_clock,root_hash,root_counts,created_clock,actor_ids "
            "FROM branch WHERE branch_id=?", (branch_id,)
        ).fetchone()
        if row is None:
            return None
        return {
            "branch_id": row[0], "parent_branch_id": row[1], "fork_clock": row[2],
            "root_hash": row[3], "root_counts": json.loads(row[4] or "{}"),
            "created_clock": row[5], "actor_ids": json.loads(row[6]),
        }

    def branch(self, branch_id: str) -> dict:
        row = self._branch(branch_id)
        if row is None:
            raise StoreRefusal("BRANCH_NOT_FOUND", branch_id)
        return row

    def branches(self) -> list[dict]:
        return [self.branch(r[0]) for r in self.db.execute(
            "SELECT branch_id FROM branch ORDER BY branch_id")]

    # ---------------- append operations ----------------
    def _last_clock(self, branch_id: str) -> int:
        values = [0]
        for table in ("episode", "world_event", "checkpoint"):
            row = self.db.execute(
                f"SELECT max(clock) FROM {table} WHERE branch_id=?", (branch_id,)
            ).fetchone()
            if row and row[0] is not None:
                values.append(int(row[0]))
        return max(values)

    def _next_seq(self, table: str, branch_id: str) -> int:
        row = self.db.execute(
            f"SELECT coalesce(max(seq),-1)+1 FROM {table} WHERE branch_id=?", (branch_id,)
        ).fetchone()
        return int(row[0])

    def append_episode(self, branch_id: str, *, actor_id: str, kind: str,
                       clock: int, body: dict) -> dict:
        branch = self.branch(branch_id)
        if actor_id not in branch["actor_ids"]:
            raise StoreRefusal("ACTOR_NOT_IN_BRANCH", actor_id)
        if int(clock) < self._last_clock(branch_id):
            raise StoreRefusal("RETROACTIVE_EPISODE")
        assert_no_forbidden(body)
        episode = {
            "schema": "BP4_C12_EPISODE@1",
            "branch_id": branch_id,
            "actor_id": actor_id,
            "kind": kind,
            "clock": int(clock),
            "body": body,
            "grade": GRADE,
            "native": False,
        }
        episode["hash"] = digest(episode)
        episode["episode_id"] = "TEST_ONLY_BP4_EP_" + episode["hash"]
        seq = self._next_seq("episode", branch_id)
        self.db.execute(
            "INSERT INTO episode VALUES (?,?,?,?,?,?,?,?)",
            (branch_id, seq, episode["episode_id"], actor_id, kind, int(clock),
             canonical(episode), episode["hash"]),
        )
        return episode

    def append_world_event(self, branch_id: str, event: dict) -> dict:
        self.branch(branch_id)
        if any(row[0] == event["event_id"] for row in self.db.execute(
                "SELECT event_id FROM world_event WHERE branch_id=? AND event_id=?",
                (branch_id, event["event_id"]))):
            raise StoreRefusal("DUPLICATE_WORLD_EVENT")
        if int(event["clock"]) < self._last_clock(branch_id):
            raise StoreRefusal("RETROACTIVE_WORLD_EVENT")
        seq = self._next_seq("world_event", branch_id)
        self.db.execute(
            "INSERT INTO world_event VALUES (?,?,?,?,?,?)",
            (branch_id, seq, event["event_id"], int(event["clock"]),
             canonical(event), event["hash"]),
        )
        return event

    def record_perception(self, branch_id: str, *, actor_id: str, event_id: str,
                          clock: int, channel: str) -> dict:
        branch = self.branch(branch_id)
        if actor_id not in branch["actor_ids"]:
            raise StoreRefusal("ACTOR_NOT_IN_BRANCH")
        if not self.world_event(branch_id, event_id):
            raise StoreRefusal("PERCEIVED_EVENT_NOT_IN_BRANCH")
        if int(clock) < self._last_clock(branch_id):
            raise StoreRefusal("RETROACTIVE_PERCEPTION")
        try:
            seq = self._next_seq("perception", branch_id)
            self.db.execute(
                "INSERT INTO perception VALUES (?,?,?,?,?,?)",
                (branch_id, seq, actor_id, event_id, int(clock), channel),
            )
        except sqlite3.IntegrityError:
            return {"actor_id": actor_id, "event_id": event_id, "clock": int(clock),
                    "channel": channel, "duplicate": True}
        return {"actor_id": actor_id, "event_id": event_id, "clock": int(clock),
                "channel": channel, "duplicate": False}

    def checkpoint(self, branch_id: str, clock: int, state: dict) -> dict:
        self.branch(branch_id)
        if int(clock) < self._last_clock(branch_id):
            raise StoreRefusal("RETROACTIVE_CHECKPOINT")
        body = {
            "schema": "BP4_C12_CHECKPOINT@1",
            "branch_id": branch_id,
            "clock": int(clock),
            "state": state,
            "grade": GRADE,
            "native": False,
        }
        body["hash"] = digest(body)
        seq = self._next_seq("checkpoint", branch_id)
        self.db.execute(
            "INSERT INTO checkpoint VALUES (?,?,?,?,?)",
            (branch_id, seq, int(clock), canonical(body), body["hash"]),
        )
        return body

    # ---------------- read ----------------
    def episodes(self, branch_id: str) -> list[dict]:
        self.branch(branch_id)
        rows = self.db.execute(
            "SELECT body FROM episode WHERE branch_id=? ORDER BY seq", (branch_id,)
        ).fetchall()
        return [json.loads(r[0]) for r in rows]

    def world_events(self, branch_id: str) -> list[dict]:
        self.branch(branch_id)
        rows = self.db.execute(
            "SELECT body FROM world_event WHERE branch_id=? ORDER BY seq", (branch_id,)
        ).fetchall()
        return [json.loads(r[0]) for r in rows]

    def world_event(self, branch_id: str, event_id: str) -> dict | None:
        row = self.db.execute(
            "SELECT body FROM world_event WHERE branch_id=? AND event_id=?",
            (branch_id, event_id),
        ).fetchone()
        return json.loads(row[0]) if row else None

    def perceptions(self, branch_id: str, actor_id: str | None = None) -> list[dict]:
        self.branch(branch_id)
        if actor_id is None:
            rows = self.db.execute(
                "SELECT actor_id,event_id,clock,channel FROM perception "
                "WHERE branch_id=? ORDER BY seq", (branch_id,)).fetchall()
        else:
            rows = self.db.execute(
                "SELECT actor_id,event_id,clock,channel FROM perception "
                "WHERE branch_id=? AND actor_id=? ORDER BY seq", (branch_id, actor_id)).fetchall()
        return [{"actor_id": r[0], "event_id": r[1], "clock": r[2], "channel": r[3]}
                for r in rows]

    def checkpoints(self, branch_id: str) -> list[dict]:
        self.branch(branch_id)
        rows = self.db.execute(
            "SELECT state FROM checkpoint WHERE branch_id=? ORDER BY seq", (branch_id,)
        ).fetchall()
        return [json.loads(r[0]) for r in rows]

    def latest_state(self, branch_id: str) -> dict:
        cps = self.checkpoints(branch_id)
        if not cps:
            raise StoreRefusal("NO_CHECKPOINT")
        return cps[-1]["state"]

    def last_clock(self, branch_id: str) -> int:
        return self._last_clock(branch_id)

    def verify(self, branch_id: str) -> dict:
        self.branch(branch_id)
        errors: list[str] = []
        for row in self.db.execute(
                "SELECT seq,body,hash FROM episode WHERE branch_id=? ORDER BY seq",
                (branch_id,)):
            if digest(json.loads(row[1])) != row[2]:
                errors.append(f"episode:{row[0]}")
        for row in self.db.execute(
                "SELECT seq,body,hash FROM world_event WHERE branch_id=? ORDER BY seq",
                (branch_id,)):
            if digest(json.loads(row[1])) != row[2]:
                errors.append(f"world_event:{row[0]}")
        for row in self.db.execute(
                "SELECT seq,state,hash FROM checkpoint WHERE branch_id=? ORDER BY seq",
                (branch_id,)):
            if digest(json.loads(row[1])) != row[2]:
                errors.append(f"checkpoint:{row[0]}")
        ep = [r[0] for r in self.db.execute(
            "SELECT seq FROM episode WHERE branch_id=? ORDER BY seq", (branch_id,))]
        we = [r[0] for r in self.db.execute(
            "SELECT seq FROM world_event WHERE branch_id=? ORDER BY seq", (branch_id,))]
        cp = [r[0] for r in self.db.execute(
            "SELECT seq FROM checkpoint WHERE branch_id=? ORDER BY seq", (branch_id,))]
        if ep != list(range(len(ep))):
            errors.append("episode_seq_not_contiguous")
        if we != list(range(len(we))):
            errors.append("world_event_seq_not_contiguous")
        if cp != list(range(len(cp))):
            errors.append("checkpoint_seq_not_contiguous")
        return {"ok": not errors, "errors": errors,
                "counts": {"episodes": len(ep), "world_events": len(we),
                           "checkpoints": len(cp),
                           "perceptions": len(self.perceptions(branch_id))}}

    # ---------------- fork ----------------
    def fork(self, parent_branch_id: str, new_branch_id: str) -> dict:
        parent = self.branch(parent_branch_id)
        if self._branch(new_branch_id) is not None:
            raise StoreRefusal("BRANCH_EXISTS")
        latest_perception = self.db.execute(
            "SELECT coalesce(max(clock),0) FROM perception WHERE branch_id=?",
            (parent_branch_id,),
        ).fetchone()[0]
        fork_clock = max(self.last_clock(parent_branch_id), int(latest_perception))
        self.db.execute(
            "INSERT INTO branch VALUES (?,?,?,?,?,?,?)",
            (new_branch_id, parent_branch_id, int(fork_clock), "", canonical({}),
             int(fork_clock), canonical(parent["actor_ids"])),
        )
        copied_hashes: list[str] = []
        copied_counts: dict[str, int] = {}
        for table in ("episode", "world_event", "perception", "checkpoint"):
            rows = self.db.execute(
                f"SELECT * FROM {table} WHERE branch_id=? AND "
                + ("clock<=?" if table != "perception" else "clock<=?")
                + " ORDER BY seq",
                (parent_branch_id, int(fork_clock)),
            ).fetchall()
            columns = {
                "episode": 8, "world_event": 6, "perception": 6, "checkpoint": 5,
            }[table]
            copied_counts[table] = len(rows)
            for row in rows:
                values = list(row)
                values[0] = new_branch_id
                placeholders = ",".join("?" for _ in range(columns))
                self.db.execute(
                    f"INSERT INTO {table} VALUES ({placeholders})", tuple(values)
                )
                if table == "episode":
                    copied_hashes.append(str(row[7]))
                elif table == "world_event":
                    copied_hashes.append(str(row[5]))
                elif table == "checkpoint":
                    copied_hashes.append(str(row[4]))
        root_hash = digest({"parent": parent_branch_id, "fork_clock": int(fork_clock),
                            "hashes": sorted(copied_hashes)})
        self.db.execute(
            "UPDATE branch SET root_hash=?, root_counts=? WHERE branch_id=?",
            (root_hash, canonical(copied_counts), new_branch_id),
        )
        # The branch row update is metadata, not append-only history. Only the
        # branch table is mutable; episode/world/perception/checkpoint stay fixed.
        return self.branch(new_branch_id)

    def shared_root_equal(self, branch_a: str, branch_b: str) -> dict:
        a = self.branch(branch_a)
        b = self.branch(branch_b)

        def rows(branch: str, table: str, limit: int | None = None) -> list:
            clauses = {"episode": "seq,hash", "world_event": "seq,hash",
                       "checkpoint": "seq,hash", "perception": "seq,event_id,actor_id"}[table]
            sql = f"SELECT {clauses} FROM {table} WHERE branch_id=? ORDER BY seq"
            values = (branch,)
            if limit is not None:
                sql += " LIMIT ?"
                values = (branch, int(limit))
            return [tuple(r) for r in self.db.execute(sql, values)]

        tables = ("episode", "world_event", "checkpoint", "perception")
        if a["parent_branch_id"] == b["branch_id"]:
            child, parent = a, b
        elif b["parent_branch_id"] == a["branch_id"]:
            child, parent = b, a
        elif (a["parent_branch_id"] is not None
              and a["parent_branch_id"] == b["parent_branch_id"]):
            return {"equal": a["root_hash"] == b["root_hash"]
                    and a["root_counts"] == b["root_counts"],
                    "fork_clock": min(a["fork_clock"], b["fork_clock"]),
                    "mode": "siblings"}
        else:
            raise StoreRefusal("NOT_SIBLING_OR_PARENT_CHILD_BRANCHES")
        counts = child.get("root_counts") or {}
        equal = True
        detail = {}
        for table in tables:
            n = int(counts.get(table, 0))
            parent_rows = rows(parent["branch_id"], table, n)
            child_rows = rows(child["branch_id"], table, n)
            same = parent_rows == child_rows
            equal = equal and same
            detail[table] = {"equal": same, "count": n}
        return {"equal": equal, "fork_clock": child["fork_clock"],
                "mode": "parent_child", "detail": detail}
