#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YFCore Canon-52 - Minimal Runnable Adjudicator + Vector Packs (v1.1)
Checker-only, zero-deps, reproducible.
"""

import json
import hashlib
import unicodedata
from typing import Any

# ====================== Spec Anchors ======================
CANON_TEXT_SPEC = """CanonText v1: NFC; strip leading/trailing whitespace; collapse internal whitespace to single space; lowercase; remove control chars except LF; forbid TAB, ZWSP/ZWNJ/ZWJ/BOM."""
CANON_JSON_SPEC = """CanonJSON v1: parse JSON (floats forbidden); recursively sort object keys; sort arrays by type-aware lexical order; compact output (no whitespace)."""
MERMAID_FUNNEL = """graph TD
    A[Raw Input] --> B{Canonize}
    B --> C{Adjudicate Route}
    C --> D[FAST / SAFE / BLACKHOLE / POLICY_ALLOW]"""

# ====================== Load Vectors ======================
def load_vectors():
    with open("vectors/canon_vectors.json", encoding="utf-8") as f:
        canon = json.load(f)
    with open("vectors/adjud_vectors.json", encoding="utf-8") as f:
        adjud = json.load(f)
    return canon, adjud

CANON_VECTORS, ADJUD_VECTORS = load_vectors()

# ====================== Canon Functions ======================
def canon_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = s.strip()
    s = " ".join(s.split())          # collapse whitespace
    s = s.lower()
    # remove forbidden chars
    s = "".join(c for c in s if c >= " " or c == "\n")
    s = s.replace("\t", " ")
    return s

def canon_json(obj: Any) -> str:
    if isinstance(obj, (dict, list)):
        return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)

# ====================== Adjudicate ======================
def adjudicate(route: str, commit_unique: int, i_flow: int, dt: str) -> bool:
    # Lemma 3: ΔΩ != 0 <=> FAST ∧ CommitUnique=1 ∧ I_FLOW=0 ∧ d_t=WORLD_ALLOW
    if route == "FAST" and commit_unique == 1 and i_flow == 0 and dt == "WORLD_ALLOW":
        return True
    if route in ("SAFE", "BLACKHOLE", "POLICY_ALLOW"):
        return False
    return False

# ====================== Tests ======================
def run_canon_test():
    ok = fail = 0
    for case in CANON_VECTORS:
        try:
            if case["type"] == "text":
                result = canon_text(case["input"])
            else:
                result = canon_json(case["input"])
            if result == case["expected"]:
                ok += 1
            else:
                fail += 1
        except:
            fail += 1
    print(f"[CanonSelfTest] OK={ok} FAIL={fail}")
    return fail == 0

def run_adjud_test():
    ok = fail = 0
    for case in ADJUD_VECTORS:
        try:
            res = adjudicate(**case["input"])
            if res == case["expected"]:
                ok += 1
            else:
                fail += 1
        except:
            fail += 1
    print(f"[AdjudTest]   OK={ok} FAIL={fail}")
    return fail == 0

# ====================== Anchors ======================
def compute_anchors():
    h = lambda x: hashlib.sha256(x.encode()).hexdigest()
    print("CanonTextSpecHash:    ", h(CANON_TEXT_SPEC))
    print("CanonJSONSpecHash:    ", h(CANON_JSON_SPEC))
    print("WorldEffectEqHash:    ", h("SUPxANNO_WORLD_EFFECT_EQ"))
    print("MermaidFunnelHash:    ", h(MERMAID_FUNNEL))
    print("CanonPackHash:        ", h(json.dumps(CANON_VECTORS, sort_keys=True)))
    print("AdjudPackHash:        ", h(json.dumps(ADJUD_VECTORS, sort_keys=True)))

# ====================== CLI ======================
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    import sys
    if cmd == "all":
        if run_canon_test() and run_adjud_test():
            print("[ALL] PASS")
            sys.exit(0)
        else:
            print("[ALL] FAIL")
            sys.exit(1)
    elif cmd == "anchors":
        compute_anchors()
    else:
        print("Usage: python src/canon52_minimal.py all | anchors")
        sys.exit(1)
