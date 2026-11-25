# 1.1 Three-Layer Risk Control Model

> 🎯 *"The three layers are an AND relationship: if any layer fails, the request is downgraded."*

## What each layer looks at

| Layer | Focus | Typical carriers |
|---|---|---|
| Device layer | Whether this device is real and its identity is trustworthy | device fingerprint, SDI token, TicketGuard key |
| Network layer | Whether this link looks like a real client | TLS fingerprint, HTTP/2 behavior, cronet version |
| Behavior layer | Whether the timing and state of this request set are self-consistent | signature headers, clock consistency, session state machine |

### Device layer

The device layer answers "who you are and whether you are real". It does not check a single field; it checks **whether the combination is plausible**:

- whether hardware parameters, system parameters, and display parameters match one another;
- whether the sensor set, ABI, and CPU topology look like those of a real device model;
- whether the dynamic readings collected at runtime agree with the static declarations.

### Network layer

The network layer answers "whether this connection was sent by a real client". It does not look at HTTP headers, but at lower-level characteristics:

- TLS fingerprint (ClientHello extensions, curves, cipher suite order);
- HTTP/2 behavior (SETTINGS, window, priority, pseudo-header order);
- whether the cronet version agrees with the UA / version declaration.

This is why "copying the request verbatim into curl" usually fails: the HTTP layer is right, but the TLS and HTTP/2 layers still do not look right.

### Behavior layer

The behavior layer answers "whether the timing and state of this request set are self-consistent". It cares about:

- whether the inputs of the signature headers reference one another (khronos, body digest, query digest);
- whether the clock is monotonic and whether it rolls back;
- whether the session state machine advances as expected (register first, then report, then search);
- whether request intervals match the distribution of real devices.

## Why AND, not OR

The three layers are not "pass any one and you are through"; **all must pass at the same time**. If any layer fails, the request is downgraded:

| Downgrade mode | Manifestation |
|---|---|
| Empty page | The request succeeds, but there are no results |
| CAPTCHA | Human verification is required |
| Rate limiting | Frequency or quota is reduced |
| Outright rejection | An error is returned or the connection is dropped |

## The most common failure: inconsistent state

The original makes a key judgment:

> In practice, the most common failure is not that "some algorithm was computed wrong", but that **the state is inconsistent**.

What this means:

- a single signature header may fully conform to the algorithm;
- but two headers reference different khronos values;
- or the body was changed while `X-SS-STUB` was not updated;
- or the device_id used during registration differs from later requests;
- or the clock origin is reset between two requests.

The server does not need to "crack" your algorithm; it only needs to find two declarations that contradict each other to rule the request anomalous.

<div class="callout note"><span class="callout-title">🔑 Key conclusion</span>
Get state consistency right first, then worry about algorithm details. A fully correct but mutually contradictory header set is worse than a simple but globally consistent one.
</div>

## Review questions

1. If the TLS fingerprint is wrong but all seven signature headers are correct, which downgrade result is the request most likely to get? Why?
2. Why does "copying a request captured from a browser into Python" usually fail the network layer?
3. Give an example of "single field valid, combination contradictory" (either the device layer or the behavior layer).

> 👉 Next: [1.2 Seven Signature Headers and Plaintext Context](./02_signature_headers.md)
