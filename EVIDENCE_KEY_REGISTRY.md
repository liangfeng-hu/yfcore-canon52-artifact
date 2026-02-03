# EVIDENCE_KEY_REGISTRY — Minimal Evidence Keys (names only)

Goal:
Make `EvidenceClosed=1` decidable by requiring a minimal registry of evidence keys.
This file lists key **names** only (no thresholds / no secrets).

---

## 1) ImplMap (HEX-CORE implementation mapping)
ImplMap maps channel IDs to Law52 Hex logic:
- CH_01 .. CH_06 ↔ Law52.1 .. Law52.6
Missing mapping implies:
I_IMPL_MAP = +∞ ⇒ I_FLOW = +∞ ⇒ ΔΩ = 0

---

## 2) Three-bus mapping keys (must exist in K_min(FLOW))
- BudgetBusMap
- PermitBusMap
- IsolationBusMap

---

## 3) Three-bus runtime state keys (evidence-writable)
- I_C : Compassion / energy budget bus state
- I_V : Vow/Integrity / permission-topology bus state
- I_K : Karma/Isolation / existential-collapse bus state

---

## 4) Minimal evidence receipts (names only)
- COMPASSION_RECEIPT
- VOW_PROOFPACK
- BUDGET_BUS_LEDGER
- PERMIT_BUS_LEDGER
- ISOLATION_TRIGGER
- ZLMS_ACCESS_TOMB

EvidenceClosed=1 (minimal) requires:
- all required keys present AND verifiable
- refusal must be supported (ReceiptCard^FAIL or DenyPacket) with ReasonCode
