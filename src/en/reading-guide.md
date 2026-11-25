# Reading Guide

## Assumed reader background

This note assumes you already have:

- Android reverse engineering basics: can read Smali / native assembly, familiar with JNI, so loading, and common hardening;
- HTTP protocol basics: request headers, query, body, TLS, HTTP/2;
- general cryptography knowledge: hashing, AES/SM4, HMAC, P-256, protobuf;
- at least one end-to-end protocol analysis under your belt.

You are not required to agree with the original's conclusions, but you are expected to **verify each item** when reproducing.

## Three recommended routes

### 🟠 Full-panorama route (fastest way to build the map)

`Preface → Chapter 1 → Chapter 2 → Chapter 3 → 4.1 → 4.8 → Chapter 5`

Suitable for: first contact with this system, or when you need to explain the overall structure to others.

Goal: be able to draw the relationship between the "device layer / network layer / behavior layer" and the seven signature headers, and understand why the registration chain has a fixed order.

### 🔵 Algorithm route (deep dive into fields)

`1.2 → 4.2 → 4.3 → 4.4 → 4.5 → 4.6 → 4.7`

Suitable for: understanding the exact inputs and outputs of field13, FL, KD, and Gorgon.

Goal: be able to explain the difference in Medusa branch selection before and after 41.1, and why the two versions cannot be mixed.

### 🟢 Engineering route (reproduce along the chain)

`2.1 → 2.4 → 3.1 → 3.2 → 3.3 → 4.1 → 4.7 → 4.8 → 5.1`

Suitable for: building a minimal chain in your own authorized lab environment.

Goal: be able to list the full dependency from device identity to signature headers for one request, and know which state must persist across requests.

## Versions and notation

| Notation | Meaning |
|---|---|
| <span class="badge old">≤40.x</span> | Old short-frame chain, content-driven field13 |
| <span class="badge new">41.1/41.2</span> | New v412 long frame, khronos-driven field13, Perseus |
| <span class="badge gap">source gap</span> | Missing in the source here; the note does not guess |
| <span class="badge">note derivation</span> | Calculated or inferred from source data, not yet measured |
| <span class="badge">to be verified</span> | Needs dynamic experiments or more samples |

## Version overview

| Version range | Key changes | Treatment in this note |
|---|---|---|
| 39.4 – 40.x | Medusa short frame; field13 selects branch by content; three hash families | Used as the old-version reference |
| 41.0 | Transition version, not expanded in the source | Marked as to be added |
| 41.1 – 41.2 | Medusa v412 long frame; field13 selects branch by khronos; four families; Perseus enabled | Main focus |

> ⚠️ **Note**: version numbers are not simply "bigger is newer". The original states explicitly that version configuration from 41.1.0 determines which chain both Medusa and Perseus take; with the wrong version configuration, even if each field is computed correctly, the combination still fails.

## Research boundaries

- Perform dynamic verification only on devices, accounts, networks, and App versions for which you hold **explicit authorization**.
- Do not carry out bulk registration, account nurture, traffic farming, fraud, or platform billing evasion.
- Do not collect, store, or distribute other people's personal information.
- Handle security findings through responsible disclosure; do not publish directly exploitable details.

> 📌 **Citation convention**: "the original" in this note means "Douyin App Risk Control Parameter Analysis"; "note derivation" means secondary calculations this project performs on source data, and is not equivalent to the original's conclusions.
