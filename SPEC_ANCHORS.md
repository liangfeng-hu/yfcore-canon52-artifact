# SPEC_ANCHORS — Sealed Anchors (No thresholds, no secrets)

本文件只记录**非敏感、可复算**的锚点（hash / 版本号），用于绑定：
- 规范化规则（CanonText / CanonJSON）
- SUP×ANNO 世界效应等价式（Lemma 3）
- Mermaid 漏斗图（物理对齐漏斗）
- 两个向量包（canon_vectors / adjud_vectors）

刻意不包含：
- 阈值族/金库/密钥
- 对抗细节/利用细节
- 任何世界写回执行器

---

## 1) Artifact identity
- Artifact: YFCore Canon-52 Artifact (checker-only)
- Version: v1.1
- Build mode: checker-only (no world executor)
- Git commit (optional): <GIT_COMMIT_SHA>
- Zenodo DOI (optional): <DOI>

---

## 2) Canonicalization spec anchors
CanonTextSpecHash: c5b6e333e9220d2e287c7140a4db6bb9e90c41149b50ac19f0396cb6fc23b4d0
CanonJSONSpecHash: 90cea96de20ebeae7561b3107315531e134b64e84fbdbe09656dad82c4a2181a

---

## 3) SUP×ANNO world-effect equivalence anchor
Equivalence ID: SUPxANNO_WORLD_EFFECT_EQ
WorldEffectEqHash: c0ce3b1d74fe6f21dabd1c15277469465a1b93534e3b0d6bec33b4ba5dbf0729

Statement:
ΔΩ ≠ 0  ⇔  (Route=FAST) ∧ (CommitUnique=1) ∧ (I_FLOW=0) ∧ (d_t=WORLD_ALLOW)

---

## 4) Mermaid funnel diagram anchor
MermaidFunnelHash: e79c1d30931da64779f18bdb57ccfc27a9b7f4b58353944e5b7652c995c57e1b
Source: `MERMAID_FUNNEL` constant in `src/canon52_minimal.py` (and identical block in README.md)

---

## 5) Vector pack anchors (canonical JSON pack hash)
CanonPackHash: 5f5cc7cc29eb4f27a9c2e3b423dfcfd1ffdae81a00e6cf290ef6a51b4d44b58a
AdjudPackHash: 4096cdc774c9a77193a10e5ea858f88c970efae07cf977ba124e294c0ab188c1

Files:
- vectors/canon_vectors.json
- vectors/adjud_vectors.json

---

## 6) Assumption-TCB (non-secret)
Correctness assumes integrity-protected execution (TEE / measured boot / hardened runtime).
This artifact demonstrates logical soundness, not physical host compromise resistance.

---

## 7) How to refresh anchors (MANDATORY after edits)
每次你改动以下任意项：
- src/canon52_minimal.py（spec字符串 / 漏斗图 / 裁决逻辑）
- vectors/*.json（向量增删改）
都必须执行：

1) `python src/canon52_minimal.py all`（必须 PASS）
2) `python src/canon52_minimal.py anchors`
3) 用屏幕输出覆盖更新本文件里的 6 个 hash
