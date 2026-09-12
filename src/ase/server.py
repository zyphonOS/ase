"""ASE Dashboard Backend — HTTP server wrapping the agent cycle.

Serves:
  GET /api/state      → full agent state (cycle, action, attestation, activity)
  GET /api/activity   → activity event log
  GET /api/attestation → current attestation data
  GET /api/status     → agent online status
  POST /api/cycle     → trigger one acting cycle (for demo/judging)
  GET /               → serve dashboard static files (dist/)

Run:
  python -m ase.server              # start on :8000
  python -m ase.server --port 9000  # custom port
"""
import json
import sys
import time
import threading
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

# Agent state singleton
_state = {
    "online": True,
    "mode": "live",
    "cycle": {
        "currentStage": "read",
        "stages": [
            {"name": "read", "status": "pending"},
            {"name": "decide", "status": "pending"},
            {"name": "pay", "status": "pending"},
            {"name": "act", "status": "pending"},
            {"name": "attest", "status": "pending"},
        ],
    },
    "action": {
        "type": "live-read",
        "live": {
            "subgraph": "The Graph",
            "balance": "—",
            "token": "USDC",
            "blockNumber": 0,
        },
    },
    "attestation": {
        "signature": "",
        "block": 0,
        "valid": False,
        "subgraph": "The Graph",
        "balance": "—",
    },
    "activity": [],
}

_lock = threading.Lock()


def _ts():
    return time.strftime("%H:%M:%S", time.gmtime())


def _add_event(stage, message, tx_hash=""):
    with _lock:
        _state["activity"].append({
            "timestamp": _ts(),
            "stage": stage,
            "message": message,
            "txHash": tx_hash,
        })
        # keep last 50
        if len(_state["activity"]) > 50:
            _state["activity"] = _state["activity"][-50:]
    # durable journal (continuity across restarts)
    try:
        from .journal import append as _jappend
        _jappend({"kind": "event", "stage": stage, "message": message,
                  "tx_hash": tx_hash})
    except Exception:
        pass


def _recover_activity():
    """On startup, remount ASE's durable memory (journal) into the live activity log."""
    try:
        from .journal import read_all as _jread
        records = _jread()
    except Exception:
        return
    for rec in records[-40:]:
        try:
            if rec.get("kind") == "cycle":
                msg = (f"Cycle  block {rec.get('block')}  {rec.get('decision','')[:80]}"
                       + ("  PAID" if rec.get("paid") else ""))
                _state["activity"].append({
                    "timestamp": rec.get("ts_iso", "")[11:19],
                    "stage": "act",
                    "message": msg,
                    "attestation": True,
                })
            elif rec.get("kind") == "event":
                _state["activity"].append({
                    "timestamp": rec.get("ts_iso", "")[11:19],
                    "stage": rec.get("stage", ""),
                    "message": rec.get("message", ""),
                    "txHash": rec.get("tx_hash", ""),
                })
        except Exception:
            continue
    _state["activity"] = _state["activity"][-50:]


def _set_stage(name, status):
    with _lock:
        for s in _state["cycle"]["stages"]:
            if s["name"] == name:
                s["status"] = status
        _state["cycle"]["currentStage"] = name


def run_live_cycle():
    """Run one full ASE cycle and update state. Returns the cycle result dict."""
    from .config import load_config
    from .wallet import load_wallet
    from .agent import run_cycle

    config = load_config()
    if not config.has_wallet:
        _add_event("read", "No ASE_PRIVATE_KEY — cannot run live cycle")
        return None

    wallet = load_wallet(config.private_key)
    from web3 import Web3
    w3 = Web3(Web3.HTTPProvider(config.rpc_url, request_kwargs={"timeout": 15}))

    # READ
    _set_stage("read", "active")
    _add_event("read", f"Reading chain state at block...")
    try:
        from .read import read_chain_state
        reading = read_chain_state(config.rpc_url, config.usdc_address, wallet.address)
        bal = reading.data.get("human", 0.0)
        _add_event("read", f"Block {reading.block} — USDC balance: {bal:.2f}")
        with _lock:
            _state["action"] = {
                "type": "live-read",
                "live": {
                    "subgraph": "The Graph",
                    "balance": f"{bal:.2f} USDC",
                    "token": "USDC",
                    "blockNumber": reading.block,
                },
            }
        _set_stage("read", "complete")
    except Exception as e:
        _add_event("read", f"Error: {e}")
        _set_stage("read", "failed")
        return None

    # DECIDE
    _set_stage("decide", "active")
    _add_event("decide", "Evaluating policy...")
    try:
        from .agent import decide
        action, rationale = decide(reading)
        _add_event("decide", f"{action}: {rationale}")
        _set_stage("decide", "complete")
    except Exception as e:
        _add_event("decide", f"Error: {e}")
        _set_stage("decide", "failed")
        return None

    # PAY (only if policy says report_surplus and payee configured)
    pay_result = None
    if config.has_payee and action == "report_surplus":
        _set_stage("pay", "active")
        _add_event("pay", f"Sending USDC payment...")
        try:
            from .pay import fetch_with_payment
            def pay_fn():
                return fetch_with_payment(
                    config.payee_address if config.payee_address.startswith("http")
                    else "http://localhost:4021/data",
                    wallet, w3, usdc_address=config.usdc_address,
                    payee_address=config.payee_address)
            pay_result = pay_fn()
            tx = pay_result.get("proof", {}).get("tx_hash", "unknown")
            _add_event("pay", f"Payment sent — tx {tx[:10]}...{tx[-4:]}", tx)
            with _lock:
                _state["action"] = {
                    "type": "payment",
                    "payment": {
                        "txHash": tx,
                        "block": pay_result.get("proof", {}).get("ts", 0),
                        "amount": "0.01",
                        "token": "USDC",
                        "status": "confirmed",
                    },
                }
            _set_stage("pay", "complete")
        except Exception as e:
            _add_event("pay", f"Payment error: {e}")
            _set_stage("pay", "failed")
    else:
        _set_stage("pay", "active")
        _add_event("pay", f"No payment needed ({action})")
        _set_stage("pay", "complete")

    # ATTEST
    _set_stage("act", "active")
    _add_event("act", "Signing attestation...")
    try:
        result = run_cycle(config, wallet, w3)
        att_data = json.loads(result.attestation_json)
        sig = att_data.get("signature", "")
        valid = att_data.get("valid", False)
        _add_event("act", f"Attestation signed — valid: {valid}")
        with _lock:
            _state["attestation"] = {
                "signature": sig[:80] + "..." if len(sig) > 80 else sig,
                "block": result.block,
                "valid": valid,
                "subgraph": "The Graph",
                "balance": f"{bal:.2f} USDC",
            }
            _state["action"] = {
                "type": "attestation",
                "attestation": _state["attestation"],
            }
        _set_stage("act", "complete")
        _set_stage("attest", "active")
        _add_event("attest", f"valid: {valid} — block {result.block}")
        _set_stage("attest", "complete")
        return {
            "block": result.block,
            "decision": result.decision,
            "paid": result.paid,
            "attestation_valid": valid,
            "balance": bal,
        }
    except Exception as e:
        _add_event("attest", f"Attestation error: {e}")
        _set_stage("attest", "failed")
        return None


def _reset_cycle():
    with _lock:
        _state["cycle"] = {
            "currentStage": "read",
            "stages": [
                {"name": "read", "status": "pending"},
                {"name": "decide", "status": "pending"},
                {"name": "pay", "status": "pending"},
                {"name": "act", "status": "pending"},
                {"name": "attest", "status": "pending"},
            ],
        }


class ASEHandler(SimpleHTTPRequestHandler):
    """Handles API routes and static file serving."""

    dashboard_dir = None  # set at startup

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/api/state":
            self._json_response(_state)
        elif path == "/api/activity":
            self._json_response(_state["activity"])
        elif path == "/api/attestation":
            self._json_response(_state["attestation"])
        elif path == "/api/status":
            self._json_response({"online": _state["online"]})
        elif path == "" or path == "/":
            self._serve_dashboard()
        else:
            # try serving from dashboard dist/
            self._serve_dashboard_file(path)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/api/cycle":
            self._handle_cycle()
        else:
            self.send_error(404)

    def _handle_cycle(self):
        """Run one full cycle in a thread, return immediately."""
        def _run():
            _reset_cycle()
            _add_event("read", "Cycle started — reading chain state...")
            result = run_live_cycle()
            if result:
                _add_event("act", f"Cycle complete — block {result['block']}")
            else:
                _add_event("act", "Cycle completed with errors")

        t = threading.Thread(target=_run, daemon=True)
        t.start()
        self._json_response({"status": "cycle_started"}, code=202)

    def _json_response(self, data, code=200):
        body = json.dumps(data, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_dashboard(self):
        dist = self.dashboard_dir
        if dist and (dist / "index.html").exists():
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            data = (dist / "index.html").read_bytes()
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404, "Dashboard not built. Run: cd dashboard && npm run build")

    def _serve_dashboard_file(self, path):
        dist = self.dashboard_dir
        if not dist:
            self.send_error(404)
            return
        file_path = dist / path.lstrip("/")
        if file_path.exists() and file_path.is_file():
            content_type = "application/octet-stream"
            if path.endswith(".js"):
                content_type = "application/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".html"):
                content_type = "text/html"
            elif path.endswith(".svg"):
                content_type = "image/svg+xml"
            elif path.endswith(".json"):
                content_type = "application/json"

            data = file_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        # quiet logging
        pass


def main():
    import argparse
    parser = argparse.ArgumentParser(description="ASE Dashboard Backend")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()

    # find dashboard dist (server.py lives at src/ase/server.py -> repo root is 3 parents up)
    dashboard_dist = Path(__file__).resolve().parent.parent.parent / "dashboard" / "dist"
    if not dashboard_dist.exists():
        print(f"Warning: dashboard dist not found at {dashboard_dist}")
        print("Build it first: cd dashboard && npm run build")
        dashboard_dist = None

    ASEHandler.dashboard_dir = dashboard_dist

    server = HTTPServer((args.host, args.port), ASEHandler)
    _recover_activity()
    print(f"ASE server running on http://{args.host}:{args.port}")
    print(f"Dashboard: {'serving' if dashboard_dist else 'not built'}")
    print(f"API: /api/state, /api/activity, /api/attestation, /api/status")
    print(f"Trigger cycle: POST /api/cycle")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()


if __name__ == "__main__":
    main()
