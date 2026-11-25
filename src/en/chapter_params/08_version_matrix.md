# 4.8 Version Differences and Implementation Constraints

> 🎯 *"The version number is not decoration; it is a switch for a complete algorithm configuration."*

## Overview matrix

| Component / dimension | Old ≤40.x | New 41.1 / 41.2 |
|---|---|---|
| Medusa frame | short frame | v412 long frame |
| Medusa pipeline | XOR stream → seed XOR → modified AES → frame encapsulation | long-frame encapsulation |
| field13 slot | 52B content mixing, take the low 4 bits | `(khronos ^ 52) & 15` |
| field13 family count | 3 families (SHA-256 / Whirlpool / MD5) | 4 families (+ BLAKE2b) |
| Family dispatch | `slot % 3` | `slot & 3` |
| Branch constants | static constant table per branch | derived by rotation from khronos |
| Digest assembly | direct 20B | 32B folded into 16B core + 4B tail |
| Perseus | not enabled | enabled (FL + KD) |
| Outer check word | none | present (query SM3 low bits + field13 low bits) |

## Version is a global switch

The source:

> The version configuration from 41.1.0 onward determines which pipeline both Medusa and Perseus take.

This means the version configuration affects at least:

1. whether Medusa uses short frames or long frames;
2. whether field13 selects branches by content or by khronos;
3. whether field13 uses three families or four;
4. whether constants are a static table or derived at runtime;
5. whether Perseus is enabled and how FL / KD work;
6. whether there is an outer check word.

So the version number cannot be just a string in the query; it should map to a **complete algorithm configuration object**.

## Implementation constraints

### 1. One session, one configuration

```text
Session
├─ app_version: "41.2.0"
├─ algorithm_profile: V412
├─ medusa: long_frame
├─ field13: khronos_driven
├─ perseus: enabled
└─ constants: runtime_derived
```

Determined at session start, and not switched within the session.

### 2. Do not reuse vectors across versions

Old-version example vectors cannot be used to verify a new-version implementation:

- slot selection differs;
- families differ;
- constants differ;
- output assembly differs.

### 3. Group regression tests by version

| Test group | Coverage |
|---|---|
| ≤40.x | short frames, content-based branch selection, three families, direct 20B |
| 41.1/41.2 | long frames, khronos-based branch selection, four families, folding + tail |

Do not run the same set of assertions against both versions.

### 4. Record the provenance of constants

- static constant tables: record the version and branch number;
- runtime-derived constants: record the khronos and the derivation rule;
- otherwise, when an inconsistency appears, you cannot tell whether the constants are wrong or the inputs are wrong.

## Common failure modes

| Failure mode | Symptom | Root cause |
|---|---|---|
| version mismatched with algorithm | signature recomputation inconsistent | request declares 41.2 but field13 uses the old version |
| invalid khronos | signature rejected | suite1's `ts & 7 == 1` not satisfied |
| body / STUB out of sync | Gorgon validation fails | body modified without updating STUB |
| KD generated per request | Perseus checksum timing anomaly | no process-wide sharing |
| session_uuid reset | session state anomaly | regenerated per request |
| token_address independently random | environment detection anomaly | offset with module_base not maintained |
| wrong license_id | entire chain fails | wrong version constant |
| clock rollback | f17 monotonicity fails | elapsed not persisted |

## Acceptance checklist

Before considering something "aligned", confirm each item:

- [ ] the version configuration is fixed and not switched within a session;
- [ ] Medusa and Perseus use the same version configuration;
- [ ] field13's slot, family, and assembly match the version;
- [ ] khronos satisfies the low-3-bit constraint in the suite1 scenario;
- [ ] body, STUB, and Gorgon are in sync;
- [ ] KD is shared process-wide, isolated by aid, and recoverable after restart;
- [ ] session_uuid is fixed within a session;
- [ ] token_address maintains an offset relationship with module_base;
- [ ] license_id matches the target App version;
- [ ] the clock is monotonic, does not roll back, and does not repeat;
- [ ] byte-by-byte verification has been performed with the example vector for the corresponding version.

<div class="callout warn"><span class="callout-title">⚠️ The most important item</span>
Do not judge success by "one header computes correctly". The server validates combined consistency; a single version configuration error makes every header fail together.
</div>

## Review questions

1. Why should the "version configuration" control both Medusa and Perseus instead of each independently?
2. If you implement only the old version and not the new one, at which version would you fail fastest?
3. In the acceptance checklist, which item is most easily overlooked when "everything looks right"?

> 👉 Next chapter: [Chapter 5: review, questions and boundaries](../chapter_reflection/README.md)
