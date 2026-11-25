# Douyin App Risk Control: From Device Fingerprints to Request Signatures

[Preface](./preface.md)
[Reading Guide](./reading-guide.md)

---

- [Part 1: Risk Control System](./part1.md)

- [Chapter 1: Risk Control System Overview](./chapter_overview/README.md)
  - [1.1 Three-Layer Risk Control Model](./chapter_overview/01_layers.md)
  - [1.2 Seven Signature Headers and Plaintext Context](./chapter_overview/02_signature_headers.md)
  - [1.3 Local SDK Component Mapping](./chapter_overview/03_sdk_components.md)
  - [1.4 Version Evolution: 39.4 → 41.2](./chapter_overview/04_version_evolution.md)

---

- [Part 2: Device Identity and Fingerprints](./part2.md)

- [Chapter 2: Device Identity and Fingerprint System](./chapter_identity/README.md)
  - [2.1 The Four Device Identifiers](./chapter_identity/01_four_ids.md)
  - [2.2 Static Fingerprint: Device Model Templates](./chapter_identity/02_static_fingerprint.md)
  - [2.3 Dynamic Fingerprint: SDI/MSSDK Collectors](./chapter_identity/03_dynamic_collectors.md)
  - [2.4 Encrypted Fingerprint Carriers](./chapter_identity/04_encrypted_carriers.md)
  - [2.5 Fingerprints and Risk Control Decisions](./chapter_identity/05_risk_decision.md)

---

- [Part 3: Registration and Trust](./part3.md)

- [Chapter 3: Device Registration Flow](./chapter_registration/README.md)
  - [3.1 Cold Start Sequence and Clock Baseline](./chapter_registration/01_cold_start_clock.md)
  - [3.2 Registration Chain Breakdown](./chapter_registration/02_register_chain.md)
  - [3.3 Registration Plaintext Body Structure](./chapter_registration/03_register_payload.md)
  - [3.4 sec_device_token and SDI Token](./chapter_registration/04_tokens.md)
  - [3.5 Nurture and Activation Chains](./chapter_registration/05_nurture_chain.md)
  - [3.6 TrustChain Warm-up](./chapter_registration/06_trustchain.md)

---

- [Part 4: Requests and Signatures](./part4.md)

- [Chapter 4: Core Request Parameter Breakdown](./chapter_params/README.md)
  - [4.1 x-common-params-v2](./chapter_params/01_common_params.md)
  - [4.2 X-Khronos and Suite Alignment](./chapter_params/02_khronos.md)
  - [4.3 X-Medusa: Two Generations and field13](./chapter_params/03_medusa.md)
  - [4.4 f17 Clock Slot, Session Structure, and the Eight-Branch Question](./chapter_params/04_medusa_clock.md)
  - [4.5 X-Perseus: FL Feature Chain](./chapter_params/05_perseus_fl.md)
  - [4.6 X-Perseus: KD, Checksums, and protobuf](./chapter_params/06_perseus_state.md)
  - [4.7 X-Gorgon](./chapter_params/07_gorgon.md)
  - [4.8 Version Differences and Implementation Constraints](./chapter_params/08_version_matrix.md)

---

- [Part 5: Review and Extensions](./part5.md)

- [Chapter 5: Review, Open Questions, and Boundaries](./chapter_reflection/README.md)
  - [5.1 Experiment Review: 400 Devices and 85%](./chapter_reflection/01_experiment_review.md)
  - [5.2 Open Questions](./chapter_reflection/02_open_questions.md)
  - [5.3 Compliance, Ethics, and Research Boundaries](./chapter_reflection/03_ethics.md)

---

- [Appendix A: Glossary](./appendix/glossary.md)
- [Appendix B: Parameters and Versions Quick Reference](./appendix/quick_reference.md)
- [Appendix C: Sources, Source Gaps, and Citations](./appendix/sources.md)
