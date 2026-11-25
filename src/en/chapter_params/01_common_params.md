# 4.1 x-common-params-v2

> 🎯 *"The other device / version declaration besides the UA."*

## What it is

The source's definition:

> A public parameter block with a fixed 30-key structure — the other device / version declaration besides the UA.

It usually appears in the query or among common parameters, containing device, version, system, language, time zone, and similar information. The core keys listed in the source include:

```text
aid / app_name / channel / version_code / version_name / device_platform
device_type / device_brand / device_id / iid / openudid / cdid
os_version / os_api / resolution / dpi / language / tz
first_launch_timestamp / _rticket / cdid / host_abi / cpu_support64
...
```

> 📌 The source lists these as a code block; in reality it is a fixed structure of 30 keys, and the above are the readable core keys. The full key table needs to be completed in a later version.

## Consistency constraints

The source's summary:

> Constraint: fully consistent with the UA, the registration body, and the query parameters — all three.

This can be drawn as a table of "one fact, four declarations":

| Fact | Registration body | UA | `x-common-params-v2` | query |
|---|---|---|---|---|
| Model / brand | ✓ | ✓ | ✓ | ✓ |
| OS version / API | ✓ | ✓ | ✓ | ✓ |
| App version | ✓ | ✓ | ✓ | ✓ |
| Resolution / dpi | ✓ | — | ✓ | ✓ |
| device_id / iid | ✓ | — | ✓ | ✓ |

Any discrepancy in any one place will be caught by the server's cross-comparison.

## Explicit validation of `version_name`

The source notes in particular:

> `version_name` is explicitly validated at the signing entry point — when the version declared in the query differs from the device template version, signing is rejected outright (avoiding the generation of self-contradictory requests).

This sentence has two implications:

1. **Validation happens at the signing entry point**, not at the business layer;
2. The purpose is **to avoid generating self-contradictory requests** — if the version declaration is inconsistent, the signature itself is meaningless.

Practical implications:

- Do not change only the `version_name` in the query while forgetting the device template;
- Do not upgrade the device template while continuing to use a query from the old version;
- Version is a global configuration, not a single field.

## Engineering implications of the 30-key structure

A fixed structure means:

- Key order, count, and naming may all be validation points;
- One missing key, one extra key, or one renamed key may be detected;
- It cannot be treated as "a query thrown together casually".

It is recommended to maintain it as a **struct**:

```text
CommonParams
├─ app: aid, app_name, channel, version_code, version_name
├─ device: device_platform, device_type, device_brand, device_id, iid
├─ identity: openudid, cdid
├─ system: os_version, os_api, resolution, dpi, language, tz
├─ time: first_launch_timestamp, _rticket
└─ cpu: host_abi, cpu_support64
```

## Self-check list

- [ ] All 30 keys present, with stable naming and order;
- [ ] `version_name` / `version_code` consistent with the device template and registration body;
- [ ] `device_id` / `iid` consistent with the registration result;
- [ ] `resolution` / `dpi` consistent with the static fingerprint;
- [ ] `os_version` / `os_api` consistent with the ROM declaration;
- [ ] `first_launch_timestamp` consistent with the clock baseline;
- [ ] `_rticket` monotonically increasing;
- [ ] `host_abi` / `cpu_support64` consistent with the ABI / CPU topology.

<div class="callout warn"><span class="callout-title">⚠️ The most common mistake</span>
Aligning only the UA and query, forgetting the registration body and `x-common-params-v2`. The server compares four places, not two.
</div>

## Review questions

1. Why should `version_name` validation live at the signing entry point rather than at the business layer?
2. If the 30-key structure is missing one key, at which layer might it be detected?
3. Is `_rticket` monotonicity the same thing as `X-SS-REQ-TICKET` monotonicity?

> 👉 Next section: [4.2 X-Khronos and suite alignment](./02_khronos.md)
