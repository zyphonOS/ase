"""ASE state journal - her durable continuity.

ASE's verifiable acts live on-chain (wallet, tx, attestation) and in signed
attestation files. Her RUNNING MEMORY (every cycle: block, decision, payment,
attestation) is journaled here, append-only JSONL, so she survives restarts
with full memory of her life instead of an in-memory reset.

Path: {repo}/state/ase_journal.jsonl
"""
import json
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
STATE = ROOT / "state"
JOURNAL = STATE / "ase_journal.jsonl"
_lock = threading.Lock()


def _ensure():
    STATE.mkdir(parents=True, exist_ok=True)


def append(entry: dict) -> dict:
    """Append one durable record. Returns the entry with ts set if missing."""
    _ensure()
    rec = dict(entry)
    rec.setdefault("ts", int(time.time()))
    rec.setdefault("ts_iso", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    with _lock:
        with open(JOURNAL, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
    return rec


def read_all(n: int | None = None) -> list[dict]:
    """Read journal entries, chronologically. n = most recent N."""
    if not JOURNAL.exists():
        return []
    with _lock:
        with open(JOURNAL, encoding="utf-8") as f:
            lines = f.readlines()
    entries = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except Exception:
            continue
    if n is not None:
        return entries[-n:]
    return entries


def count() -> int:
    return len(read_all())


def path() -> str:
    return str(JOURNAL)