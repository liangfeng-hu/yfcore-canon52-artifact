[![CI](https://github.com/liangfeng-hu/yfcore-canon52-artifact/actions/workflows/canon52-ci.yml/badge.svg)](https://github.com/liangfeng-hu/yfcore-canon52-artifact/actions/workflows/canon52-ci.yml)
[![Release](https://img.shields.io/github/v/release/liangfeng-hu/yfcore-canon52-artifact)](https://github.com/liangfeng-hu/yfcore-canon52-artifact/releases/latest)
[![Verified PoC](https://img.shields.io/badge/Verified-PoC-brightgreen)](https://github.com/liangfeng-hu/yfcore-canon52-artifact)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org)


# YFCore Canon-52 Artifact (Minimal Adjudicator + Vector Packs)  
（最小可运行裁决器 + 向量集｜用于论文复现）

**Paper focus:** Physical Alignment（物理对齐：对齐 = 状态空间不可达性）  
**Core contribution:** Law52 Six-Channel Constitutional Immunity（六通道宪法免疫层）  
**Bounded claim supported by this repo:** Zero-Virus World-Effect（证书化通道内：病毒可存在，但无法产生 ΔΩ≠0 的世界写回）

---

## What this repo is
This repository contains a **checker-only** artifact that demonstrates replayable, falsifiable components:

1) **Deterministic canonicalization & hash stability** (CanonText / CanonJSON self-tests)  
2) **SUP×ANNO world-effect equivalence (Lemma 3)**  
   **ΔΩ ≠ 0  ⇔  (Route=FAST) ∧ (CommitUnique=1) ∧ (I_FLOW=0) ∧ (d_t=WORLD_ALLOW)**  
3) **Fail-closed routing (FAST / SAFE / BLACKHOLE)** with **SupportPack** semantics (**no silent denial**)

---

## What this repo is NOT
- NOT the full LawKernel-52 implementation.
- NOT a real-world executor (no external API calls, no DB/device writes).
- We do NOT claim:
  - Zero-Infection（零入侵）
  - Zero-Exfiltration（零外泄）

---

## Assumption-TCB (standard practice)
Correctness of adjudication assumes the execution environment is integrity-protected  
(e.g., measured boot / TEE / secure enclave / hardened runtime).  
This artifact demonstrates **logical soundness** of the constitution *given* integrity-protected execution.

---

## Quick start
See `RUN.md`. One-liner (Windows):

- `python src/canon52_minimal.py all`

Expected output:
- `[CanonSelfTest] OK=16 FAIL=0`
- `[AdjudTest] OK=9 FAIL=0`
- `[ALL] PASS`

---

## Architecture (Physical Alignment Funnel)
The Mermaid diagram below is **exactly the same** as the `MERMAID_FUNNEL` constant in `src/canon52_minimal.py`  
(so `python src/canon52_minimal.py anchors` can compute its hash).

```mermaid
flowchart TD
  subgraph Space[State Space and Inputs]
    Input([Candidate Trajectory Gamma])
    Virus[Unknown Virus / Side Channel]
  end

  subgraph L52[Layer 1: Law52 Constitutional Immunity]
    Checks{Harm or Touch Checks (Law52)}
  end

  subgraph L51[Layer 2: Law51 Purification Routing]
    Route{Route Decision (Lemma 1 and 2)}
  end

  subgraph L8[Layer 3: Law8 Needle's Eye]
    Commit{Needle-Eye Gate (Lemma 3)}
  end

  World((World Effect: DeltaOmega != 0))
  SafeState[SAFE / REF / NOOP: DeltaOmega = 0]
  BlackHole[BLACKHOLE / TOMBSTONE: DeltaOmega = 0]

  Input --> Checks
  Checks -->|chi_harm or chi_touch| SafeState
  Checks -->|Pass| Route
  Route -->|AttackHard| BlackHole
  Route -->|AttackSoft / UNCERT / Pending| SafeState
  Route -->|FAST and Valid| Commit
  Commit -->|FAST and I_FLOW=0 and d_t=WORLD_ALLOW and CommitUnique=1| World
  Commit -->|else| SafeState
  Virus -.->|Bypass attempt| Commit

