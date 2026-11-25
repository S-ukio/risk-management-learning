# 4.3 X-Medusa: Two Generations and field13

> 🎯 *"The core difference between the two lies in field13's hash branch mechanism."*

## What Medusa is

The source's definition:

> Medusa is the long-frame encrypted report of device state.

It is not a single field but a report containing:

- device-state collection results;
- clock slot;
- field13 (request-content digest);
- session structure.

## The two generations

| Version | Chain | Structure |
|---|---|---|
| 39.x – 40.x | short frame | XOR stream → seed XOR → modified AES → frame packing |
| 41.1 / 41.2 | v412 long frame | long-frame packing, field13 mechanism changed |

The source does not expand the full long-frame packing format; the focus is on field13.

## field13's input

field13 is the digest hash of request content in the Medusa report; its input is fixed at **52 bytes**:

```text
msg52 = query_sm3(32B) || body_md5(16B) || khronos_le(4B)
```

Breaking it down:

| Part | Length | Meaning |
|---|---|---|
| `query_sm3` | 32B | SM3 digest of the query |
| `body_md5` | 16B | MD5 of the request body |
| `khronos_le` | 4B | little-endian encoding of khronos |

Note:

- `body_md5` is related to `X-SS-STUB` but is not a simple duplication of it;
- `khronos_le` is 4 bytes little-endian, not a decimal string;
- The order of the three is fixed and cannot be swapped.

## Old version (≤40.x): content-driven

### Branch selection

- The 52-byte input buffer is processed by a dedicated mixing function;
- The mixing function uses a fixed seed;
- Two sets of obfuscation operations alternate over even and odd bytes;
- After iteration, the low 4 bits are taken, yielding `slot 0–15`.

Key property:

> Which branch is selected is determined by the request content itself — the same query / body / khronos necessarily lands on the same branch, while different requests spread across different branches.

### Branch composition

The source:

> The 16 branches are a permutation mapping of three families of modified hashes, split into families by `slot % 3`.

Three families:

- SHA-256 family;
- Whirlpool family;
- MD5 family.

Each branch is implemented independently, with constants and round counts modified independently per branch, outputting a 20B digest.

<span class="badge gap">source gap</span> The specific permutation mapping table after "split into families by `slot % 3`" is missing from the extracted page; these notes do not fill the gap by guessing.

## New version (41.1/41.2): khronos-driven

### Branch selection

```text
slot = (khronos ^ 52) & 15
```

Computed from khronos in one step; no longer dependent on content mixing.

The source's observation:

> Combined with suite1's constraint on khronos's low bits, the slot distribution of real requests is not uniform.

This agrees with the derivation in 4.2: under suite1, `slot ∈ {5, 13}`.

### Branch composition

The source:

> The 16 branches are rearranged into four families, dispatched by `slot & 3`.

Four families:

- SHA-256 family;
- Whirlpool family;
- BLAKE2b family;
- MD5 family.

<span class="badge gap">source gap</span> The specific family mapping table after "dispatched by `slot & 3`" is missing from the extracted page; these notes do not fill the gap by guessing.

### Digest assembly

The source:

> 32B-family digests are first XOR-folded (first 16B XOR last 16B) into a 16B core (the MD5 family uses its 20B digest directly), then a trailing 4B is appended — the tail is derived from the first 8 bytes of the core via alternating even/odd bit-operation iteration plus `(khronos ^ 52) & 15`, forming the final 20B field13.

Broken into steps:

```text
1. Select family (slot & 3)
2. Compute family digest
   ├─ 32B families: first16 XOR last16 → 16B core
   └─ MD5 family: 20B digest directly
3. Generate 4B tail
   └─ core[0..7] alternating even/odd bit-operation iteration + slot
4. Concatenate → 20B field13
```

## Old vs new

| Dimension | Old ≤40.x | New 41.1/41.2 |
|---|---|---|
| slot selection | low 4 bits after iterating the 52B content-mixing function | one-step `(khronos ^ 52) & 15` |
| Branch families | SHA-256 / Whirlpool / MD5 (three) | SHA-256 / Whirlpool / BLAKE2b / MD5 (four) |
| Branch–input relation | same content always same branch (verifiable by per-request replay) | khronos changes → branch changes |
| Constant form | per-branch independent files, static constant table | constants derived by khronos rotation (generated at runtime) |
| Output assembly | 20B directly | 32B folded to 16B core + 4B khronos tail |

## Search scenario: search_field13

The source:

> The search scenario has its own separate search_field13 branch convention (computed after khronos normalization), sharing the algorithm with the general branch but with a different calling contract.

Implications:

- The search scenario does not directly reuse the general field13;
- It has its own branch convention;
- The algorithm may be shared, but the calling contract differs;
- How exactly "khronos normalization" is performed is not expanded in the source.

<span class="badge gap">source gap</span> The normalization rules and calling contract of search_field13 have no details in the source; listed as an open question.

## The most important practical conclusion

The source:

> The two versions' algorithms cannot be mixed. The old version selects branches by content and the new version by khronos — if a request uses the 41.2 version number but derives field13 with the old algorithm, the server's recomputation under the new rules will necessarily disagree; and vice versa.

This is why implementations must keep both branch algorithm sets and partition them by version:

- It is not "old-new compatibility";
- It is "select the whole algorithm set by version";
- The version configuration from 41.1.0 onward determines which chain both Medusa and Perseus take.

<div class="callout warn"><span class="callout-title">⚠️ Failure mode</span>
Request declares 41.2 → field13 uses the old algorithm → server recomputes under 41.2 → different slot → different digest → verification fails. The algorithm itself is not wrong; the error is "version and algorithm do not match".
</div>

## Review questions

1. Why can the old version's "same content, same branch" be verified by per-request replay, while the new version cannot?
2. Why does the new field13's 4B tail depend on the first 8 bytes of the core instead of taking khronos directly?
3. "search_field13 and the general field13 share the algorithm but have different calling contracts" — where might they differ?

> 👉 Next section: [4.4 f17 clock slot, session structure, and the eight-branch question](./04_medusa_clock.md)
