# 4.4 f17 Clock Slot, Session Structure, and the Eight-Branch Question

> 🎯 *"The first second pins the origin; thereafter elapsed grows monotonically."*

## f17 clock slot

The source:

> f17 clock slot: the clock sample inside the report, containing f17_base_ns, ticks, and the request sequence number.

The three components:

| Field | Meaning |
|---|---|
| `f17_base_ns` | clock base (nanoseconds) |
| `ticks` | sample count |
| request sequence number | the request's index within the session |

### Monotonicity requirement

The source:

> Monotonicity is required — no regression and no repetition across requests; this is the core means of detecting clock rollback / multiple app instances.

Three constraints:

1. **No regression**: a later request's clock value must be ≥ the previous one;
2. **No repetition**: two requests cannot use the same clock value;
3. **Cross-request persistence**: clock state must not be lost between requests.

### Lifecycle

The source:

> The clock lifecycle must persist across requests: the first second pins the origin, and elapsed grows monotonically thereafter.

It can be drawn as:

```text
request 1: base = T0, elapsed = 0
request 2: base = T0, elapsed = Δ1   (Δ1 > 0)
request 3: base = T0, elapsed = Δ2   (Δ2 > Δ1)
...
```

Note: `base` stays fixed while `elapsed` grows monotonically. If every request resets `base`, the server sees "the session origin drifting continuously".

### Differences in 41.2

The source:

> The 41.2 long frame arranges clock slots differently from the old short frame, but the monotonicity constraint is the same in both versions.

Implications:

- How slots are arranged and where they are placed differ between 41.2 and the old version;
- But the "no regression, no repetition" constraint is unchanged;
- Implementations must not relax monotonicity merely because the long frame is used.

## Session structure

### `medusa_session_uuid`

The source:

> `medusa_session_uuid` is generated on the session's first request and then fixed; request-level slots such as `req_f2` are updated per request.

| Field | Lifecycle | Update timing |
|---|---|---|
| `medusa_session_uuid` | session-level | generated on the session's first request, fixed thereafter |
| `req_f2` etc. | request-level | updated every request |

### The clock group in the registration body

The source:

> The clock group embedded in the registration body is consumed here.

That is, `medusa_clock_origin` / `medusa_session_ms` / `medusa_elapsed_ms` / `medusa_session_uuid` from 3.3 do not become useless once registration is complete; they are later consumed in Medusa reports.

### 41.2's outer check word

The source:

> The 41.2 report body adds an outer check word (composed of the low bits of the query SM3 and the low bits of field13), further binding the request content to the report.

Implications:

- The 41.2 report body has one extra check word on the outside;
- It is composed of the low bits of the query SM3 and the low bits of field13;
- Its role is to bind "request content" and "report" more tightly.

<span class="badge gap">source gap</span> The check word's exact bit width, composition method, and verification rules are not expanded in the source; listed as an open question.

## The eight-branch structure: a passage to be verified

At the end of 4.3, the source contains the following passage:

> The composition of the eight branches:
>
> Branch selection: `slot = int(khronos) & 7`, **determined only by the low 3 bits of khronos, unrelated to body length and content**.

And gives the following table:

| slot | Algorithm form | Characteristic |
|---|---|---|
| 0 | modified AES-CBC (2 rounds) | S-box XOR `0x3d` |
| 1 | modified AES-CBC (2 rounds) | S-box XOR `0x33` |
| 2 | modified AES-CBC (2 rounds) | S-box XOR `0x3b` |
| 3 | modified AES-CBC (2 rounds) | S-box XOR `0x39` |
| 4 | affine SPN (24 rounds) | fixed affine parameter table |
| 5 | second virtual-machine core | main-state generation + two 24-round reductions |
| 6 | modified SM4 form (24 rounds) | S-box XOR `0x17` |
| 7 | modified SM4 form (24 rounds) | S-box XOR `0x1f` |

### Structural pattern

The source:

> Structural pattern: `slot % 4` determines the family (AES-CBC / affine SPN / VM / SM4), and `slot // 4` determines the variant within the family (S-box XOR values `0x39` and `0x3d`, `0x17` and `0x1f`, in pairs). The four AES branches share the round structure and differ by only one constant XOR; the two SM4 branches likewise.

### Forward and reverse directions

The source:

> Each branch provides two directions: forward (19B → 32B MAC) and reverse (32B → 19B); AES/SM4-form branches internally pad the 19-byte input with 13 `0x0d` bytes to make two blocks. After the inverse transform, the forward computation must be recomputed and compared, to prevent MAC forgery.

### ⚠️ Attribution question

This passage clearly conflicts with the earlier field13 description:

- Earlier, field13 is said to have **16 branches**, selected by `slot & 15`;
- This passage says **8 branches**, selected by `slot & 7`;
- Earlier, the output is said to be **20B**; this passage says forward **19B → 32B MAC**.

Possible explanations:

1. It describes another component (not field13) and was simply placed at the end of 4.3 when the source was laid out;
2. It is the algorithm of some older version / sub-feature, existing in parallel with field13;
3. The source uses the word "branch" inconsistently across versions; the two actually refer to different things.

<span class="badge gap">source gap</span> The source does not say which header or version these eight branches belong to. These notes **do not guess the attribution**; only the table and the question are retained.

> 📌 This is the first priority among the open questions in 5.2: first confirm what the "eight branches" actually belong to, then discuss reproduction.

## State lifecycle summary

| State | Scope | Lifecycle | Constraint |
|---|---|---|---|
| `f17_base_ns` | session | persists across requests | fixed and unchanging |
| `ticks` | request / session | updated per request | monotonic |
| request sequence number | session | incrementing | no repetition |
| `medusa_session_uuid` | session | generated on first request | fixed |
| `req_f2` | request | updated every request | bound to the request |
| outer check word (41.2) | request | generated per request | binds query + field13 |

## Review questions

1. Why require both "no regression" and "no repetition"? What happens if only one holds?
2. If `medusa_session_uuid` is regenerated for every request, what does the server see?
3. Can the "eight branches" and the "16-branch field13" be the same algorithm? List the evidence for your judgment.

> 👉 Next section: [4.5 X-Perseus: the FL feature chain](./05_perseus_fl.md)
