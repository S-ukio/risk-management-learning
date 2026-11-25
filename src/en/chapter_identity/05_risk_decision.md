# 2.5 Fingerprints and Risk Control Decisions

> 🎯 *"empty is not failure; it is a normal stage after the cold start of a new device."*

## Four States

The source divides search-type request results into four states and uses them as risk-control decision boundaries:

| State | Meaning | Risk-control interpretation |
|---|---|---|
| `success` | Video / user results returned | Device trusted |
| `empty` | Request succeeded but returned an empty page | Slightly downweighted; the device label is not fully established yet |
| `blocked` | Verification or rate limiting required | Fingerprint / behavior flagged |
| `error` | Request or response abnormal | Protocol-layer error; check the signature before the fingerprint |

## Why `empty` Is the Most Easily Misjudged

The source has an important reminder:

> empty is the state most easily misjudged: it is not failure, but a normal stage after the cold start of a new device.

Newcomers often take "no data returned" as "request failed", and therefore:

- Retry repeatedly;
- Change device parameters frequently;
- Assume the signature algorithm is wrong.

In fact, when a new device has just registered and its trust score has not been established, an empty page is expected behavior. Frequent retries instead make the behavioral layer look scripted.

## The Correct Way to Judge

The source suggests:

> Whether a device is usable should be judged by `search_ok` (true for both results and a normal empty page), not merely by whether data came back.

The decision logic can be written as pseudocode:

```text
if response.status == success:
    search_ok = true
elif response.status == empty:
    search_ok = true     # normal empty page; does not mean the device is unavailable
elif response.status == blocked:
    search_ok = false    # fingerprint or behavior flagged
else:  # error
    search_ok = false    # check the signature first, then the fingerprint
```

## States and Troubleshooting Order

| State | Check first | Check next |
|---|---|---|
| `success` | — | — |
| `empty` | New device / insufficient trust score | Whether TrustChain was warmed up |
| `blocked` | Fingerprint consistency | Behavioral timing, environment detection |
| `error` | Signature algorithm | Parameter format, version configuration |

<div class="callout warn"><span class="callout-title">⚠️ Troubleshooting Order Matters</span>
Seeing `error` and checking the fingerprint first often wastes effort—most `error`s are signature or parameter-format problems. Conversely, seeing `blocked` and checking only the signature misses the real fingerprint contradiction.
</div>

## Mapping to the Three-Layer Model

| State | Most likely failing layer |
|---|---|
| `empty` | Behavioral layer (insufficient trust score) |
| `blocked` | Device layer / behavioral layer |
| `error` | Protocol layer (signature, parameters, version) |

This also explains why Chapter 1 stresses that "the three layers are an AND": different states correspond to different failing layers, and troubleshooting must locate the layer first, then the field.

## Study Questions

1. Why should `empty` be treated as "usable" rather than "failure"?
2. If a new device returns `empty` on consecutive searches, what should be checked first?
3. When `error` is investigated as a fingerprint problem, which steps are usually wasted?

> 👉 Next chapter: [Chapter 3: Device Registration Flow](../chapter_registration/README.md)
