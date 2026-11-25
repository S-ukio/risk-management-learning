# 3.6 TrustChain Warm-up

> 🎯 *"The content returned by a warm-up request does not matter; what matters is that it occurred."*

## What TrustChain Is

The source's definition:

> TrustChain is the server's mechanism for accumulating device trust.

It is not a client-side algorithm but a server-side process of accumulating a device trust score. What the client can do is trigger warm-up requests at key points, giving the server an opportunity to establish initial trust.

## Two Trigger Points

| Trigger point | Timing | Role |
|---|---|---|
| pre-register | Before registration | Establish the initial trust score |
| Pre-search warm-up | Before the first search | Compensate for a new device's insufficient trust score |

### 1. pre-register

- Triggered before formal registration;
- The purpose is to establish the initial trust score;
- So that the later registration request is not a "completely unfamiliar" first appearance.

### 2. Pre-Search Warm-Up

- Triggered before the first search;
- The purpose is to compensate for a new device's insufficient trust score;
- It lowers the probability that the first search directly returns `empty`.

## Why "It Occurred" Matters More Than "What It Returned"

The source:

> The content returned by a warm-up request does not matter; what matters is that it occurred.

The meaning of this sentence:

- What the server records is "this device had a warm-up before registration / before search";
- The response content of the warm-up request may have no practical business value;
- But it leaves a timeline record on the server that helps establish the trust score.

## Consequences of Skipping Warm-Up

The source:

> New devices that skip warm-up and search directly show a significantly higher probability of empty.

This is consistent with the conclusion in 2.5:

- `empty` is not failure;
- But if a new device skips warm-up, the probability of `empty` is higher;
- Because the server does not yet have enough timeline evidence to judge "whether this device is trustworthy".

## Position of Warm-Up in the Chain

```text
pre-register warm-up
      │
      ▼
device_register
      │
      ▼
device_report / app_log / get_token / activate / birth
      │
      ▼
pre-search warm-up
      │
      ▼
first search
```

Note:

- pre-register is before registration;
- Pre-search warm-up is before the first search;
- The two warm-ups address trust at different stages.

<div class="callout note"><span class="callout-title">🔑 Key Takeaway</span>
TrustChain is not an "optional request" but timeline evidence for the trust score. Skipping it is equivalent to starting a new device from zero, making the first search more likely to return empty.
</div>

## Study Questions

1. Why should pre-register warm-up happen before registration rather than after?
2. Does "the returned content of a warm-up request does not matter" mean you can send anything? Why?
3. If a device searches immediately after registration without pre-search warm-up, what state is most likely?

> 👉 Next chapter: [Chapter 4: Core Request Parameter Breakdown](../chapter_params/README.md)
