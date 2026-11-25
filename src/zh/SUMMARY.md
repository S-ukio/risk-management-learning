# 某音 App 风控参数解析

[前言](./preface.md)
[阅读指南](./reading-guide.md)

---

- [第一部分：风控体系](./part1.md)

- [第1章 风控体系总览](./chapter_overview/README.md)
  - [1.1 三层风控模型](./chapter_overview/01_layers.md)
  - [1.2 七神签名组与明文上下文](./chapter_overview/02_signature_headers.md)
  - [1.3 本地 SDK 组件对应关系](./chapter_overview/03_sdk_components.md)
  - [1.4 版本演进：39.4 → 41.2](./chapter_overview/04_version_evolution.md)

---

- [第二部分：设备身份与指纹](./part2.md)

- [第2章 设备身份与指纹体系](./chapter_identity/README.md)
  - [2.1 设备标识四件套](./chapter_identity/01_four_ids.md)
  - [2.2 静态指纹：机型模板](./chapter_identity/02_static_fingerprint.md)
  - [2.3 动态指纹：SDI/MSSDK 采集器](./chapter_identity/03_dynamic_collectors.md)
  - [2.4 加密指纹载体](./chapter_identity/04_encrypted_carriers.md)
  - [2.5 指纹与风控决策](./chapter_identity/05_risk_decision.md)

---

- [第三部分：注册与信任](./part3.md)

- [第3章 设备注册流程](./chapter_registration/README.md)
  - [3.1 冷启动时序与时钟基准](./chapter_registration/01_cold_start_clock.md)
  - [3.2 注册链路分解](./chapter_registration/02_register_chain.md)
  - [3.3 注册明文体结构](./chapter_registration/03_register_payload.md)
  - [3.4 sec_device_token 与 SDI token](./chapter_registration/04_tokens.md)
  - [3.5 养号与激活链路](./chapter_registration/05_nurture_chain.md)
  - [3.6 TrustChain 预热](./chapter_registration/06_trustchain.md)

---

- [第四部分：请求与签名](./part4.md)

- [第4章 核心请求参数拆解](./chapter_params/README.md)
  - [4.1 x-common-params-v2](./chapter_params/01_common_params.md)
  - [4.2 X-Khronos 与 suite 对齐](./chapter_params/02_khronos.md)
  - [4.3 X-Medusa：两代链路与 field13](./chapter_params/03_medusa.md)
  - [4.4 f17 时钟槽、会话结构与八分支疑问](./chapter_params/04_medusa_clock.md)
  - [4.5 X-Perseus：FL 特征链](./chapter_params/05_perseus_fl.md)
  - [4.6 X-Perseus：KD、校验和与 protobuf](./chapter_params/06_perseus_state.md)
  - [4.7 X-Gorgon](./chapter_params/07_gorgon.md)
  - [4.8 版本差异与实现约束](./chapter_params/08_version_matrix.md)

---

- [第五部分：复盘与延伸](./part5.md)

- [第5章 复盘、疑问与边界](./chapter_reflection/README.md)
  - [5.1 实验复盘：400 台设备与 85%](./chapter_reflection/01_experiment_review.md)
  - [5.2 待研究问题清单](./chapter_reflection/02_open_questions.md)
  - [5.3 合规、伦理与研究边界](./chapter_reflection/03_ethics.md)

---

- [附录 A：术语表](./appendix/glossary.md)
- [附录 B：参数与版本速查](./appendix/quick_reference.md)
- [附录 C：来源、缺图与引用说明](./appendix/sources.md)
