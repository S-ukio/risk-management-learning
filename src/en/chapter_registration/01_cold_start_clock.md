# 3.1 Cold Start Sequence and Clock Baseline

> 🎯 *"It must be determined before the first request and remain consistent throughout."*

## Why the Clock Is a Prerequisite for Registration

The validity of a registration request depends on a set of clock baselines. The source's requirement:

> The validity of a registration request depends on a set of clock baselines, which must be determined before the first request and remain consistent throughout.

The reason is not hard to understand:

- Medusa's f17 clock slot requires monotonicity;
- Perseus fields such as `sts` and `do` relate to startup duration;
- The `X-Khronos` signature header needs a stable time anchor;
- The registration body must also pre-embed `medusa_clock_origin` / `medusa_session_ms` / `medusa_elapsed_ms` / `medusa_session_uuid`.

If each component takes its own time, the contradiction of "multiple time baselines within one request" appears.

## Known Cross-Relations

The source gives an explicit inequality:

```text
boot_time ≤ first_launch ≤ app_start ≤ request time
```

Meaning:

| Value | Meaning |
|---|---|
| `boot_time` | Device boot time |
| `first_launch` | Time the App first launched |
| `app_start` | Start time of the current process |
| request time | Time the request is sent |

Any inversion is clearly anomalous. For example:

- `app_start` earlier than `first_launch`: the current process cannot start before the App's first launch;
- Request time earlier than `app_start`: the request cannot be sent before the process starts;
- `first_launch` earlier than `boot_time`: the App cannot launch before the device boots.

## What the Source Is Missing

<span class="badge gap">source gap</span> The source says here:

> The validity of a registration request depends on a set of clock baselines, which must be determined before the first request and remain consistent throughout:
>
> - The cross-relation of these values is: `boot_time ≤ first_launch ≤ app_start ≤ request time`.

The list of "this set of clock baselines" after the colon is empty on the extracted page, and there is no corresponding image. **This note does not guess at the specific field names**; it keeps only the known inequality and the Medusa clock group that explicitly appears in the registration body.

Questions still to be verified:

- What values does this set of baselines contain? Are they exactly `boot_time_ms` / `app_start_ms` in the registration body?
- Do `first_launch` and `app_start` correspond to different fields?
- What deviation range does the server allow?

See [the open questions list](../chapter_reflection/02_open_questions.md).

## Medusa Clock Group

The registration body explicitly contains four Medusa clock fields:

| Field | Role |
|---|---|
| `medusa_clock_origin` | Session clock origin |
| `medusa_session_ms` | Cumulative milliseconds within the session |
| `medusa_elapsed_ms` | Elapsed milliseconds |
| `medusa_session_uuid` | Session UUID |

The source explains:

> The session clock state must be established already at registration, for reuse by later Medusa reports.

This means:

- The clock origin is not taken fresh on every request;
- It is "pinned" during registration;
- `elapsed` in subsequent requests must increase monotonically;
- `session_uuid` is generated on the session's first request and then fixed.

## Correct Mental Model of Clock State

```text
Process start
  │
  ├─ generate SDK seed
  ├─ pin clock_origin
  ├─ generate session_uuid
  │
  ├─ registration request: carries clock_origin / session_ms / elapsed / uuid
  │
  ├─ subsequent request 1: elapsed = now - clock_origin
  ├─ subsequent request 2: elapsed must be ≥ the previous value
  └─ ...
```

<div class="callout warn"><span class="callout-title">⚠️ Common Mistake</span>
Taking `clock_origin` afresh on every request, or letting `elapsed` move backward. The former makes the "session origin" drift continuously; the latter directly violates monotonicity.
</div>

## Study Questions

1. Why must `boot_time` be earlier than `first_launch`? What happens if the device clock is set back?
2. When should `medusa_clock_origin` be determined: process start, App start, or the first request?
3. If `elapsed` moves backward between two requests, what can the server infer from that?

> 👉 Next section: [3.2 Registration Chain Breakdown](./02_register_chain.md)
