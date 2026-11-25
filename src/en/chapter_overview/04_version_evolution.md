# 1.4 Version Evolution: 39.4 → 41.2

> 🎯 *"Starting from 41.1, the algorithm changed somewhat."*

## Version range of the source

The original analyzes the different versions between **39.4 and 41.2**, focusing on the updates and differences from 41.1 onward.

| Version range | State | Coverage in the source |
|---|---|---|
| 39.4 – 40.x | old short-frame chain | used as a comparison |
| 41.0 | transition version | not expanded |
| 41.1 – 41.2 | v412 long frame, khronos-driven, Perseus | main focus |

> <span class="badge gap">source gap</span> The original does not give the specific changes in 41.0, and this note does not guess.

## Core differences around 41.1

### Difference 1: Medusa switches from short frames to long frames

- **Old version (≤40.x)**: short-frame chain, with the flow "XOR stream → seed XOR → modified AES → frame packing".
- **New version (41.1/41.2)**: v412 long-frame chain, and the branch selection mechanism of field13 is completely changed.

### Difference 2: field13 changes from "content-driven" to "khronos-driven"

| Dimension | Old version ≤40.x | New version 41.1/41.2 |
|---|---|---|
| slot selection | iterate the 52B content mixing function, then take the low 4 bits | `slot = (khronos ^ 52) & 15` |
| branch family | SHA-256 / Whirlpool / MD5, three families | SHA-256 / Whirlpool / BLAKE2b / MD5, four families |
| branch vs input relationship | the same content always yields the same branch | khronos changes → the branch changes |
| constant form | independent static constant table per branch | constants derived by rotation from khronos |
| output assembly | direct 20B | 32B folded into a 16B core + 4B khronos tail |

### Difference 3: Perseus is enabled

From 41.1 onward, a new-generation device report, `X-Perseus`, is enabled. Its core fields are:

- **FL**: a feature chain deterministically derived from the SDK startup state;
- **KD**: key-value state within the SDK process, which participates in session verification.

## Why the versions cannot be mixed

The original gives the most important practical conclusion:

> The two versions' algorithms cannot be mixed. The old version selects the branch by content, while the new version selects it by khronos — if a request uses the 41.2 version number but derives field13 with the old rules, the server's recomputation under the new rules will inevitably disagree, and vice versa.

This is not a "compatibility issue" but **direct failure**:

- the request declares 41.2;
- but field13 selects its branch by the 40.x rules;
- the server recomputes under 41.2 and gets a different slot;
- the digest differs, and verification fails.

## Role of the version configuration

The original notes: **version configuration from 41.1.0 determines which chain both Medusa and Perseus take**.

This means the version number is not "just a request header field", but a **global switch**:

- it determines whether Medusa uses short frames or long frames;
- it determines whether field13 selects the branch by content or by khronos;
- it determines whether Perseus is enabled and which FL / KD logic it takes.

<div class="callout warn"><span class="callout-title">⚠️ Implementation reminder</span>
Do not treat the "version number" as simple string concatenation. It should map to a complete algorithm configuration and stay consistent for the entire session.
</div>

## Review questions

1. Why could the old version's "same content always yields the same branch" be verified by request-by-request replay, while the new version cannot?
2. If only the version number is changed without changing the field13 algorithm, at which step will the server notice the inconsistency?
3. The 41.1 version configuration affects both Medusa and Perseus; what does this require of regression testing?

> 👉 Next chapter: [Chapter 2: Device Identity and Fingerprint System](../chapter_identity/README.md)
