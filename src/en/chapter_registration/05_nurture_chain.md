# 3.5 Nurture and Activation Chains

> 🎯 *"All requests finishing within 1 second is itself an anomalous signature."*

## Registration Only Obtains Identity

The source's framing is clear:

> Registration only obtains identity; the behavioral cold-start chain includes:

That is, successful registration ≠ device usable. There is a "behavioral cold start" chain afterward.

## Four Steps

| Step | Action | Content |
|---|---|---|
| 1 | `app_log` report | First-launch manifest; does not carry fingerprint run results |
| 2 | `stats_collect` | Behavioral statistics (Sword encoding): launch, page, and exposure events |
| 3 | `app_alert_check` | Fetches and parses the server-issued configuration, determining subsequent behavior switches |
| 4 | Supplementary reports | `log_settings`, permission events, etc. |

### 1. `app_log`

- First-launch manifest;
- **Does not carry fingerprint run results**;
- The fingerprint is a later step and cannot be mixed into the first-launch log in advance.

### 2. `stats_collect`

- Behavioral statistics;
- Uses Sword encoding;
- Content covers launch, page, and exposure events.

### 3. `app_alert_check`

- Fetches the server-issued configuration;
- Parses the configuration;
- Determines subsequent behavior switches.

This step shows that the server is not "passively receiving data"; it issues configuration to guide client behavior. The client's subsequent actions should be influenced by this configuration.

### 4. Supplementary Reports

- `log_settings`;
- Permission events, etc.

## Timing Is Modeled

The source's key judgment:

> The timing of the behavioral chain is likewise modeled: the server has an expected distribution for "what was done within how long after registration".

This means the server looks not only at "what you did" but also at "how long you took to do it".

### Why Finishing Within 1 Second Is Instead Anomalous

The source:

> A registration + nurture chain in which all requests finish within 1 second is itself an anomalous signature—a real device's chain naturally has second-level intervals.

A real device's chain includes:

- Network round trips (RTT);
- Page rendering;
- User interaction;
- System scheduling;
- Waiting for server responses.

These factors naturally produce second-level intervals. Compressing the entire chain into 1 second indicates:

- No waiting for pages;
- No real interaction;
- No progress driven by server responses.

This is itself the signature of a "script".

## The Right Rhythm for Behavioral Cold Start

The chain can be understood as a "dependency-bearing asynchronous process":

```text
Registration succeeds
  │
  ├─ app_log (first-launch manifest, without fingerprint results)
  │      │  wait for network + rendering
  │      ▼
  ├─ stats_collect (launch / page / exposure)
  │      │  wait for events to occur
  │      ▼
  ├─ app_alert_check (fetch configuration)
  │      │  decide next steps from the configuration
  │      ▼
  └─ supplementary reports (log_settings / permission events)
```

Each step should:

- Wait for the previous step to finish;
- Wait for real pages / events;
- Decide the next step from the server's response.

<div class="callout warn"><span class="callout-title">⚠️ Do Not "Optimize Away" the Interval</span>
Compressing intervals to the minimum is not optimization; it is exposure. A real device's chain inherently has waits; only scripts pursue "zero latency".
</div>

## Study Questions

1. Why must `app_log` not carry fingerprint run results?
2. What is the role of `app_alert_check`? What happens if it is ignored?
3. If the entire chain took only 800ms, from which dimensions might the server judge it anomalous?

> 👉 Next section: [3.6 TrustChain Warm-up](./06_trustchain.md)
