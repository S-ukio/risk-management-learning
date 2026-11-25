# 4.2 X-Khronos and Suite Alignment

> 🎯 *"X-Khronos is the time anchor of the entire signature system."*

## Basic role

The source's definition:

> X-Khronos is the time anchor of the entire signature system; every signature header's input includes it.

This means:

- It is not a private field of any one header;
- It is a common input to all signature headers;
- It determines the temporal validity of signatures and also affects the derivation of other fields.

## Two modes

### Regular mode

Take the current second directly:

```text
khronos = floor(now / 1000)
```

### suite1 mode

The source:

> suite1 mode requires the timestamp to satisfy `ts & 7 == 1` (the low 3 bits are binary `001`); when it does not hold, move forward to the next valid value.

That is:

```text
while (ts & 7) != 1:
    ts += 1
```

Or the equivalent form:

```text
ts = ts + ((1 - (ts & 7)) & 7)
```

> Note: the source says "take the next valid value forward"; combined with the `ts & 7 == 1` constraint, this in practice means **moving in the increasing direction** to the next second that satisfies the condition. This note follows "increment to the next valid value" as authoritative.

## Why this constraint exists

The source's explanation:

> This is one of the server's probes for distinguishing "normal clients / non-standard calls": a real App naturally produces khronos values with this distribution in certain scenarios, whereas a forged call that does not know the constraint produces uniformly distributed timestamps.

Implications:

- A real App's khronos is not "any second";
- In suite1 scenarios it only falls on the `...001` mod-8 distribution;
- If you take the current time arbitrarily, the low 3 bits are uniformly distributed;
- The server sees the distribution and knows "this is not a real client".

## The new role in 41.1

The source:

> Version difference: in old versions (≤40.x), khronos is merely the common time input to the signature headers; from 41.1/41.2 it further determines Medusa field13's branch selection (`(khronos ^ 52) & 15`).

This means:

| Version | Role of khronos |
|---|---|
| ≤40.x | common time input |
| 41.1/41.2 | common time input + field13 branch selection |

So from 41.1, an inappropriate khronos value not only causes an "illegal timestamp" but also lands on the wrong hash branch.

<div class="callout"><span class="callout-title">🧮 Note derivation (to be verified)</span>
If the suite1 constraint and the new field13 are both in effect, a simple bit-level derivation can be made:

- `khronos & 7 == 1`, i.e. the low 3 bits are `001`;
- `52 = 0b110100`, low 3 bits `100`;
- the low 3 bits of `khronos ^ 52` are `001 ^ 100 = 101 = 5`;
- `slot = (khronos ^ 52) & 15`, whose low 3 bits are fixed at `101`, with bit 3 determined by bit 3 of khronos;
- therefore `slot ∈ {5, 13}`, and `slot & 3 == 1`.

Corollary: under suite1, the new field13 can only land on the "family index 1" branch.  
**This is a note derivation, not a source conclusion; it needs empirical verification.**
</div>

## Version–khronos relationship diagram

```text
            ┌───────────────────────────────────────┐
            │               X-Khronos               │
            │  time anchor + branch selection input │
            └───────────────────┬───────────────────┘
                                │
          ┌─────────────────────┴────────────────────┐
          │                                          │
  ≤40.x: time input only                41.1/41.2: time + slot
          │                                          │
          ▼                                          ▼
  time fields of signature headers       slot = (khronos ^ 52) & 15
                                                     │
                                                     ▼
                                          Medusa field13 branch
```

## Review questions

1. Why can the server use the distribution of khronos's low 3 bits to distinguish real clients from scripts?
2. If suite1 and the new field13 are both in effect, which two values can slot take? What experiment is needed to verify this derivation?
3. In regular mode khronos takes the current second — does that mean it can be chosen arbitrarily? What other constraints exist?

> 👉 Next section: [4.3 X-Medusa: two generations and field13](./03_medusa.md)
