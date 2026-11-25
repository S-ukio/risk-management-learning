# 4.7 X-Gorgon

> 🎯 *"Among the seven signature headers, it is the one most tightly bound to 'this request', and the core of anti-replay."*

## Input four-tuple

The source:

```text
Gorgon = F(khronos, X-SS-STUB(body MD5), URL digest, cookie/context digest)
```

Four inputs:

| Input | Source | Role |
|---|---|---|
| `khronos` | `X-Khronos` | time anchor |
| `X-SS-STUB` | request body MD5 (hex) | binds the request body |
| URL digest | request URL | binds the target endpoint |
| cookie / context digest | session context | binds session state |

## SEED

The source:

> In practice, `SEED=0x0000` aligns with the real package.

This is an implementation detail: when Gorgon's seed is `0x0000`, the output aligns with the real App.

> 📌 The source does not give the concrete algorithm or rounds of `F`, only the input structure and SEED. This note does not guess.

## What it binds

Gorgon's role is to bind request content to the signature:

> Gorgon's role is to bind request content to the signature — if one byte of the body changes while STUB is not updated in sync, validation fails.

Specifically:

- body changes → `X-SS-STUB` changes → Gorgon changes;
- URL changes → URL digest changes → Gorgon changes;
- khronos changes → Gorgon changes;
- session context changes → context digest changes → Gorgon changes.

If any one of the four inputs is out of sync, Gorgon will not match.

## Anti-replay

The source:

> It is the header most tightly bound to "this request" among the seven signature headers, and the core of anti-replay: an expired khronos or reuse of an old signature is rejected.

Two points:

1. **khronos expired**: the signature of an old request cannot be used in a new time window;
2. **reuse of an old signature**: the same signature cannot be used for a second request.

This is why "capture one packet and replay it repeatedly" usually fails: Gorgon binds the request, the time, and the session together.

## Relationship with STUB

`X-SS-STUB` is the hexadecimal string of the request body MD5, and it is one of Gorgon's inputs.

A common error chain:

```text
modify body
  │
  ├─ forget to update X-SS-STUB
  │      │
  │      ▼
  │   Gorgon uses the old STUB
  │      │
  │      ▼
  └─ server recomputes body MD5 → mismatch with STUB → reject
```

Note: even if the Gorgon algorithm is entirely correct, it fails as long as STUB and body are out of sync.

## Self-check list

- [ ] `X-SS-STUB` matches the MD5 (hex) of the current body;
- [ ] `khronos` has not expired and uses the same value as Medusa / Perseus;
- [ ] the URL digest is based on the final request URL (including the necessary query);
- [ ] the cookie / context digest matches the session state;
- [ ] `SEED=0x0000` (aligned with the target version);
- [ ] no Gorgon from an old request is reused.

<div class="callout note"><span class="callout-title">🔑 Key conclusion</span>
Gorgon is the gatekeeper of "request-level binding". It is not responsible for device identity, nor for state reporting; it answers only one question: was this signature generated for this request, this time, and this session?
</div>

## Review questions

1. Why does Gorgon bind body, URL, khronos, and context at the same time instead of binding only the body?
2. If the body and URL are unchanged but khronos changes, can Gorgon still be reused?
3. Is `X-SS-STUB` the same value as Medusa's `body_md5`? Who does each serve?

> 👉 Next section: [4.8 Version differences and implementation constraints](./08_version_matrix.md)
