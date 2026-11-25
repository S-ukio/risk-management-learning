# 1.2 七神签名组与明文上下文

> 🎯 *“明文头是声明，签名头是证明。”*

## 七神签名组（算法层）

| 头部 | 作用 | 输入依赖 |
|---|---|---|
| X-Khronos | 秒级时间戳，签名体系的时间锚点 | 当前时间 |
| X-Argus | 核心设备签名，protobuf 加密体 | 设备参数、query、khronos |
| X-Gorgon | 请求级校验签名 | khronos + X-SS-STUB + URL 摘要 |
| X-Ladon | 轻量签名，随 khronos 刷新 | khronos + license_id |
| X-Helios | 辅助校验 | 请求上下文 |
| X-Medusa | 设备状态长帧报告 | 采集器输出、时钟槽、field13 |
| X-Perseus | 设备状态报告 | FL 特征链、KD 进程状态、会话 UUID |

### 怎么记这七个头

可以按“时间 → 设备 → 请求 → 状态”分组：

- **时间锚点**：`X-Khronos`，所有签名头的公共输入。
- **设备身份**：`X-Argus`（核心设备签名）、`X-Ladon`（轻量、随 khronos 刷新）。
- **请求绑定**：`X-Gorgon`（与 body / URL 绑定最强）、`X-Helios`（辅助校验）。
- **状态报告**：`X-Medusa`（长帧设备状态）、`X-Perseus`（FL / KD 报告）。

> 📌 原文没有展开 `X-Argus`、`X-Ladon`、`X-Helios` 的内部算法，本笔记也不补猜；重点放在 Medusa、Perseus、Gorgon 三个有详细拆解的头。

## 风控上下文组（明文层）

| 头部 | 作用 |
|---|---|
| X-SS-STUB | 请求体 MD5（hex），Gorgon 的输入之一 |
| X-SS-REQ-TICKET | 请求票据，单调递增 |
| X-Tt-Dt / X-Tt-Store-Region | 分发与存储区域 |
| sdk-version / x-tt-request-tag | SDK 与请求标签 |

这些头不加密，服务端可以直接读。它们的作用是**声明**：我是什么版本、我来自哪个区域、我的请求体摘要是什么、我的票据走到哪了。

## 声明与证明的关系

原文的总结非常精炼：

> 服务端先读声明，再用签名头反推解密，验证声明与签名内部数据是否一致。声明与证明不符是比算错签名更常见的风控命中原因。

可以把服务端的验证拆成三步：

1. **读声明**：从明文头、query、UA、`x-common-params-v2` 里读出版本、设备、区域、body 摘要。
2. **验证明**：用签名头（Gorgon / Medusa / Perseus 等）反推或重算，得到签名内部的数据。
3. **交叉比对**：声明与证明是否一致？同一事实的多份编码（例如 SDI 与 dtrait）是否一致？

<div class="callout warn"><span class="callout-title">⚠️ 常见误区</span>
“每个头都能单独算对”不等于“请求合法”。服务端比对的是一致性，而不是单点正确性。
</div>

## 一个具体的例子

假设你改了请求体：

- `body` 变了；
- `X-SS-STUB` 没更新；
- `X-Gorgon` 用旧的 STUB 计算。

结果：

- Gorgon 算法本身可能完全正确；
- 但服务端重算 `X-SS-STUB` 时发现与 body 不匹配，直接判定请求被篡改。

这就是“声明与证明不符”的典型场景。

## 思考题

1. 七个签名头里，哪个与“这条请求”的绑定最强？为什么？
2. 为什么 `X-Khronos` 是所有签名头的公共输入，而不是各自取时间？
3. 如果 `X-SS-REQ-TICKET` 不单调，可能说明什么问题？

> 👉 下一节：[1.3 本地 SDK 组件对应关系](./03_sdk_components.md)
