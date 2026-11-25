# 3.1 冷启动时序与时钟基准

> 🎯 *“必须在首个请求前确定并全程一致。”*

## 为什么时钟是注册的前提

注册请求的合法性依赖一组时钟基准。原文的要求是：

> 注册请求的合法性依赖一组时钟基准，必须在首个请求前确定并全程一致。

原因不难理解：

- Medusa 的 f17 时钟槽要求单调；
- Perseus 的 `sts`、`do` 等字段与启动时长有关；
- 签名头的 `X-Khronos` 需要一个稳定的时间锚点；
- 注册体里还要预埋 `medusa_clock_origin` / `medusa_session_ms` / `medusa_elapsed_ms` / `medusa_session_uuid`。

如果每个组件各自取时间，就会出现“同一请求内多个时间基准”的矛盾。

## 已知的交叉关系

原文给出了一个明确的不等式：

```text
boot_time ≤ first_launch ≤ app_start ≤ 请求时刻
```

含义：

| 值 | 含义 |
|---|---|
| `boot_time` | 设备启动时间 |
| `first_launch` | App 首次启动时间 |
| `app_start` | 当前进程启动时间 |
| 请求时刻 | 发出请求的时间 |

任何一个倒置，都是明显异常。例如：

- `app_start` 早于 `first_launch`：当前进程不可能在 App 首次启动之前启动；
- 请求时刻早于 `app_start`：请求不可能在进程启动之前发出；
- `first_launch` 早于 `boot_time`：App 不可能在设备启动之前启动。

## 原文缺失的部分

<span class="badge gap">原文缺图</span> 原文在此处写的是：

> 注册请求的合法性依赖一组时钟基准，必须在首个请求前确定并全程一致：
>
> - 这些值的交叉关系是：`boot_time ≤ first_launch ≤ app_start ≤ 请求时刻`。

冒号后的“这组时钟基准”列表在提取页面中为空，且没有对应图片。**本笔记不补猜具体字段名**，只保留已知的不等式与注册体中明确出现的 Medusa 时钟组。

待确认的问题：

- 这组基准具体包含哪些值？是否就是注册体中的 `boot_time_ms` / `app_start_ms`？
- `first_launch` 与 `app_start` 是否分别对应不同的字段？
- 服务端允许的偏差范围是多少？

见[待研究问题清单](../chapter_reflection/02_open_questions.md)。

## Medusa 时钟组

注册体中明确出现了四个 Medusa 时钟字段：

| 字段 | 作用 |
|---|---|
| `medusa_clock_origin` | 会话时钟起点 |
| `medusa_session_ms` | 会话内累计毫秒 |
| `medusa_elapsed_ms` | 已流逝毫秒 |
| `medusa_session_uuid` | 会话 UUID |

原文的说明：

> 注册阶段就要建立会话时钟状态，供后续 Medusa 报告复用。

这意味着：

- 时钟起点不是每次请求现取的；
- 它在注册阶段就被“钉住”；
- 后续请求的 `elapsed` 必须单调增长；
- `session_uuid` 在会话首请求生成并固定。

## 时钟状态的正确心智模型

```text
进程启动
  │
  ├─ 生成 SDK 种子
  ├─ 钉住 clock_origin
  ├─ 生成 session_uuid
  │
  ├─ 注册请求：携带 clock_origin / session_ms / elapsed / uuid
  │
  ├─ 后续请求 1：elapsed = now - clock_origin
  ├─ 后续请求 2：elapsed 必须 ≥ 上一次
  └─ ...
```

<div class="callout warn"><span class="callout-title">⚠️ 常见错误</span>
每次请求重新取 `clock_origin`，或者让 `elapsed` 回退。前者会让“会话起点”不断漂移，后者直接违反单调性。
</div>

## 思考题

1. 为什么 `boot_time` 必须早于 `first_launch`？如果设备时钟被回拨，会发生什么？
2. `medusa_clock_origin` 应该在什么时刻确定？进程启动、App 启动，还是首个请求？
3. 如果 `elapsed` 在两个请求之间回退，服务端能据此推断出什么？

> 👉 下一节：[3.2 注册链路分解](./02_register_chain.md)
