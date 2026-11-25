# 4.5 X-Perseus: FL Feature Chain

> 🎯 *"The same set of inputs always yields the same set of chain values, so it can be reproduced offline and verified byte by byte."*

## What Perseus is

The source:

> A new-generation device report enabled from 41.1 onward; the core fields of its protobuf encoding are FL and KD.

Two cores:

- **FL**: a feature chain deterministically derived from SDK startup state;
- **KD**: key-value state inside the SDK process that participates in session validation.

This page covers FL; KD is covered in 4.6.

## FL structure

The source:

> FL is a feature chain deterministically derived from SDK startup state; its structure is a 9-element array plus a request-level thread word:

```text
FL = [slot0, slot1, chain[0..4], slot2, slot3] + thread_word
String form: "0|0|c0|c1|c2|c3|c4|0|0|thread_word"
```

Broken down:

| Position | Content | Notes |
|---|---|---|
| 0 | `slot0` | external slot, default 0 |
| 1 | `slot1` | external slot, default 0 |
| 2–6 | `chain[0..4]` | five uint32 chain values |
| 7 | `slot2` | external slot, default 0 |
| 8 | `slot3` | external slot, default 0 |
| 9 | `thread_word` | request-level component |

In the string form, all four external slots default to `0`, the chain values sit in the middle, and `thread_word` comes last.

## Derivation inputs

The triple given by the source:

| Input | Meaning |
|---|---|
| `seed` | seed generated at SDK startup |
| `k` | startup round |
| `flags` | derivation flags |

The source:

> The derivation function takes `(seed, k, flags)` as input and produces five uint32 chain values — the same set of inputs always yields the same set of chain values (determinism), so the chain can be reproduced offline and verified byte by byte.

This is an important property:

- FL is not random;
- it depends only on the state at startup;
- given `(seed, k, flags)`, `chain[0..4]` can be computed independently;
- therefore example vectors can be used for byte-by-byte verification.

## chain_flags

The source:

> `chain_flags=3` means both the http and ws callbacks are registered, which is the state of a real App after startup.

Meaning:

- `chain_flags` is a bit flag;
- `3` means both callbacks are registered;
- a real App is usually in this state after startup;
- if `chain_flags` is not 3 in the simulated environment, FL may not match.

## thread_word

The source:

> `thread_word` is a request-level component derived from the request URL and the token address; it is fixed within a request and changes across requests.

| Property | Notes |
|---|---|
| Derivation input | request URL + token address |
| Scope | request-level |
| Within the same request | fixed |
| Across requests | changes |

## fl_slots

The source:

> The four external slots of FL (`fl_slots`) default to 0 and are determined by SDK internal state; in the measured 41.2 scenario, keeping them at 0 aligns with the real package.

Practical conclusion:

- default to 0;
- do not fill in non-zero values arbitrarily;
- in the measured 41.2 scenario, 0 is enough to align.

## Complete example (from the source)

> ⚠️ The following values come from the source and are used only to illustrate the vector structure; they may become invalid as versions change. Do not treat them as usable credentials.

### Inputs (SDK source state)

```json
{
  "seed": 45884766,
  "k": 418,
  "flags": 511,
  "chain_flags": 3,
  "http_callback": true,
  "ws_callback": true,
  "fl_slots": [0, 0, 0, 0],
  "query": "version_code=410200&device_platform=android&device_id=3559594890366347&aid=1128&iid=1527634069305532&tt_data=a",
  "license_id": 1588093228,
  "token": "AkZhxlbm-UC3lv4akPhb6BKmG",
  "token_address": 512296902576,
  "khronos": 1795342217,
  "session_uuid": "861775c1-5ed4-47f2-b474-2c51dcd9e43e",
  "kd": 0,
  "vpn": 0,
  "sts": 59,
  "do": 1
}
```

### Derived output

```text
chain       = [45884668, 4230265858, 2147978368, 974138666, 3197775088]
thread_word = 482472847
FL string   = "0|0|45884668|4230265858|2147978368|974138666|3197775088|0|0|482472847"
lp string   = "2|520830913191|521288087767|2041205042694|512296902576"
```

### A verifiable observation

The source:

> `chain[0] = 45884668` differs from `seed = 45884766` by only 98 (`0x62`), so the first derivation step applies an observable direct transformation to the seed; subsequent chain values are fully dispersed.

This implies:

- the first step of the derivation function applies an observable transformation to `seed`;
- the difference of 98 can serve as the first checkpoint for "is the implementation correct";
- later chain values disperse quickly and are suitable for whole-chain verification.

<div class="callout note"><span class="callout-title">🔑 Key conclusion</span>
FL is deterministic: you can first verify only the difference of 98 between `chain[0]` and `seed`, then verify all five chain values. This separates a "wrong first step" from "wrong later rounds".
</div>

## Review questions

1. Why can FL be reproduced offline while the new version of field13 cannot (hint: does the input include request content)?
2. `thread_word` is derived from the URL and the token address. What does this bind it to?
3. What class of implementation error can the difference of 98 between `chain[0]` and `seed` help diagnose?

> 👉 Next section: [4.6 X-Perseus: KD, checksums and protobuf](./06_perseus_state.md)
