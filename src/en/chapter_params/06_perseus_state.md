# 4.6 X-Perseus: KD, Checksums, and protobuf

> 🎯 *"The semantics of KD are process-wide sharing with lifecycle isolation."*

## Process environment

The source gives a set of process environment fields:

```json
{
  "pid": 20033,
  "ppid": 886,
  "thread_pointer": 498090588864,
  "module_base": 497986002944,
  "jni_call_void": 505028537152
}
```

| Field | Meaning |
|---|---|
| `pid` | process ID |
| `ppid` | parent process ID |
| `thread_pointer` | thread pointer |
| `module_base` | module base address |
| `jni_call_void` | JNI call address |

The source:

> These address characteristics are part of the environment consistency check.

## Address offset pattern

The source's observation:

> `token_address`(512296902576) − `module_base`(497986002944) = 4310889632 ≈ an offset pattern on the order of `0x4000000`; `thread_pointer` and `module_base` likewise satisfy a base-address offset relationship.

<div class="callout warn"><span class="callout-title">⚠️ Note check: the magnitudes do not add up</span>
Computing directly from the values given in the source:

- `512296902576 − 497986002944 = 14310899632 = 0x354FEFFB0`, about **13.3 GiB**;
- `0x4000000` is only **64 MiB**; the two differ by a factor of about 213.

`thread_pointer − module_base = 104585920 = 0x63BDAC0`, about **99.7 MiB**.

Therefore, the source's "≈ 0x4000000 order of magnitude" may:
1. be missing several hexadecimal digits (for example, the intent was an order of magnitude of `0x400000000`);
2. or the numeric units / field meanings differ from the literal reading;
3. or the example values and the description come from different versions.

**This note does not take it upon itself to correct the source's conclusion**; it only records the computed results and lists the issue under [open questions](../chapter_reflection/02_open_questions.md).
</div>

## The lp string

`lp` in the source example:

```text
"2|520830913191|521288087767|2041205042694|512296902576"
```

The source only describes it as "a path chain inside the report" and does not expand the meaning of each segment.

<span class="badge gap">source gap</span> The generation rule for each `lp` segment is not expanded in the source.

## Session checksum

The output given by the source:

```json
{
  "cmr": 16777216,
  "cmr2": 16777216,
  "un_h": 1886076704,
  "vpn": 0,
  "sts": 59,
  "kd": 0,
  "fkd": 2665330607,
  "pd": 815239457,
  "do": 1
}
```

| Field | Example value | Notes |
|---|---|---|
| `cmr` | 16777216 | corresponds to `pd` |
| `cmr2` | 16777216 | corresponds to `fkd` |
| `un_h` | 1886076704 | related to session validation |
| `vpn` | 0 | VPN status |
| `sts` | 59 | startup duration / status |
| `kd` | 0 | KD value |
| `fkd` | 2665330607 | KD-derived value |
| `pd` | 815239457 | session-derived value |
| `do` | 1 | flag bit |

The source:

> `pd` (cmr) and `fkd` (cmr2) are written into the report; the server decrypts and recomputes them for comparison.

## What KD is

The source:

> KD is key-value state inside the SDK process and participates in session validation.

Two paths:

1. **Restored from SDK provider stored text**: the stored text is parsed as a decimal `uint32`;
2. **Default initial value 0**: cold start with no persisted state.

In the example vector `kd=0`, i.e., the cold-start scenario.

## Checksum function

The source:

```text
pd, fkd = F(session_uuid, kd)
```

Example:

- `kd = 0`;
- `session_uuid = "861775c1-5ed4-47f2-b474-2c51dcd9e43e"`;
- yields `pd = 815239457`, `fkd = 2665330607`.

<span class="badge gap">source gap</span> The source does not give the concrete implementation of `F`. This note does not guess.

## Key consistency requirements

The source:

> The semantics of KD are process-wide sharing with lifecycle isolation — within the same App process, the same KD value is shared across requests (the first request writes it, later requests read the same value); different App identities (aid) are isolated from each other; after the SDK process restarts, the value is restored from the stored text. If a simulated implementation generates KD independently per request, the timing characteristics of the checksum expose it.

Broken into four:

| Requirement | Meaning |
|---|---|
| Process-wide sharing | multiple requests in the same process read the same KD |
| Lifecycle isolation | must not be shared across different aids |
| Restart recovery | after an SDK process restart, restored from the stored text |
| No per-request generation | generating KD independently per request exposes timing characteristics |

## protobuf structure

The source:

```text
report.field1 = 1
report.field3 = {
  "6":  "v04.10.05.02-bugfix",   # SDK build version
  "7":  40066,
  "14": "41.2.0",                # App version
  "15": 1772,
  "18": 3285352954,
  "19": 3590681842,
  "20": 992990262394
}
report.field4 embedded JSON = {
  the session checksum fields above + "fl" / "lp" / "tk"
}
```

| Field number | Example value | Notes |
|---|---|---|
| `field1` | 1 | fixed value |
| `field3.6` | `v04.10.05.02-bugfix` | SDK build version |
| `field3.7` | 40066 | version-related |
| `field3.14` | `41.2.0` | App version |
| `field3.15` | 1772 | version-related |
| `field3.18` | 3285352954 | unknown |
| `field3.19` | 3590681842 | unknown |
| `field3.20` | 992990262394 | unknown |
| `field4` | JSON | checksum + fl / lp / tk |

<span class="badge gap">source gap</span> The meaning of `field3.18/19/20` and `field4.tk` is not expanded in the source.

## Session UUID and token address

The source:

> `session_uuid`: derived from SDK internal RNG state, generated and cached on the first request of a session, and unchanged within the same session.

> `token_address`: a process memory address characteristic associated with the module base address, satisfying a base address + fixed-magnitude offset pattern. During simulation it may be generated randomly but must maintain the offset relationship with `module_base`; an independently random address is one of the signatures of environment detection.

Two points:

1. `session_uuid` is session-level and fixed after the first request;
2. `token_address` cannot be independently random; it must maintain an offset relationship with `module_base`.

<div class="callout note"><span class="callout-title">🔑 Key conclusion</span>
Perseus consistency is not only about field values but also about the "lifetime of state" and the "relative relationship of addresses". Generating KD per request, changing session_uuid per request, and independently random token_address are all typical exposure points.
</div>

## Review questions

1. Why should KD be "shared process-wide and isolated by aid"? What does each requirement prevent?
2. `pd` / `fkd` are derived from `session_uuid` and `kd`. What two things can the server therefore verify?
3. Why is an independently random `token_address` detected? What should it maintain a relationship with?

> 👉 Next section: [4.7 X-Gorgon](./07_gorgon.md)
