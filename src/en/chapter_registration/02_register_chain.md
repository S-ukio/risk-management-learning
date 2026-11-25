# 3.2 Registration Chain Breakdown

> 🎯 *"Order is the contract."*

## The Six-Step Chain

The complete cold registration chain given by the source (in strict order):

| Step | API / action | Output |
|---|---|---|
| 1 | `device_register` | Obtain `device_id` / `iid` (`klink.amemv.com`) |
| 2 | `device_report` | Perseus device report |
| 3 | `app_log` | First-launch events (Sword encoding) |
| 4 | `get_token` | SDI token issuance |
| 5 | `activate` / `activate_record` | Activation state report |
| 6 | `birth()` | Nurture chain (see 3.5) |

```text
1. device_register  → device_id / iid
2. device_report    → Perseus device report
3. app_log          → first-launch events (Sword encoding)
4. get_token        → SDI token
5. activate / activate_record → activation state
6. birth()          → nurture chain
```

## Why Order Matters

The source's summary:

> Order is the contract: app_log must send the first-launch manifest before the fingerprint runs (it must not carry fingerprint run results); birth's alert report must sign the first-launch message; the ri report uses on-device parameters. Out-of-order does not necessarily fail, but the server records behavioral timing as a long-term profile, and the subsequent requests of out-of-order devices receive lower weight.

Broken down, there are three concrete constraints:

### 1. `app_log` Must Come Before the Fingerprint Runs

- The first-launch manifest must not carry "fingerprint run results";
- That is, `app_log` records "what was seen just after launch", not "what was summarized after collection finished".

### 2. `birth`'s Alert Report Must Sign the First-Launch Message

- `birth` is not just sending "I was born";
- It must sign the **first-launch message**;
- This means the first-launch message must be saved for later signing.

### 3. `ri` Reports Use On-Device Parameters

- Consistent with the reminder in 2.3;
- `ri` contents must come from on-device collection and must not be passed in externally.

## Consequences of Out-of-Order

The source says "out-of-order does not necessarily fail", which is easily misread as "order does not matter". The actual meaning is:

- The server will not reject immediately because of a single out-of-order event;
- But it records the timing into a long-term profile;
- The weight of subsequent requests is reduced;
- The reduction accumulates; it is not a single decision.

It is like a credit score: being late once does not get you banned immediately, but it leaves a record.

## A Counterexample: Finishing Within 1 Second

The source notes in 3.5:

> A registration + nurture chain in which all requests finish within 1 second is itself an anomalous signature—a real device's chain naturally has second-level intervals.

So **"fast" is not an advantage**. A real device's chain has:

- Network round trips;
- Page rendering;
- User interaction;
- System scheduling.

All of these naturally produce second-level intervals. Compressing six steps into 1 second instead exposes "this is not a real device".

## Chain State Diagram

```text
[1] device_register
      │  device_id / iid
      ▼
[2] device_report ──▶ Perseus
      │
      ▼
[3] app_log ─────────▶ first-launch events (without fingerprint results)
      │
      ▼
[4] get_token ───────▶ SDI token
      │
      ▼
[5] activate / activate_record
      │
      ▼
[6] birth() ─────────▶ nurture chain
```

Each step consumes the state produced by the previous step and writes the new state into the shared container.

<div class="callout note"><span class="callout-title">🔑 Key Takeaway</span>
Correctness of the registration chain = correct order + natural timing + continuous state. Satisfying only one of these is not enough to pass the behavioral layer.
</div>

## Study Questions

1. Why must `app_log` not carry fingerprint run results?
2. Why must birth's alert report sign the first-launch message? What state does that require saving?
3. If all six steps are correct but the interval is only 200ms, how might the server judge it?

> 👉 Next section: [3.3 Registration Plaintext Body Structure](./03_register_payload.md)
