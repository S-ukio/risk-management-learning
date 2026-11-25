# 5.1 Experiment Review: 400 Devices and 85%

> 🎯 *"Here I registered roughly 400+ devices; about 350 of them could run search and comment; the success rate was around 85%."*

## Source data

The review given at the end of the source:

> Here I registered over 400 devices; about 350 could run search and comment, a success rate of around 85%. If any experts have experience with account-login risk control, or with protocol-level posting and ordering, we are happy to exchange notes and learn together.

Organized into a table:

| Metric | Value |
|---|---|
| Devices registered | 400+ |
| Able to run search / comment | about 350 |
| Success rate | about 85% |

> ⚠️ **Note**: This is the result reported by the original author; this note has not independently reproduced it and cannot verify its statistical methodology. The discussion here covers only the methodology it reveals, not a reproducible operational guide.

## What 85% tells us

### 1. Per-point correctness is not enough; end-to-end consistency is

If the seven signature headers, SDI, dtrait, and TicketGuard could all be computed correctly in isolation, the success rate should be close to 100%. The actual 85% indicates that the failing 15% is mainly not "the algorithm is unknown" but:

- inconsistent state (clock, KD, session_uuid);
- mismatched version configuration;
- environment detection hits (root, Frida, emulator, VPN);
- contradictory fingerprint combinations;
- unnatural timing.

This matches Chapter 1's conclusion: **the most common failure is inconsistent state**.

### 2. Chain integrity matters more than per-field precision

The source says in 2.3 that "the server tolerates some missing fields but does not tolerate a broken chain". The 85% success rate also indicates:

- a small number of missing fields is tolerable;
- a broken chain, wrong order, or timing anomaly leads to cumulative downgrading;
- getting end-to-end through matters more than "every field perfect".

### 3. Failure samples carry more information than success samples

If you can obtain those 15% failure samples, classify them by the four states from 2.5:

| State | Possible cause |
|---|---|
| `empty` | insufficient trust score, missing warm-up, new device cold start |
| `blocked` | fingerprint contradiction, environment detection, behavioral anomaly |
| `error` | signature error, version mismatch, parameter format |

This is more valuable than the number "85% success rate" itself.

## Methodological takeaways

| Takeaway | Corresponding chapter |
|---|---|
| Ensure state consistency first, then refine the algorithm | 1.1, 1.3 |
| Version is a global configuration, not a string | 1.4, 4.8 |
| Clock, KD, session_uuid must persist across requests | 3.1, 4.4, 4.6 |
| Behavioral timing should be natural; do not pursue zero latency | 3.5 |
| Use the four states to locate the failure layer instead of blind retries | 2.5 |
| Do not guess at source gaps; list the questions first | 5.2 |

## Where not to misread

The original author concludes with "if any experts have experience with account-login risk control, or with protocol-level posting and ordering, we are happy to exchange notes and learn together". This sentence is easily misread as "this is an operational guide".

In fact:

- the source does not give steps for bulk registration, account nurturing, posting, or ordering;
- it analyzes **the composition of risk-control parameters and version differences**;
- this note provides no operational steps either.

<div class="callout warn"><span class="callout-title">⚠️ Boundary</span>
"Understanding how risk control works" and "bulk bypassing risk control" are two different things. The former can serve defense, assessment, and compliance testing; the latter may violate platform terms and the law. This note discusses only the former.
</div>

## Review questions

1. What categories of causes most likely make up the 85% success rate?
2. Why do "failure samples classified by four states" carry more information than "the overall success rate"?
3. If you were to design an authorized experiment to verify the suite1 derivation in 4.2, how would you control the variables?

> 👉 Next section: [5.2 Open questions](./02_open_questions.md)
