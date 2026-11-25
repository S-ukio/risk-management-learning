# 2.4 Encrypted Fingerprint Carriers

> 🎯 *"Two independent encodings of the same fact."*

Collected data is not reported in plaintext; it goes through three encrypted carriers:

1. SDI body (MSSDK token);
2. dtrait (Badger v4.0 form);
3. TicketGuard (P-256 key system).

## SDI Body (MSSDK Token)

- The collector output is a natively encrypted binary block;
- The server can decrypt and verify it;
- It contains a large number of device measurements.

The difficulty is that **any measurement conflicting with a declaration elsewhere in the request loses points**.

For example:

- SDI reports a resolution of 1080×2400;
- The UA says 1440×3200;
- The two disagree, and even if the SDI encryption is entirely correct, the request is judged anomalous.

## dtrait (Badger v4.0 Form)

- `dtrait_pk1` + Badger form construction;
- The content is another structured encoding of device information;
- Its relationship with SDI is **two independent encodings of the same fact**.

The source emphasizes:

> The server can cross-compare the consistency of the two encodings, which is why both algorithms must be fully reproduced rather than just one.

This means:

- Only SDI and no dtrait → one proof short;
- Both present but inconsistent → cross-comparison fails;
- Both present and consistent → this layer can be passed.

## TicketGuard (P-256 Key System)

- Two sets of P-256 keys are generated per device: **REE (normal world) / TEE (trusted execution environment)**;
- A verification header is injected per route;
- The TEE side should be inside trusted hardware.

The practical conclusion given by the source:

> In an emulated environment, only the REE-side implementation can be built, and the keys must be kept persistent—keys for the same device_id must be stable across sessions; key drift equals device drift.

Key points:

- Keys for the same `device_id` must be stable across sessions;
- Regenerating keys on every launch = changing devices on every launch;
- The server sees the anomaly of "same identity, different keys".

## Division of Labor Among the Three Carriers

| Carrier | Encoding | Main content | Key constraint |
|---|---|---|---|
| SDI body | Natively encrypted binary | Collector measurements | Consistent with other declarations in the request |
| dtrait | Badger form | Structured encoding of device information | Cross-consistent with SDI |
| TicketGuard | P-256 signature | Device key proof | Keys stable for the same device_id |

<div class="callout note"><span class="callout-title">🔑 Key Takeaway</span>
The three carriers are not "pick one of three" but "three pieces of evidence that corroborate one another". A missing piece, or two that contradict, lowers the trust score.
</div>

## Study Questions

1. Why are SDI and dtrait designed as "two encodings of the same fact" instead of being merged into one?
2. The TEE side of TicketGuard cannot be reproduced in an emulated environment; what must the REE-side implementation take care of?
3. If SDI is entirely correct but dtrait is missing, how might the server judge the request?

> 👉 Next section: [2.5 Fingerprints and Risk Control Decisions](./05_risk_decision.md)
