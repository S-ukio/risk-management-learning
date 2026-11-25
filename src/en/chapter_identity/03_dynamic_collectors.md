# 2.3 Dynamic Fingerprint: SDI/MSSDK Collectors

> 🎯 *"Static fingerprints are declarations; dynamic collection is measurement. The two must match."*

## Collection Surface

The MSSDK dynamic collection surface falls into three categories:

### 1. Runtime Probing

- Installed app list (partial);
- Real-time sensor readings;
- Battery / charging state.

### 2. Environment Detection

- root artifacts;
- Xposed / Frida hook artifacts;
- Emulator artifacts;
- VPN status.

### 3. Behavioral Features

- Screen interaction timing;
- The "authenticity" of sensor noise (real-device noise vs synthetic data).

## Why "Measurement" Is Harder to Forge Than "Declaration"

Static fields can be copied from a real device, but dynamic collection requires:

- Sensor readings to follow physical laws (noise, drift, range);
- Battery / charging state to be consistent with time and usage intensity;
- Screen interaction timing to look human rather than scripted;
- Environment detection to show no hooks, injection, or emulator traces.

The source's use of the word "measurement" is apt: the server is not reading the form you filled in; it is checking whether the data you measured looks real.

## Token Issuance Chain

The source says:

> The corresponding token issuance chain has three entry points:

<span class="badge gap">source gap</span> **The source does not give the specific contents of the three entry points here** (the text after the colon is empty on the extracted page, and there is no corresponding image). This note does not guess.

Known related facts:

- The SDI token is issued by MSSDK;
- It is a short-lived collection credential that must be refreshed periodically;
- The caching mechanism supports recovery from historical sessions, and recovery requires validating that `app_id` matches.

The concrete form of the three entry points (for example: registration, activation, before search?) must be confirmed later from the full source text or from testing; see [the open questions list](../chapter_reflection/02_open_questions.md).

## Two Practical Points

The source gives two very concrete reminders at the end of 2.3:

### 1. `ri` Reports Must Use On-Device Parameters

> The ri report must use on-device parameters rather than phone parameters passed in from outside—one kind of risk-control cross-check compares the model consistency of the ri contents against the UA / static fingerprint.

Implications:

- The model, resolution, and system version in the `ri` report must come from real collection on the current device;
- They cannot be "passed in" from external configuration;
- The server compares the `ri` contents with the UA and static fingerprint.

### 2. A Missing `raw24` Should Not Break the Chain

> If raw24 is missing during the registration flow, it should not interrupt the get_token and birth chains (the server tolerates missing fields but not an interrupted chain).

Implications:

- Missing some fields is tolerable;
- But a broken chain (for example, not sending `get_token` because one field is missing) has more serious consequences;
- The design should be "report as best you can, allow missing fields", not "stop when a field is missing".

<div class="callout note"><span class="callout-title">🔑 Key Takeaway</span>
The point of dynamic collection is not to "collect every field" but to make "the fields collected agree with each other and with the static declarations". Missing fields can be tolerated; a broken chain or self-contradiction cannot.
</div>

## Study Questions

1. Why can "sensor noise" distinguish a real device from synthetic data?
2. If the `ri` report uses externally supplied parameters, which declarations would it conflict with?
3. Why does the server "tolerate missing fields but not an interrupted chain"?

> 👉 Next section: [2.4 Encrypted Fingerprint Carriers](./04_encrypted_carriers.md)
