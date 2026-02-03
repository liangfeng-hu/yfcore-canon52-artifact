# Open Science & Artifact Appendix

## A. Artifact Identification
- **Title:** YFCore Canon-52 Artifact: Minimal Adjudicator + Vector Packs
- **Authors:** Feng Hu (YFCore Technology Limited)
- **Artifact Stable URL / DOI:** [INSERT_ZENODO_DOI_HERE]
- **Software License:** MIT License
- **Status:** Available, Functional, Reproducible

## B. Artifact Description
This artifact provides a minimal, runnable reference implementation of the **checker-level adjudication logic** described in the paper.

### B.1 Claims Supported (bounded)
The artifact supports the following replayable claims:

1) **Lemma 1 (ANNO-Route Consistency, minimal):** deterministic routing based on AttackHard/AttackSoft and basic prerequisites.
2) **Lemma 2 (SUP-Branch Binding, minimal):** strict enumeration of support branches d_t per Route.
3) **Lemma 3 (World-Effect Equivalence, SUP×ANNO):**
   ΔΩ ≠ 0  ⇔  (Route=FAST) ∧ (CommitUnique=1) ∧ (I_FLOW=0) ∧ (d_t=WORLD_ALLOW)
4) **Zero-Virus World-Effect (bounded):** even with malicious inputs (e.g., chi_touch=1), the checker fail-closes to ΔΩ=0 unless Lemma 3 conditions hold.

### B.2 Contents
- `src/canon52_minimal.py`: reference checker (Python stdlib only)
- `vectors/canon_vectors.json`: canonicalization vectors (drift detection)
- `vectors/adjud_vectors.json`: adjudication vectors (Route/d_t/ΔΩ equivalence + SupportPack)
- `SPEC_ANCHORS.md`: cryptographic hashes to ensure reproducibility
- `SUPPORTPACK_SCHEMA.md`: refusal must be supported (no silent denial)

## C. Setup & Installation
**Hardware/OS:** Any platform supporting Python 3.10+ (Windows, Linux, macOS).  
**Dependencies:** None (Standard Library only).

Run:
- `python src/canon52_minimal.py all`

## D. Evaluation Instructions
### D.1 Functional Test
- `python src/canon52_minimal.py all`
Expected output: `[ALL] PASS`

### D.2 Verify anchors (recommended)
- `python src/canon52_minimal.py anchors`
Compare output with `SPEC_ANCHORS.md`.

## E. Notes on TCB
This artifact runs in checker mode and does not execute real-world effects.
Correctness assumes integrity-protected execution environment (TCB), as discussed in the paper’s threat model.
