# 3.3 Registration Plaintext Body Structure

> 🎯 *"The device_register request body is plaintext JSON (some fields base64)."*

## Five Groups

The source divides the `device_register` request body into five groups:

| Group | Role | Key fields |
|---|---|---|
| Device declaration group | Declares what the device is | `device_type`, `device_brand`, `device_manufacturer`, `device_board`, `device_codename`, `hardware`, `rom`, `resolution`, `dpi` |
| Version declaration group | Declares the App and channel | `version_name`, `version_code`, `channel`, `license_id` |
| Identity seed group | Provides local identity seeds | `openudid`, `cdid`, `boot_time_ms`, `app_start_ms` |
| Environment group | Declares the runtime environment | `is_vpn`, `is_activated`, `register_signal` |
| Medusa clock group | Establishes the session clock | `medusa_clock_origin`, `medusa_session_ms`, `medusa_elapsed_ms`, `medusa_session_uuid` |

## Device Declaration Group

Must be fully consistent with the UA and later collection.

The source's reminder:

> Must be fully consistent with the UA and later collection.

This means the same fact must appear in at least four places:

1. The `device_register` request body;
2. The UA;
3. `x-common-params-v2`;
4. Later SDI / dtrait collection results.

Any difference in any place will be found by cross-comparison.

## Version Declaration Group

| Field | Description |
|---|---|
| `version_name` | App version name, e.g. `41.2.0` |
| `version_code` | Version code, e.g. `410200` |
| `channel` | Channel |
| `license_id` | A fixed constant for each App |

The source specifically notes:

> `license_id` is a fixed constant for each App (the `1588093228` series for Douyin 41.x); an error invalidates the entire chain.

That is, `license_id` is not "some number you fill in", but one of the constants of the whole signature system. A wrong value causes the entire chain to fail, not just one header.

## Identity Seed Group

| Field | Description |
|---|---|
| `openudid` | Generated locally, device-level |
| `cdid` | Generated locally, install-level, uppercase UUID |
| `boot_time_ms` | Device boot time (milliseconds) |
| `app_start_ms` | App start time (milliseconds) |

The source explains:

> Generated locally; fixed once registration succeeds, and reused by all subsequent requests.

These four are "seeds": after successful registration they never change, and all later requests reference them.

## Environment Group

| Field | Description |
|---|---|
| `is_vpn` | Whether a VPN is used |
| `is_activated` | Whether activation has completed |
| `register_signal` | Registration signal |

The source's reminder:

> VPN status must truthfully reflect the transport layer; the local detection result should be synchronized to the registration body and to the `vpn` field in the Perseus source.

Implications:

- If the transport layer goes through a VPN, `is_vpn` must be true;
- The `is_vpn` in the registration body must match the `vpn` field in the Perseus source;
- It cannot be that "the registration body says VPN is off while Perseus says it is on".

## Medusa Clock Group

| Field | Description |
|---|---|
| `medusa_clock_origin` | Session clock origin |
| `medusa_session_ms` | Cumulative milliseconds within the session |
| `medusa_elapsed_ms` | Elapsed milliseconds |
| `medusa_session_uuid` | Session UUID |

The source explains:

> The session clock state must be established already at registration, for reuse by later Medusa reports.

## Consistency Checklist

Before constructing the registration body, you can self-check against this list:

- [ ] Device declaration ↔ UA ↔ `x-common-params-v2` ↔ later collection: all four consistent;
- [ ] `version_name` / `version_code` consistent with the request headers and query;
- [ ] `license_id` matches the target App version;
- [ ] `openudid` / `cdid` / `boot_time_ms` / `app_start_ms` are fixed;
- [ ] `is_vpn` consistent with the transport layer and the Perseus `vpn` field;
- [ ] The Medusa clock group is established, and `elapsed` is monotonic thereafter.

<div class="callout warn"><span class="callout-title">⚠️ The Most Easily Overlooked Item</span>
`license_id`. It looks like just a constant, but the source explicitly says "an error invalidates the entire chain". On version upgrades, verify this value first.
</div>

## Study Questions

1. Why must the registration body contain both the device declaration and the identity seeds? How do their roles differ?
2. If `is_vpn` disagrees with the transport layer, where would it surface?
3. Why does `license_id` cause "whole-chain failure" rather than a single-point failure?

> 👉 Next section: [3.4 sec_device_token and SDI Token](./04_tokens.md)
