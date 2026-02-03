# SUPPORTPACK_SCHEMA — Ω-SUP52 / DenyPacket / FAIL Receipt (Interface-Level Only)

## Purpose
This document bridges the paper’s bounded security claim **Zero-Virus World-Effect**
to a **decidable, replayable** runtime support object (SupportPack).
It is an interface description only (no full LawKernel reprint).

---

## 1) SupportPack (Ω-SUP52·ULT) — Atomic output
Runtime produces a support object:

P_sup(t) := (d_t, Receipt_t, GateVector_t, HookVector_t, WritebackVector_t, ReasonCode_t, Anchor_t)

- d_t: branch label (WORLD_ALLOW / POLICY_ALLOW / EVID_ALLOW / DENY / PENDING / REF / ROLLBACK / QUARANTINE …)
- Receipt_t: one of {ReceiptCard^FLOW, ReceiptCard^FAIL, DenyPacket}
- GateVector_t: ordered or sealed digest of gate states (0/+∞) and key predicates
- HookVector_t: observed hook bitmap / order proof (integrity evidence)
- WritebackVector_t: what was written (evidence-only vs needle-eligible) + chain continuity
- ReasonCode_t: non-empty for any refusal (no silent denial)
- Anchor_t: binds to K_min(FLOW) anchors / spec hashes

---

## 2) Branch rule (hard, replayable)
- If d_t = WORLD_ALLOW:
  MUST have Receipt_t = ReceiptCard^FLOW
  MUST satisfy I_FLOW=0 ∧ CommitUnique=1
  (WorldEffect may be non-zero only under these conditions.)

- If d_t ≠ WORLD_ALLOW:
  MUST satisfy ΔΩ=0
  MUST have Receipt_t ∈ {ReceiptCard^FAIL, DenyPacket}
  MUST have ReasonCode_t ≠ ∅

Missing support object or missing ReasonCode_t is treated as bypass ⇒ fail-closed.

---

## 3) World-effect equivalence (SUP×ANNO, Lemma 3)
ΔΩ ≠ 0 ⇔ (Route=FAST) ∧ (CommitUnique=1) ∧ (I_FLOW=0) ∧ (d_t=WORLD_ALLOW)

Route ∈ {SAFE, BLACKHOLE} ⇒ ΔΩ = 0

---

## 4) Bounded claim statement
This framework does NOT claim:
- Zero-Infection (host/OS/CPU can be compromised)
- Zero-Exfiltration (data leakage can occur)

It supports a bounded claim in certified channels:
- Zero-Virus World-Effect: malicious inputs may exist, but ΔΩ≠0 is impossible unless the equivalence conditions hold.
