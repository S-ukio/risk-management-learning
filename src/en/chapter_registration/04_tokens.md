# 3.4 sec_device_token and SDI Token

> 🎯 *"Two tokens, two lifecycles."*

## Comparison

| Token | Issuer | Lifecycle | Role | Consequence of invalidation |
|---|---|---|---|---|
| `sec_device_token` | Server (after registration / activation) | Long-term, device-level | Device signing credential; participates in the Perseus / Medusa context | Search-type APIs are most likely downweighted |
| SDI token | Issued by MSSDK | Short-lived, requires refresh | Short-lived collection credential | Collection chain fails |

## `sec_device_token`

The source explains:

> `sec_device_token` is a device-level signing credential issued by the server after registration / activation. It is valid long-term and participates in the Perseus / Medusa context. If acquisition fails, the chain can continue in a downgraded form (some APIs tolerate its absence), but search-type APIs are very likely to be downweighted.

Key points:

- **Device-level**: bound to `device_id`, not install-level;
- **Long-term**: does not need refreshing on every request;
- **Participates in the context**: Perseus / Medusa consume it;
- **Downgradable**: some APIs can continue without it, but search is downweighted.

## SDI Token

The source explains:

> SDI token (issued by MSSDK): a short-lived collection credential that must be refreshed periodically. The caching mechanism supports recovery from historical sessions, and recovery requires validating that `app_id` matches.

Key points:

- **Short-lived**: it expires and must be refreshed;
- **Collection credential**: used for the SDI collection chain;
- **Cache-recoverable**: can be recovered from historical sessions;
- **Validates `app_id`**: recovery must confirm it is the same App; it cannot be reused across Apps.

## Persistence Granularity

The source's summary:

> The persistence granularity of both is "device + App version"; after changing the version number, the token system must be rebuilt.

This means:

- You cannot cache by `device_id` alone;
- Nor by App name alone;
- You must cache by the **device + App version** combination;
- After a version upgrade, old tokens cannot continue to be used.

## State Container Design

If the two kinds of token are placed in the same state container, it can be designed like this:

```text
TokenStore
├─ sec_device_token
│    key = device_id
│    value = token + issued_at
│
└─ sdi_token
     key = device_id + app_version
     value = token + app_id + expires_at
```

The corresponding read rules:

1. `sec_device_token` is read by `device_id` and reused long-term;
2. SDI token is read by `device_id + app_version` and refreshed after expiry;
3. SDI recovery validates `app_id`;
4. When the version changes, clear the SDI cache.

<div class="callout note"><span class="callout-title">🔑 Key Takeaway</span>
Do not merge the two kinds of token into one "token field". Their issuers, lifecycles, cache keys, and invalidation consequences are all different.
</div>

## Common Mistakes

| Mistake | Consequence |
|---|---|
| Re-fetching `sec_device_token` on every request | The server sees the device credential changing frequently |
| Not refreshing an expired SDI token | Collection chain fails |
| Reusing an SDI token across Apps | `app_id` validation fails |
| Continuing to use an old token after a version upgrade | The token system does not match the version |
| Caching only by device without distinguishing versions | Inexplicable failures after an upgrade |

## Study Questions

1. Why is `sec_device_token` device-level, while the SDI token is cached by "device + App version"?
2. When recovering an SDI token from a historical session, why must `app_id` be validated?
3. If `sec_device_token` acquisition fails, which APIs can continue in a downgraded form, and which are most likely downweighted?

> 👉 Next section: [3.5 Nurture and Activation Chains](./05_nurture_chain.md)
