# 5.2 Open Questions

> 🎯 *"Turn 'what I failed to understand' into actionable next steps."*

## Priority legend

| Priority | Meaning |
|---|---|
| P0 | without resolving it, the core chain cannot be fully reproduced |
| P1 | affects version comparison or boundary judgment |
| P2 | supplementary, can be deferred |

## P0: Core chain gaps

### Q1. Which component do the "eight branches" belong to?

- **Location**: end of 4.3 / 4.4
- **Observation**: the earlier text says field13 has 16 branches, `slot & 15`, and 20B output; this passage says 8 branches, `slot & 7`, and forward 19B → 32B MAC.
- **Possible explanations**: a different component, a different version, or the source conflates the word "branch".
- **Verification approach**:
  1. go back to the full original text and confirm the heading levels around this passage;
  2. locate the two branch selections `& 7` and `& 15` in the target .so;
  3. compare input/output lengths (20B vs 32B) using authorized samples.

### Q2. field13's family mapping table is missing

- **Location**: 4.3
- **Observation**: after the old version's "family by `slot % 3`" and the new version's "dispatch by `slot & 3`", the concrete mapping table is missing.
- **Impact**: cannot confirm which slot corresponds to which family.
- **Verification approach**: infer from known vectors, or locate the family dispatch table in the .so.

### Q3. Perseus's `F(session_uuid, kd)` is not given

- **Location**: 4.6
- **Observation**: the source gives only `pd, fkd = F(session_uuid, kd)` and one set of example values.
- **Impact**: cannot independently reproduce `pd` / `fkd`.
- **Verification approach**: infer from multiple `(session_uuid, kd)` samples, or locate the checksum function in the .so.

### Q4. Construction of the 41.2 outer check word

- **Location**: 4.4
- **Observation**: only states "composed of the low bits of the query SM3 and the low bits of field13".
- **Impact**: cannot confirm the integrity check on the outer layer of the report body.
- **Verification approach**: compare multiple query / field13 / check-word samples to determine the bit width and combination method.

### Q5. `search_field13` normalization rules

- **Location**: 4.3
- **Observation**: only says "computed after khronos normalization" and "shares the algorithm with the general branch but has a different calling contract".
- **Impact**: field13 for the search scenario cannot be aligned.
- **Verification approach**: compare field13 for the same request in search and non-search scenarios; locate the normalization function.

## P1: Version and parameter gaps

### Q6. 2.3's "three token entry points"

- **Location**: 2.3
- **Observation**: the source writes "the corresponding token delivery chain has three entry points:", with nothing after the colon.
- **Impact**: the acquisition path for the SDI token is incomplete.
- **Verification approach**: confirm the call order of the three entry points from the full original text or from packet captures.

### Q7. 3.1's clock baseline list

- **Location**: 3.1
- **Observation**: only says "a set of clock baselines"; the list is missing; the known inequality is `boot_time ≤ first_launch ≤ app_start ≤ request time`.
- **Impact**: cannot confirm the specific fields and tolerances.
- **Verification approach**: infer from the registration body and the Medusa report; compare samples from multiple devices.

### Q8. The full 30 keys of `x-common-params-v2`

- **Location**: 4.1
- **Observation**: the source lists the core keys in a code block and does not give the full 30-key table.
- **Impact**: structural completeness cannot be confirmed.
- **Verification approach**: capture real requests and enumerate the keys in order; compare across versions.

### Q9. Perseus `field3.18/19/20` and `field4.tk`

- **Location**: 4.6
- **Observation**: the source gives only example values, without meaning.
- **Impact**: the protobuf structure is incomplete.
- **Verification approach**: compare multiple samples; locate the serialization code.

### Q10. Generation rule for the `lp` path chain

- **Location**: 4.6
- **Observation**: only the example `"2|520830913191|521288087767|2041205042694|512296902576"` is given.
- **Impact**: cannot generate it independently.
- **Verification approach**: analyze it together with `token_address`, `module_base`, and the request context.

### Q11. Inconsistent address offset magnitude

- **Location**: 4.6
- **Observation**: the source writes `token_address − module_base ≈ 0x4000000` order of magnitude; computing from the given values yields `0x354FEFFB0` (about 13.3 GiB).
- **Impact**: the understanding of the "offset pattern" may be off.
- **Verification approach**: confirm the numeric units; compare differences across multiple samples.

### Q12. Changes in 41.0

- **Location**: 1.4
- **Observation**: the source covers 39.4–41.2 but does not expand 41.0.
- **Impact**: the version evolution chain is incomplete.
- **Verification approach**: find 41.0 samples and diff them.

## P2: Extended questions

### Q13. Internal algorithms of X-Argus / X-Ladon / X-Helios

- **Location**: 1.2
- **Observation**: the source gives only their roles and input dependencies, without expanding the algorithms.
- **Impact**: three of the seven signature headers remain black boxes.
- **Verification approach**: analyze the .so separately; compare inputs and outputs.

### Q14. TrustChain response content and trust score model

- **Location**: 3.6
- **Observation**: only says "the response content does not matter; what matters is that it occurred".
- **Impact**: cannot quantify the warm-up effect.
- **Verification approach**: compare the `empty` ratio with and without warm-up.

### Q15. Complete short-frame format for 39.4–40.x

- **Location**: 4.3
- **Observation**: only the pipeline is given (XOR stream → seed XOR → modified AES → frame encapsulation), without the field layout.
- **Impact**: the old version cannot be fully reproduced.
- **Verification approach**: static analysis of the old .so; compare frame lengths and fields between old and new.

## Proposed order of work

```text
Q1 (ownership of the eight branches)
  → Q2 (family mapping)
  → Q3 (F function)
  → Q4 (outer check word)
  → Q5 (search_field13)
  → remaining P1 / P2
```

Rationale: Q1 determines "which component you are analyzing"; Q2–Q5 determine "whether the core digest chain closes". Until these five are clear, filling in the remaining parameters has little value.

> 📌 **How to record**: each time you resolve an item, go back to the corresponding chapter, add a "verification record", and mark it done in this section; do not start a separate new note, to avoid fragmenting knowledge.
