# 2.2 Static Fingerprint: Device Model Templates

> 🎯 *"The risk in a static fingerprint is not in any single field but in whether the combination is plausible."*

## What a Static Fingerprint Is

A static fingerprint is the device's "hardware declaration". It is reported once at registration and stays consistent afterward.

Categories listed by the source:

| Category | Contents |
|---|---|
| Hardware parameters | Brand, model, board, codename, hardware name (the `ro.product.*` family) |
| System parameters | Android version, API level, ROM build, kernel |
| Display parameters | Resolution, dpi, notch / cutout information |
| Sensor set | Presence and range of the accelerometer, gyroscope, and magnetometer |
| ABIs and CPU topology | `arm64-v8a` support, core count, frequency tiers |

## Why the Combination Matters More Than Single Fields

A single field is easy to forge: pick any brand and any resolution, and it can "look plausible".

What is genuinely hard is **a self-consistent combination**. The source gives two examples:

### Example 1: Contradiction Between Resolution and dpi

- Resolution `1080×2400`;
- dpi stated as `480`.

The problem: `480 dpi` usually corresponds to 1440p-class devices, not 1080p. Collectors look at the two fields together and find that they do not belong to the same class of device.

### Example 2: Contradiction Between API Level and ROM String

- API level stated as `33` (Android 13);
- The ROM signature string is from Android 12.

The problem: the system version and the ROM build information disagree, indicating that the fingerprint was not collected intact from a real device but assembled.

## How Collectors Cross-Validate

Static-fingerprint validation can be understood in three layers:

1. **Field-level validation**: whether length, character set, and enum values are valid;
2. **Combination-level validation**: resolution ↔ dpi ↔ model, API ↔ ROM ↔ kernel, ABI ↔ CPU topology;
3. **Declaration-level validation**: whether the static fingerprint ↔ UA ↔ `x-common-params-v2` ↔ registration body agree in all four places.

<div class="callout warn"><span class="callout-title">⚠️ Common Mistake</span>
Aligning only the UA while neglecting the registration body and `x-common-params-v2`. The server compares them together; any mismatch loses points.
</div>

## Engineering Implications of Device Model Templates

If you want to build a reproducible experimental environment, the static fingerprint should not be made up on the fly. Instead:

- Choose a real device model template;
- Organize that model's `ro.product.*`, resolution, dpi, API, ABI, and sensor set into a single configuration;
- Have the UA, registration body, `x-common-params-v2`, and all later collection reference the same configuration.

This is the idea of a "device model template": **one configuration source, referenced in many places, kept consistent**.

## Study Questions

1. Besides resolution and dpi, what other field combinations are likely to be cross-validated?
2. If only the model in the UA is changed and the registration body is not, at which step would the mismatch surface?
3. Why is a "real device model template" more stable than "randomly generated fields"?

> 👉 Next section: [2.3 Dynamic Fingerprint: SDI/MSSDK Collectors](./03_dynamic_collectors.md)
