"""Unit tests for the ASE spine. No network required - the loop is tested
with injected fakes so the logic is verified even offline."""
import json
import time

import pytest

from ase.agent import decide, run_cycle
from ase.config import Config
from ase.identity import Attestation, make_attestation, sign_attestation, verify_attestation
from ase.read import Reading
from ase.wallet import create_wallet, load_wallet, verify_signature


# ---------------------------------------------------------------- wallet

def test_wallet_roundtrip():
    w = create_wallet()
    assert w.address.startswith("0x") and len(w.address) == 42
    # key roundtrip: load_wallet must reconstruct the exact same account
    w2 = load_wallet(w.account.key.to_0x_hex())
    assert w2.address == w.address


def test_sign_and_verify():
    w = create_wallet()
    sig = w.sign_message("ase test message")
    assert verify_signature("ase test message", sig, w.address)
    assert not verify_signature("ase test message", sig, "0x" + "1" * 40)
    assert not verify_signature("tampered", sig, w.address)


# ---------------------------------------------------------------- identity

def _att(wallet):
    return make_attestation(agent_address=wallet.address, act="test_act",
                            ts=1234567890, block=42,
                            decision="test decision", payload={"x": 1})


def test_attestation_verify_ok():
    w = create_wallet()
    signed = sign_attestation(_att(w), w)
    res = verify_attestation(signed.to_json())
    assert res["valid"] is True
    assert res["agent"] == w.address


def test_attestation_rejects_tamper():
    w = create_wallet()
    signed = sign_attestation(_att(w), w)
    d = json.loads(signed.to_json())
    d["decision"] = "tampered decision"
    res = verify_attestation(json.dumps(d))
    assert res["valid"] is False


def test_attestation_deterministic_message():
    w = create_wallet()
    a1, a2 = _att(w), _att(w)
    assert a1.signing_message() == a2.signing_message()


# ---------------------------------------------------------------- decide

def test_decide_bands():
    low = Reading(block=1, kind="erc20_balance",
                  data={"human": 0.5, "symbol": "USDC"})
    mid = Reading(block=1, kind="erc20_balance",
                  data={"human": 2.5, "symbol": "USDC"})
    high = Reading(block=1, kind="erc20_balance",
                   data={"human": 9.0, "symbol": "USDC"})
    assert decide(low)[0] == "accumulate"
    assert decide(mid)[0] == "hold_and_observe"
    assert decide(high)[0] == "report_surplus"


# ---------------------------------------------------------------- cycle

class _FakeW3:
    pass


def test_run_cycle_no_payee(monkeypatch):
    import ase.agent as agent_mod
    w = create_wallet()
    reading = Reading(block=77, kind="erc20_balance",
                      data={"holder": w.address, "token": "0x" + "a" * 40,
                            "symbol": "USDC", "raw": 2_500_000, "human": 2.5})
    monkeypatch.setattr(agent_mod, "read_chain_state",
                        lambda *a, **k: reading)
    cfg = Config(rpc_url="http://fake", usdc_address="0x" + "a" * 40)
    res = run_cycle(cfg, w, _FakeW3(), pay_fn=None)
    assert res.block == 77
    assert res.decision.startswith("hold_and_observe")
    assert res.paid is False
    att = json.loads(res.attestation_json)
    assert att["signature"]
    # attestation inside the cycle must verify
    assert verify_attestation(res.attestation_json)["valid"] is True


def test_run_cycle_pays_on_surplus(monkeypatch):
    import ase.agent as agent_mod
    w = create_wallet()
    reading = Reading(block=88, kind="erc20_balance",
                      data={"holder": w.address, "token": "0x" + "a" * 40,
                            "symbol": "USDC", "raw": 9_000_000, "human": 9.0})
    monkeypatch.setattr(agent_mod, "read_chain_state",
                        lambda *a, **k: reading)
    calls = []

    def fake_pay():
        calls.append(1)
        return {"paid": True, "tx": "0xdeadbeef"}

    cfg = Config(rpc_url="http://fake", usdc_address="0x" + "a" * 40,
                 payee_address="0x" + "b" * 40)
    res = run_cycle(cfg, w, _FakeW3(), pay_fn=fake_pay)
    assert res.paid is True and calls == [1]
    assert res.payment["tx"] == "0xdeadbeef"


def test_run_cycle_records_chainlink_feed(monkeypatch):
    import ase.agent as agent_mod
    w = create_wallet()
    reading = Reading(block=111, kind="erc20_balance",
                      data={"holder": w.address, "token": "0x" + "a" * 40,
                            "symbol": "USDC", "raw": 3_000_000, "human": 3.0})
    monkeypatch.setattr(agent_mod, "read_chain_state",
                        lambda *a, **k: reading)
    monkeypatch.setattr(
        agent_mod, "read_chainlink_feed",
        lambda *a, **k: Reading(block=111, kind="chainlink_feed",
                                data={"description": "ETH / USD",
                                      "human": 2650.5, "round": 1}))
    cfg = Config(rpc_url="http://fake", usdc_address="0x" + "a" * 40,
                 chainlink_feed="0x" + "c" * 40)
    res = run_cycle(cfg, w, _FakeW3(), pay_fn=None)
    assert res.reading["chainlink"]["human"] == 2650.5
    att = json.loads(res.attestation_json)
    assert "chainlink" in att["payload"]["reading"]


def test_run_cycle_records_subgraph_data(monkeypatch):
    import ase.agent as agent_mod
    w = create_wallet()
    reading = Reading(block=99, kind="erc20_balance",
                      data={"holder": w.address, "token": "0x" + "a" * 40,
                            "symbol": "USDC", "raw": 3_000_000, "human": 3.0})
    monkeypatch.setattr(agent_mod, "read_chain_state",
                        lambda *a, **k: reading)
    monkeypatch.setattr(agent_mod, "subgraph_available", lambda url: True)
    monkeypatch.setattr(
        agent_mod, "read_subgraph",
        lambda url, q, variables=None: {"pools": [{"id": "0xabc", "feeTier": "3000"}]})
    cfg = Config(rpc_url="http://fake", usdc_address="0x" + "a" * 40,
                 subgraph_url="http://fake-graph",
                 subgraph_query="{ pools(first: 1) { id feeTier } }")
    res = run_cycle(cfg, w, _FakeW3(), pay_fn=None)
    assert res.reading.get("subgraph") == "reachable"
    assert res.reading.get("subgraph_data", {}).get("pools")
    att = json.loads(res.attestation_json)
    assert "subgraph_data" in att["payload"]["reading"]


def test_run_cycle_records_subgraph_error(monkeypatch):
    import ase.agent as agent_mod
    w = create_wallet()
    reading = Reading(block=100, kind="erc20_balance",
                      data={"holder": w.address, "token": "0x" + "a" * 40,
                            "symbol": "USDC", "raw": 3_000_000, "human": 3.0})
    monkeypatch.setattr(agent_mod, "read_chain_state",
                        lambda *a, **k: reading)
    monkeypatch.setattr(agent_mod, "subgraph_available", lambda url: True)

    def boom(url, q, variables=None):
        raise RuntimeError("subgraph down")

    monkeypatch.setattr(agent_mod, "read_subgraph", boom)
    cfg = Config(rpc_url="http://fake", usdc_address="0x" + "a" * 40,
                 subgraph_url="http://fake-graph",
                 subgraph_query="{ __typename }")
    res = run_cycle(cfg, w, _FakeW3(), pay_fn=None)
    assert any("subgraph" in e for e in res.errors)
    att = json.loads(res.attestation_json)
    assert "subgraph" in att["payload"]["reading"]
