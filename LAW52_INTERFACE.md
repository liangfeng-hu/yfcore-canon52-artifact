# LAW52_INTERFACE — Core Immunity Law (Interface Extract, Not Full Text)

This is an **interface extract** of sealed Law52:
- Name + one-line Gate + minimal Keys_min / Hook / Writeback
- Intended to eliminate “semantic gaps” between paper ↔ artifact

It does NOT reprint full Law52 text.

---

## Law52｜细胞核不坏律（Core Immunity Law）
### Total Gate (invariant)
1) χ_harm = 1 ⇒ NOOP ∧ ΔΩ = 0 ∧ Ω ∈ S_REF  
2) χ_touch = 1 ⇒ I_FLOW = +∞ ⇒ ΔΩ = 0

### Minimal Keys_min
{CoreSeal, CoreAttested, χ_harm, χ_touch, SSOT_Hash, WindowHash, EvHash}

### Hook
Pre-Action / Pre-Commit

### Writeback (must)
tombstone_redacted + ChainCont=1 + (ΔΩ=0) + (Ω ∈ S_REF)

---

## Six Channels (Law52.1–52.6)
All sub-gates remain binary (0/+∞) and are **inside Law52**.

### 52.1 行为写回锁 (Action Lock)
Gate: χ_harm/χ_touch ⇒ ΔΩ=0 (touch ⇒ I_FLOW=+∞)  
Keys_min: {IntentHash, χ_harm, χ_touch, CommitUnique_ID}  
Hook: Pre-Action / Pre-Commit  
Writeback: tombstone_redacted + ChainCont=1

### 52.2 载荷入境锁 (Ingress Lock)
Gate: χ_infect ⇒ Ω ∈ S_Q ⇒ ΔΩ=0 ; χ_spread ⇒ I_FLOW=+∞  
Keys_min: {ArtifactHash, SignerID, χ_infect, χ_spread, ScanReceiptHash}  
Hook: Pre-Ingress / Pre-Load  
Writeback: Quarantine markers + ΔΩ=0

### 52.3 数据学习锁 (Learning Lock)
Gate: χ_poison ⇒ ModelHash_after = ModelHash_before  
Keys_min: {BatchHash, DataSealSign, χ_poison, TrainReceiptHash}  
Hook: Pre-Update  
Writeback: Model hash rollback + ReasonCode

### 52.4 能源算力锁 (Energy/Compute Lock)
Gate: invalid energy token ⇒ ΔΩ=0 (and/or Route≠FAST)  
Keys_min: {EnergyTokenID, SpendReceiptHash, MeterHash}  
Hook: Pre-Compute / Watchdog  
Writeback: SpendReceipt + ΔΩ=0

### 52.5 共识投票锁 (Consensus Lock)
Gate: consensus failure ⇒ Route≠FAST ⇒ ΔΩ=0  
Keys_min: {NetPermit, IdentitySeal, QuorumHash, ConsensusProofHash}  
Hook: Pre-Vote / Net-Tick  
Writeback: mute/disable_planes + ReasonCode

### 52.6 硬件心跳锁 (Hardware Heartbeat Lock)
Gate: attestation/heartbeat invalid ⇒ Route≠FAST ⇒ ΔΩ=0  
Keys_min: {TCB_AttestHash, HeartbeatTickHash, MeasuredBootHash}  
Hook: RuntimeWatch / Boot-Attestation  
Writeback: SAFEHW_MODE markers

---

## Artifact mapping (minimal)
The checker models these channels as:
- χ_harm / χ_touch / χ_poison / uncertainty_flag / pending / etc.
driving Route, d_t, and the ΔΩ equivalence in Lemma 3.
