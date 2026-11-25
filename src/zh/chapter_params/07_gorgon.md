# 4.7 X-Gorgon

> 🎯 *“它是七神中与‘这条请求’绑定最强的头，也是防重放的核心。”*

## 输入四元组

原文：

```text
Gorgon = F(khronos, X-SS-STUB(body MD5), URL 摘要, cookie/上下文摘要)
```

四个输入：

| 输入 | 来源 | 作用 |
|---|---|---|
| `khronos` | `X-Khronos` | 时间锚点 |
| `X-SS-STUB` | 请求体 MD5（hex） | 绑定请求体 |
| URL 摘要 | 请求 URL | 绑定目标接口 |
| cookie / 上下文摘要 | 会话上下文 | 绑定会话状态 |

## SEED

原文：

> 实践中 `SEED=0x0000` 与实包对齐。

这是一个实现细节：Gorgon 的种子取 `0x0000` 时，与真实 App 的输出对齐。

> 📌 原文没有给出 `F` 的具体算法与轮次，只给出输入结构和 SEED。本笔记不补猜。

## 它绑定了什么

Gorgon 的作用是把请求内容绑定到签名：

> Gorgon 的作用是把请求内容绑定到签名——body 改一个字节而 STUB 不同步更新，即校验失败。

具体来说：

- body 变 → `X-SS-STUB` 变 → Gorgon 变；
- URL 变 → URL 摘要变 → Gorgon 变；
- khronos 变 → Gorgon 变；
- 会话上下文变 → 上下文摘要变 → Gorgon 变。

四个输入任何一个不同步，Gorgon 就对不上。

## 防重放

原文：

> 它是七神中与“这条请求”绑定最强的头，也是防重放的核心：khronos 过期或复用旧签名均被拒。

两条：

1. **khronos 过期**：旧请求的签名不能在新时间窗口使用；
2. **复用旧签名**：同一个签名不能用于第二个请求。

这就是为什么“抓一个包反复重放”通常会失败：Gorgon 把请求、时间、会话绑在了一起。

## 与 STUB 的关系

`X-SS-STUB` 是请求体 MD5 的十六进制字符串，它是 Gorgon 的输入之一。

一个常见的错误链：

```text
改 body
  │
  ├─ 忘记更新 X-SS-STUB
  │      │
  │      ▼
  │   Gorgon 用的是旧 STUB
  │      │
  │      ▼
  └─ 服务端重算 body MD5 → 与 STUB 不符 → 拒绝
```

注意：即使 Gorgon 算法完全正确，只要 STUB 与 body 不同步，就会失败。

## 自查清单

- [ ] `X-SS-STUB` 与当前 body 的 MD5（hex）一致；
- [ ] `khronos` 未过期，且与 Medusa / Perseus 使用的是同一个值；
- [ ] URL 摘要基于最终请求 URL（包含必要的 query）；
- [ ] cookie / 上下文摘要与会话状态一致；
- [ ] `SEED=0x0000`（与目标版本对齐）；
- [ ] 没有复用旧请求的 Gorgon。

<div class="callout note"><span class="callout-title">🔑 关键结论</span>
Gorgon 是“请求级绑定”的守门员。它不负责设备身份，也不负责状态报告；它只回答一个问题：这个签名是不是为这条请求、这个时间、这个会话生成的？
</div>

## 思考题

1. 为什么 Gorgon 要同时绑定 body、URL、khronos 和上下文，而不是只绑定 body？
2. 如果 body 没变、URL 没变，但 khronos 变了，Gorgon 还能复用吗？
3. `X-SS-STUB` 与 Medusa 的 `body_md5` 是同一个值吗？它们各自服务谁？

> 👉 下一节：[4.8 版本差异与实现约束](./08_version_matrix.md)
