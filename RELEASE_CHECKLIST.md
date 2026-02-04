# ✅ RELEASE_CHECKLIST – Canon-52 Artifact (Reviewer-Proof)

This checklist ensures:
- zero dependencies
- anchors match on your machine
- drift is detected
- ready for GitHub release + Zenodo DOI

## A) Pre-release (must do)

- [x] 1) Run full tests:  
  `python src/canon52_minimal.py all`  
  Must show `[ALL] PASS`.

- [x] 2) Refresh anchors (CRITICAL):  
  `python src/canon52_minimal.py anchors`  
  Copy the printed hashes into `SPEC_ANCHORS.md` (replace old values).

- [x] 3) Commit & tag:  
  commit message: `artifact v1.1.0: checker + vectors + supportpack + anchors`  
  tag: `v1.1.0`

## B) GitHub release (recommended)

- [x] Create a release from tag `v1.1.0`
- [x] Paste the 6 hashes from `SPEC_ANCHORS.md` into release notes.

## C) Zenodo DOI (fast public timestamp)

- [x] Zip the repo (checker-only; no world executor).
- [x] Zenodo → New upload → Get a DOI now! → upload paper PDF + artifact.zip → Publish
- [x] Update `CITATION.md` with DOI and URL.

## D) Post-release sanity check

- [x] Clone into a new folder and rerun:
  - `python src/canon52_minimal.py all`
  - `python src/canon52_minimal.py anchors`
- [x] Ensure hashes match `SPEC_ANCHORS.md`.
