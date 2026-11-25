# Appendix A: Glossary

> Roughly sorted by initial letter / pinyin for easy lookup.

| Term | Full name / meaning | Notes |
|---|---|---|
| **Badger** | Encryption component implemented by `libbdbadger.so` | Outputs `dtrait_pk1` |
| **BadgerCipher** | Badger's encryption algorithm | Used for the `dtrait` form |
| **cdid** | Client-generated install-level identifier | Uppercase UUID |
| **Cronet** | Chromium network stack | Affects TLS / HTTP/2 fingerprints |
| **device_id** | Server-assigned device-level identifier | 14–19 digits |
| **dtrait** | Device information encoded in the Badger form | Cross-validated with SDI |
| **empty** | Request succeeded but returned an empty page | Normal stage during cold start of a new device |
| **f17** | Clock slot in the Medusa report | Contains `f17_base_ns`, `ticks`, request sequence number |
| **field13** | Request digest hash in the Medusa report | 52B input, 20B output |
| **FL** | Perseus startup feature chain | 9 elements + `thread_word` |
| **iid** | Server-assigned install-level identifier | install_id |
| **KD** | Key-value state inside the SDK process | Participates in Perseus session verification |
| **khronos** | Second-level timestamp / signature time anchor | `X-Khronos` header |
| **license_id** | Fixed constant of the App | `1588093228` series for 41.x Douyin |
| **lp** | Path chain in the Perseus report | Generation rules not expanded in the source |
| **MSSDK** | SDK implemented by `libmetasec_ml.so` | Collection, token, Seven Gods signatures |
| **Medusa** | Device-state long-frame report | `X-Medusa` header |
| **msg52** | 52-byte input to field13 | `query_sm3(32B) + body_md5(16B) + khronos_le(4B)` |
| **openudid** | Client-generated device-level identifier | Reported at first registration |
| **Perseus** | Device report enabled in 41.1 | `X-Perseus` header |
| **REE / TEE** | Normal world / Trusted Execution Environment | TicketGuard's two sets of P-256 keys |
| **SDI** | Device collection / token system | SDI body, SDI token |
| **sec_device_token** | Server-issued device-level credential | Long-lived |
| **slot** | Index for field13 / branch algorithms | 0–15 in old versions; determined by khronos in new versions |
| **Sword** | Encoding implemented by `libbdsword.so` | `SwordCipher`, `stats_collect` |
| **TicketGuard** | P-256 key system | Two key sets per device, REE / TEE |
| **TrustChain** | Server-side device trust accumulation mechanism | pre-register, warm-up before search |
| **X-Argus** | Core device signature header | Protobuf-encrypted body |
| **X-Gorgon** | Request-level verification signature header | Bound to body / URL / khronos / context |
| **X-Helios** | Auxiliary verification header | Not expanded in the source |
| **X-Khronos** | Time anchor header | Common input to all signature headers |
| **X-Ladon** | Lightweight signature header | Refreshed with khronos |
| **X-Medusa** | Device-state long-frame header | field13, f17, session structure |
| **X-Perseus** | Device report header | FL, KD, protobuf |
| **X-SS-STUB** | Request body MD5 (hex) | Input to Gorgon |
| **X-SS-REQ-TICKET** | Request ticket | Monotonically increasing |
| **Family (族)** | Classification of hash branches | Three families in old versions, four in new versions |
| **Normalization** | Preprocessing for search_field13 | Not expanded in the source |

> 📌 Terminology follows the usage in the source; this table is an index only and does not replace the contextual explanations in each chapter.
