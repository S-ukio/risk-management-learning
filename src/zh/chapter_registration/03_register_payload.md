# 3.3 注册明文体结构

> 🎯 *“device_register 的请求体是明文 JSON（部分字段 base64）。”*

## 五个分组

原文把 `device_register` 的请求体分成五组：

| 分组 | 作用 | 关键字段 |
|---|---|---|
| 设备声明组 | 声明设备是什么 | `device_type`、`device_brand`、`device_manufacturer`、`device_board`、`device_codename`、`hardware`、`rom`、`resolution`、`dpi` |
| 版本声明组 | 声明 App 与渠道 | `version_name`、`version_code`、`channel`、`license_id` |
| 身份种子组 | 提供本地身份种子 | `openudid`、`cdid`、`boot_time_ms`、`app_start_ms` |
| 环境组 | 声明运行环境 | `is_vpn`、`is_activated`、`register_signal` |
| Medusa 时钟组 | 建立会话时钟 | `medusa_clock_origin`、`medusa_session_ms`、`medusa_elapsed_ms`、`medusa_session_uuid` |

## 设备声明组

必须与 UA、后续采集完全一致。

原文的提醒：

> 必须与 UA、后续采集完全一致。

这意味着同一个事实要出现在至少四处：

1. `device_register` 请求体；
2. UA；
3. `x-common-params-v2`；
4. 后续 SDI / dtrait 采集结果。

任何一处不同，都会被交叉比对发现。

## 版本声明组

| 字段 | 说明 |
|---|---|
| `version_name` | App 版本名，例如 `41.2.0` |
| `version_code` | 版本号，例如 `410200` |
| `channel` | 渠道 |
| `license_id` | 各 App 的固定常数 |

原文特别指出：

> `license_id` 是各 App 的固定常数（抖音 41.x 为 `1588093228` 系），错误即全链路失效。

也就是说，`license_id` 不是“随便填一个数字”，而是整个签名体系的常量之一。填错会导致全链路失败，而不只是某一个头失败。

## 身份种子组

| 字段 | 说明 |
|---|---|
| `openudid` | 本地生成，设备级 |
| `cdid` | 本地生成，安装级，UUID 大写 |
| `boot_time_ms` | 设备启动时间（毫秒） |
| `app_start_ms` | App 启动时间（毫秒） |

原文的说明：

> 本地生成，一旦注册成功即固定，后续请求全部复用。

这四者是“种子”：注册成功后不再变化，后续请求全部引用。

## 环境组

| 字段 | 说明 |
|---|---|
| `is_vpn` | 是否使用 VPN |
| `is_activated` | 是否已激活 |
| `register_signal` | 注册信号 |

原文的提醒：

> VPN 状态必须真实反映传输层，本地检测结果应同步到注册体与 Perseus 源的 vpn 字段。

含义：

- 如果传输层走了 VPN，`is_vpn` 必须为真；
- 注册体的 `is_vpn` 与 Perseus 源里的 `vpn` 字段必须一致；
- 不能“注册体说没开 VPN，Perseus 说开了”。

## Medusa 时钟组

| 字段 | 说明 |
|---|---|
| `medusa_clock_origin` | 会话时钟起点 |
| `medusa_session_ms` | 会话内累计毫秒 |
| `medusa_elapsed_ms` | 已流逝毫秒 |
| `medusa_session_uuid` | 会话 UUID |

原文的说明：

> 注册阶段就要建立会话时钟状态，供后续 Medusa 报告复用。

## 一致性检查清单

在构造注册体之前，可以按这张表自查：

- [ ] 设备声明 ↔ UA ↔ `x-common-params-v2` ↔ 后续采集，四处一致；
- [ ] `version_name` / `version_code` 与请求头、query 一致；
- [ ] `license_id` 与目标 App 版本匹配；
- [ ] `openudid` / `cdid` / `boot_time_ms` / `app_start_ms` 已固定；
- [ ] `is_vpn` 与传输层、Perseus `vpn` 字段一致；
- [ ] Medusa 时钟组已建立，且 `elapsed` 后续单调。

<div class="callout warn"><span class="callout-title">⚠️ 最容易忽略的一项</span>
`license_id`。它看起来只是一个常数，但原文明确说“错误即全链路失效”。版本升级时，先确认这个值。
</div>

## 思考题

1. 为什么注册体要同时包含设备声明和身份种子？两者的作用有何不同？
2. `is_vpn` 与传输层不一致，会在哪些地方暴露？
3. `license_id` 为什么会导致“全链路失效”，而不是单点失败？

> 👉 下一节：[3.4 sec_device_token 与 SDI token](./04_tokens.md)
