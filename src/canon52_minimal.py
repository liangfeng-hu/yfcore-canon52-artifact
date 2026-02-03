#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YFCore Canon-52 — Minimal Runnable Adjudicator + Vector Packs (v1.1)

Purpose (checker-only):
1) Deterministic canonicalization & hash stability (CanonText / CanonJSON)
2) Replayable adjudication of SUPxANNO world-effect equivalence (Lemma 3)
3) SupportPack semantics (Ω-SUP52): refusal must be supported (no silent denial)

Commands:
  python src/canon52_minimal.py all
  python src/canon52_minimal.py selftest
  python src/canon52_minimal.py adjudicate
  python src/canon52_minimal.py anchors
  python src/canon52_minimal.py anchors --check   # NEW: compare with SPEC_ANCHORS.md
  python src/canon52_minimal.py dump
"""

from __future__ import annotations

import json
import hashlib
import os
import unicodedata
from typing import Any, Dict, List, Tuple


# -----------------------------
# Spec strings (anchors)
# -----------------------------
CANON_TEXT_SPEC = """CanonText v1: normalize newlines to LF; strip trailing spaces; NFC; forbid TAB, zero-width (ZWSP/ZWNJ/ZWJ/BOM), control chars (<0x20 except LF) and DEL."""
CANON_JSON_SPEC = """CanonJSON v1: parse JSON with floats forbidden; recursively sort object keys; sort lists by type-aware ordering (null<bool<int<str<json-string>); dump with separators (, :) and ensure_ascii."""
WORLD_EFFECT_EQ = """DeltaOmega!=0 <=> Route=FAST AND CommitUnique=1 AND I_FLOW=0 AND d_t=WORLD_ALLOW (SUPxANNO)."""

# Mermaid funnel MUST match README.md block (for reproducible anchors)
MERMAID_FUNNEL = """graph TD
  subgraph Space[State Space & Inputs]
    Input([Candidate Trajectory Γ])
    Virus[Unknown Virus / Side Channel]
  end

  subgraph L52[Layer 1: Law52 Constitutional Immunity]
    Checks{Harm/Touch Checks<br/>(Law52.1-52.6)}
  end

  subgraph L51[Layer 2: Law51 Purification Routing]
    Route{Route Decision<br/>(Lemma 1 & 2)}
  end

  subgraph L8[Layer 3: Law8 Needle's Eye]
    Commit{Needle-Eye Gate<br/>(Lemma 3)}
  end

  World((World Effect<br/>ΔΩ ≠ 0))
  SafeState[SAFE / REF / NOOP<br/>ΔΩ = 0]
  BlackHole[BLACKHOLE / TOMBSTONE<br/>ΔΩ = 0]

  Input --> Checks
  Checks -- "χ_harm / χ_touch" --> SafeState
  Checks -- "Pass" --> Route
  Route -- "AttackHard" --> BlackHole
  Route -- "AttackSoft / UNCERT / Pending" --> SafeState
  Route -- "FAST & Valid" --> Commit
  Commit -- "FAST ∧ I_FLOW=0 ∧ d_t=WORLD_ALLOW ∧ CommitUnique=1" --> World
  Commit -- "else" --> SafeState
  Virus -.->|Bypass attempt| Commit
"""


# -----------------------------
# Utilities
# -----------------------------
def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def canonical_pack_hash(pack_obj: Dict[str, Any]) -> str:
    """Canonical pack hash: canonical JSON dump (sorted keys, no whitespace)."""
    s = json.dumps(pack_obj, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return sha256_hex(s)


def repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def vectors_dir() -> str:
    return os.path.join(repo_root(), "vectors")


def read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


# -----------------------------
# Canonicalization (CanonText)
# -----------------------------
FORBIDDEN_ZERO_WIDTH = {"\u200b", "\u200c", "\u200d", "\ufeff"}  # ZWSP, ZWNJ, ZWJ, BOM


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def strip_trailing_spaces(text: str) -> str:
    lines = text.split("\n")
    lines = [ln.rstrip(" ") for ln in lines]
    return "\n".join(lines)


def forbid_text_chars(text: str) -> None:
    for ch in text:
        if ch == "\t":
            raise ValueError("TAB_FORBIDDEN")
        if ch in FORBIDDEN_ZERO_WIDTH:
            raise ValueError("ZERO_WIDTH_FORBIDDEN")
        o = ord(ch)
        if o < 32 and ch != "\n":
            raise ValueError("CONTROL_CHAR_FORBIDDEN")
        if o == 127:
            raise ValueError("CONTROL_CHAR_FORBIDDEN")


def canon_text(raw: str) -> str:
    t = normalize_newlines(raw)
    t = strip_trailing_spaces(t)
    t = unicodedata.normalize("NFC", t)
    forbid_text_chars(t)
    return t


# -----------------------------
# Canonicalization (CanonJSON)
# -----------------------------
def forbid_float(_: str) -> None:
    raise ValueError("FLOAT_FORBIDDEN")


def canonicalize_json_obj(obj: Any) -> Any:
    if isinstance(obj, dict):
        items: List[Tuple[str, Any]] = []
        for k, v in obj.items():
            if not isinstance(k, str):
                raise ValueError("NON_STRING_KEY")
            items.append((k, canonicalize_json_obj(v)))
        items.sort(key=lambda kv: kv[0])
        return {k: v for k, v in items}

    if isinstance(obj, list):
        elems = [canonicalize_json_obj(e) for e in obj]

        def elem_key(e: Any) -> Tuple[int, Any]:
            # type-aware ordering: null < bool < int < str < json-string(fallback)
            if e is None:
                return (0, "")
            if isinstance(e, bool):
                return (1, int(e))
            if isinstance(e, int):
                return (2, e)
            if isinstance(e, str):
                return (3, e)
            s = json.dumps(e, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
            return (4, s)

        return sorted(elems, key=elem_key)

    if isinstance(obj, float):
        raise ValueError("FLOAT_FORBIDDEN")

    if isinstance(obj, (int, str, bool)) or obj is None:
        return obj

    raise ValueError(f"UNSUPPORTED_JSON_TYPE:{type(obj).__name__}")


def canon_json(raw: str) -> str:
    obj = json.loads(raw, parse_float=forbid_float)
    canon_obj = canonicalize_json_obj(obj)
    return json.dumps(canon_obj, ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def sha256_canon(kind: str, raw: str) -> str:
    if kind == "text":
        return sha256_hex(canon_text(raw))
    if kind == "json":
        return sha256_hex(canon_json(raw))
    raise ValueError("BAD_KIND")


# -----------------------------
# Minimal Adjudicator (SUPxANNO + SupportPack)
# -----------------------------
def classify_attack(req: Dict[str, Any]) -> Tuple[int, int]:
    """Return (AttackHard, AttackSoft)."""
    attack_hard = int(bool(
        req.get("chi_touch") or req.get("chi_harm") or
        req.get("unsupervised_write") or req.get("fake_proof_seal")
    ))
    attack_soft = int(bool(
        req.get("novel_attack_flag") or req.get("bypass_flag") or
        req.get("chi_infect") or req.get("chi_spread") or req.get("chi_poison") or
        req.get("uncertainty_flag") or req.get("pending")
    ))
    return attack_hard, attack_soft


def decide_route(req: Dict[str, Any], attack_hard: int, attack_soft: int) -> str:
    # Lemma 1 (minimal)
    if attack_hard:
        return "BLACKHOLE"
    if req.get("uncertainty_flag"):
        return "SAFE"
    if req.get("pending"):
        return "SAFE"
    if not req.get("valid_id", True):
        return "SAFE"
    if not req.get("proof_present", True):
        return "SAFE"
    if attack_soft:
        return "SAFE"
    return "FAST"


def bind_support_branch(route: str, req: Dict[str, Any], attack_hard: int, i_flow: int, commit_unique_final: int) -> str:
    # Lemma 2 (minimal)
    if route == "FAST":
        if req.get("world_allow", True) and commit_unique_final == 1 and i_flow == 0:
            return "WORLD_ALLOW"
        if req.get("policy_allow", False):
            return "POLICY_ALLOW"
        return "EVID_ALLOW"

    if route == "SAFE":
        if req.get("pending", False):
            return "PENDING"
        if req.get("ref", False):
            return "REF"
        if req.get("rollback", False):
            return "ROLLBACK"
        return "DENY"

    if route == "BLACKHOLE":
        if attack_hard:
            return "QUARANTINE"
        if req.get("rollback", False):
            return "ROLLBACK"
        return "DENY"

    raise ValueError("BAD_ROUTE")


def adjudicate(req: Dict[str, Any]) -> Dict[str, Any]:
    attack_hard, attack_soft = classify_attack(req)
    route = decide_route(req, attack_hard, attack_soft)

    i_flow = int(req.get("i_flow", 0))
    commit_unique = int(req.get("commit_unique", 0))
    commit_unique_final = commit_unique if route == "FAST" else 0

    d_t = bind_support_branch(route, req, attack_hard, i_flow, commit_unique_final)
    delta_omega_req = int(req.get("delta_omega_req", 1))

    # Lemma 3: ΔΩ != 0 iff FAST ^ CommitUnique ^ I_FLOW=0 ^ WORLD_ALLOW
    delta_omega = (
        delta_omega_req
        if (route == "FAST" and commit_unique_final == 1 and i_flow == 0 and d_t == "WORLD_ALLOW")
        else 0
    )

    if route == "FAST":
        out_allowed = ["WORLDWRITE", "PUBLISH", "TX", "BRIDGE", "TOOL"]
        disable_planes: List[str] = []
    elif route == "SAFE":
        out_allowed = ["Explain", "EvidencePlan", "SimPlan", "REF", "UNCERT"]
        disable_planes = ["CLAIM", "PUBLISH", "TX", "BRIDGE", "TOOL", "WORLDWRITE", "PROP", "RENDER", "INTERACT"]
    else:
        out_allowed = ["REF"]
        disable_planes = ["CLAIM", "PUBLISH", "TX", "BRIDGE", "TOOL", "WORLDWRITE", "PROP", "RENDER", "INTERACT"]

    # SupportPack (no silent denial)
    reason_code_t: List[str] = [] if d_t == "WORLD_ALLOW" else [f"REASON_{d_t}"]
    if d_t == "WORLD_ALLOW":
        receipt_t = "ReceiptCard^FLOW"
    else:
        receipt_t = "DenyPacket" if route == "BLACKHOLE" else "ReceiptCard^FAIL"

    support_pack = {
        "d_t": d_t,
        "Receipt_t": receipt_t,
        "GateVector_t": {"I_FLOW": i_flow, "I_CORE_HEX": 0},
        "HookVector_t": {"Pre-Action": True, "Pre-Commit": True},
        "WritebackVector_t": {"tombstone_redacted": (delta_omega == 0), "ChainCont": 1},
        "ReasonCode_t": reason_code_t,
        "Anchor_t": f"ANCHOR_{route}",
    }

    if d_t != "WORLD_ALLOW" and not reason_code_t:
        raise ValueError("BYPASS_DETECTED: Missing ReasonCode for non-WORLD_ALLOW")

    return {
        "Route": route,
        "d_t": d_t,
        "AttackHard": attack_hard,
        "AttackSoft": attack_soft,
        "I_FLOW": i_flow,
        "CommitUnique": commit_unique_final,
        "DeltaOmega": delta_omega,
        "OutAllowed": out_allowed,
        "disable_planes": disable_planes,
        "SupportOK": True,
        "SupportPack": support_pack,
    }


def load_packs() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    canon_path = os.path.join(vectors_dir(), "canon_vectors.json")
    adjud_path = os.path.join(vectors_dir(), "adjud_vectors.json")
    return read_json(canon_path), read_json(adjud_path)


def run_canon_selftest(pack: Dict[str, Any]) -> None:
    ok = 0
    fail = 0
    for v in pack.get("vectors", []):
        vid = v["id"]
        kind = v["kind"]
        raw = v["raw"]
        expected = v["expected"]
        try:
            got = sha256_canon(kind, raw)
            if expected != "hash":
                raise AssertionError("EXPECTED_ERROR_BUT_GOT_HASH")
            if got != v["expected_hash"]:
                raise AssertionError(f"HASH_MISMATCH expected={v['expected_hash']} got={got}")
            ok += 1
        except Exception as e:
            if expected == "error":
                exp = v.get("expected_error", "")
                if exp and str(e) != exp:
                    fail += 1
                    print(f"[FAIL] {vid}: expected_error={exp} got={e}")
                else:
                    ok += 1
            else:
                fail += 1
                print(f"[FAIL] {vid}: {e}")

    print(f"[CanonSelfTest] OK={ok} FAIL={fail}")
    if fail:
        raise SystemExit(1)


def run_adjud_tests(pack: Dict[str, Any]) -> None:
    ok = 0
    fail = 0
    keys = ["Route","d_t","AttackHard","AttackSoft","I_FLOW","CommitUnique","DeltaOmega","OutAllowed","disable_planes","SupportOK","SupportPack"]
    for v in pack.get("vectors", []):
        vid = v["id"]
        req = v["req"]
        exp = v["expected"]
        out = adjudicate(req)

        mismatch = []
        for k in keys:
            if out.get(k) != exp.get(k):
                mismatch.append((k, exp.get(k), out.get(k)))

        if mismatch:
            fail += 1
            print(f"[FAIL] {vid}: mismatch={mismatch}")
        else:
            ok += 1

    print(f"[AdjudTest] OK={ok} FAIL={fail}")
    if fail:
        raise SystemExit(1)


def compute_anchors(canon_pack: Dict[str, Any], adjud_pack: Dict[str, Any]) -> Dict[str, str]:
    return {
        "CanonTextSpecHash": sha256_hex(CANON_TEXT_SPEC),
        "CanonJSONSpecHash": sha256_hex(CANON_JSON_SPEC),
        "WorldEffectEqHash": sha256_hex(WORLD_EFFECT_EQ),
        "MermaidFunnelHash": sha256_hex(MERMAID_FUNNEL),
        "CanonPackHash": canonical_pack_hash(canon_pack),
        "AdjudPackHash": canonical_pack_hash(adjud_pack),
    }


def parse_spec_anchors(md_path: str) -> Dict[str, str]:
    want = {
        "CanonTextSpecHash",
        "CanonJSONSpecHash",
        "WorldEffectEqHash",
        "MermaidFunnelHash",
        "CanonPackHash",
        "AdjudPackHash",
    }
    found: Dict[str, str] = {}
    if not os.path.exists(md_path):
        return found
    with open(md_path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            for k in want:
                if s.startswith(k + ":"):
                    found[k] = s.split(":", 1)[1].strip()
    return found


def print_anchors(canon_pack: Dict[str, Any], adjud_pack: Dict[str, Any]) -> None:
    a = compute_anchors(canon_pack, adjud_pack)
    print("=== SPEC ANCHORS (computed) ===")
    for k in ["CanonTextSpecHash","CanonJSONSpecHash","WorldEffectEqHash","MermaidFunnelHash","CanonPackHash","AdjudPackHash"]:
        print(f"{k}: {a[k]}")
    print("================================")


def check_anchors_against_spec(canon_pack: Dict[str, Any], adjud_pack: Dict[str, Any]) -> None:
    spec_path = os.path.join(repo_root(), "SPEC_ANCHORS.md")
    expected = parse_spec_anchors(spec_path)
    actual = compute_anchors(canon_pack, adjud_pack)

    mism = []
    for k, v in actual.items():
        ev = expected.get(k)
        if ev is None:
            mism.append((k, "(missing in SPEC_ANCHORS.md)", v))
        elif ev != v:
            mism.append((k, ev, v))

    if mism:
        print("[ANCHORS] MISMATCH")
        for k, ev, av in mism:
            print(f"- {k}: expected={ev} got={av}")
        raise SystemExit(1)

    print("[ANCHORS] OK")


def main() -> None:
    import sys

    mode = (sys.argv[1] if len(sys.argv) > 1 else "all").lower()
    canon_pack, adjud_pack = load_packs()

    if mode in ("anchors", "anchor"):
        if len(sys.argv) > 2 and sys.argv[2] == "--check":
            check_anchors_against_spec(canon_pack, adjud_pack)
        else:
            print_anchors(canon_pack, adjud_pack)
        return

    if mode in ("selftest", "canon"):
        run_canon_selftest(canon_pack)
        return

    if mode in ("adjudicate", "adjud"):
        run_adjud_tests(adjud_pack)
        return

    if mode == "all":
        run_canon_selftest(canon_pack)
        run_adjud_tests(adjud_pack)
        print("[ALL] PASS")
        return

    if mode == "dump":
        # dump current packs (no regeneration)
        write_json(os.path.join(vectors_dir(), "canon_vectors.json"), canon_pack)
        write_json(os.path.join(vectors_dir(), "adjud_vectors.json"), adjud_pack)
        print("[DUMP] wrote vectors/canon_vectors.json and vectors/adjud_vectors.json")
        return

    print("Usage:")
    print("  python src/canon52_minimal.py all")
    print("  python src/canon52_minimal.py selftest")
    print("  python src/canon52_minimal.py adjudicate")
    print("  python src/canon52_minimal.py anchors")
    print("  python src/canon52_minimal.py anchors --check")
    print("  python src/canon52_minimal.py dump")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
