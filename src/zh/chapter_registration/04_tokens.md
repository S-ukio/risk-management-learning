# 3.4 sec_device_token 与 SDI token

> 🎯 *“两个 token，生命周期不同。”*

## 对比

| Token | 签发方 | 生命周期 | 作用 | 失效后果 |
|---|---|---|---|---|
| `sec_device_token` | 服务端（注册 / 激活后） | 长期，设备级 | 设备签名凭证，参与 Perseus / Medusa 上下文 | 搜索类接口大概率降权 |
| SDI token | MSSDK 下发 | 短周期，需刷新 | 短周期采集凭证 | 采集链路失效 |

## `sec_device_token`

原文的说明：

> `sec_device_token` 是注册 / 激活后服务端签发的设备级签名凭证，长期有效，参与 Perseus / Medusa 上下文。获取失败时链路可降级继续（部分接口容忍缺失），但搜索类接口大概率降权。

关键点：

- **设备级**：与 `device_id` 绑定，不是安装级；
- **长期**：不需要每个请求刷新；
- **参与上下文**：Perseus / Medusa 会消费它；
- **可降级**：缺失时部分接口仍可继续，但搜索会降权。

## SDI token

原文的说明：

> SDI token（MSSDK 下发）：短周期采集凭证，需要按周期刷新。缓存机制支持从历史会话恢复，恢复时需校验 `app_id` 匹配。

关键点：

- **短周期**：会过期，需要刷新；
- **采集凭证**：用于 SDI 采集链路；
- **可缓存恢复**：可以从历史会话恢复；
- **校验 `app_id`**：恢复时必须确认是同一个 App，不能跨 App 混用。

## 持久化粒度

原文的总结：

> 两者的持久化粒度都是“设备 + App 版本”，换版本号后 token 体系需要重建。

这意味着：

- 不能只按 `device_id` 缓存；
- 也不能只按 App 名缓存；
- 必须按 **设备 + App 版本** 组合缓存；
- 版本升级后，旧 token 不能继续使用。

## 状态容器设计

如果把两类 token 放进同一个状态容器，可以这样设计：

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

对应的读取规则：

1. `sec_device_token` 按 `device_id` 读取，长期复用；
2. SDI token 按 `device_id + app_version` 读取，过期后刷新；
3. SDI 恢复时校验 `app_id`；
4. 版本变化时，清空 SDI 缓存。

<div class="callout note"><span class="callout-title">🔑 关键结论</span>
不要把两类 token 混成一个“token 字段”。它们的签发方、生命周期、缓存键、失效后果都不同。
</div>

## 常见错误

| 错误 | 后果 |
|---|---|
| 每个请求重新获取 `sec_device_token` | 服务端看到设备凭证频繁变化 |
| SDI token 过期不刷新 | 采集链路失败 |
| 跨 App 复用 SDI token | `app_id` 校验失败 |
| 版本升级后继续用旧 token | token 体系与版本不匹配 |
| 只按设备缓存，不区分版本 | 升级后出现不可解释的失败 |

## 思考题

1. 为什么 `sec_device_token` 是设备级，而 SDI token 要按“设备 + App 版本”缓存？
2. SDI token 从历史会话恢复时，为什么必须校验 `app_id`？
3. 如果 `sec_device_token` 获取失败，哪些接口可以降级继续，哪些大概率降权？

> 👉 下一节：[3.5 养号与激活链路](./05_nurture_chain.md)
