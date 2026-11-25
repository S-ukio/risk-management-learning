# 1.2 Seven Signature Headers and Plaintext Context

> 🎯 *"Plaintext headers are the declaration; signature headers are the proof."*

## Seven signature headers (algorithm layer)

| Header | Role | Input dependencies |
|---|---|---|
| X-Khronos | Second-level timestamp; the time anchor of the signature system | current time |
| X-Argus | Core device signature, encrypted protobuf payload | device parameters, query, khronos |
| X-Gorgon | Request-level verification signature | khronos + X-SS-STUB + URL digest |
| X-Ladon | Lightweight signature, refreshed with khronos | khronos + license_id |
| X-Helios | Auxiliary verification | request context |
| X-Medusa | Device state long-frame report | collector output, clock slot, field13 |
| X-Perseus | Device state report | FL feature chain, in-process KD state, session UUID |

### How to remember the seven

Group them as "time → device → request → state":

- **Time anchor**: `X-Khronos`, the common input to all signature headers.
- **Device identity**: `X-Argus` (core device signature), `X-Ladon` (lightweight, refreshed with khronos).
- **Request binding**: `X-Gorgon` (strongest binding to body / URL), `X-Helios` (auxiliary verification).
- **State reporting**: `X-Medusa` (long-frame device state), `X-Perseus` (FL / KD report).

> 📌 The original does not expand the internal algorithms of `X-Argus`, `X-Ladon`, or `X-Helios`, and this note does not guess either; the focus is on the three headers with detailed breakdowns: Medusa, Perseus, and Gorgon.

## Risk control context headers (plaintext layer)

| Header | Role |
|---|---|
| X-SS-STUB | Request body MD5 (hex), one of Gorgon's inputs |
| X-SS-REQ-TICKET | Request ticket, monotonically increasing |
| X-Tt-Dt / X-Tt-Store-Region | Distribution and storage region |
| sdk-version / x-tt-request-tag | SDK and request tags |

These headers are not encrypted, so the server can read them directly. Their role is to **declare**: what version I am, which region I come from, what my request body digest is, and how far my ticket has advanced.

## The relationship between declaration and proof

The original's summary is very concise:

> The server reads the declaration first, then reverse-derives decryption through the signature headers and verifies whether the declaration agrees with the data inside the signature. A mismatch between declaration and proof is a more common cause of risk control hits than a wrongly computed signature.

The server's verification can be broken into three steps:

1. **Read the declaration**: extract version, device, region, and body digest from the plaintext headers, query, UA, and `x-common-params-v2`.
2. **Verify the proof**: reverse-derive or recompute with the signature headers (Gorgon / Medusa / Perseus, etc.) to obtain the data inside the signature.
3. **Cross-compare**: do the declaration and the proof agree? Do multiple encodings of the same fact (for example SDI and dtrait) agree?

<div class="callout warn"><span class="callout-title">⚠️ Common misconception</span>
"Every header computed correctly on its own" does not mean "the request is valid". The server compares consistency, not single-point correctness.
</div>

## A concrete example

Suppose you changed the request body:

- the `body` changed;
- `X-SS-STUB` was not updated;
- `X-Gorgon` was computed with the old STUB.

The result:

- the Gorgon algorithm itself may be perfectly correct;
- but when the server recomputes `X-SS-STUB` and finds it does not match the body, it rules the request tampered with immediately.

This is the typical scenario of "declaration and proof do not agree".

## Review questions

1. Among the seven signature headers, which is most strongly bound to "this request"? Why?
2. Why is `X-Khronos` the common input to all signature headers, instead of each taking its own time?
3. If `X-SS-REQ-TICKET` is not monotonic, what might that indicate?

> 👉 Next: [1.3 Local SDK Component Mapping](./03_sdk_components.md)
