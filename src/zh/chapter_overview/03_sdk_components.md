# 1.3 本地 SDK 组件对应关系

> 🎯 *“这些库共享同一个进程内状态。”*

## 四个核心组件

签名头不是凭空出现的，它们由 App 内一组 native 库生成。原文给出的对应关系如下：

| SDK 库 | 职责 | 对应输出 |
|---|---|---|
| `libmetasec_ml.so`（MSSDK） | 设备采集、token 下发、七神签名 | X-Gorgon / X-Ladon / SDI token / Perseus |
| `libbdsword.so` | SwordCipher，stats_collect 编码 | app_log / stats 数据体 |
| `libbdbadger.so`（v4.0） | BadgerCipher、dtrait 表单 | `dtrait_pk1` |
| ttNet / Cronet | 网络传输栈 | TLS 指纹、HTTP/2、cronet 版本号 |

### MSSDK（`libmetasec_ml.so`）

这是最核心的库，负责：

- 设备信息采集；
- token 下发（SDI token）；
- 七神签名（至少包括 Gorgon、Ladon、Perseus）。

它不是一个“纯函数库”，而是带有内部状态的运行时：启动时初始化种子、维护时钟、缓存 token、保存会话 UUID。

### Sword（`libbdsword.so`）

负责 `SwordCipher` 与 `stats_collect` 编码，输出 `app_log` / `stats` 数据体。

它对应的是“行为层”的上报：首启埋点、页面事件、曝光事件等。

### Badger（`libbdbadger.so`，v4.0）

负责 `BadgerCipher` 与 `dtrait` 表单，输出 `dtrait_pk1`。

`dtrait` 是设备信息的另一种结构化编码。原文特别强调：它与 SDI 是**同一事实的两份独立编码**，服务端可以交叉比对一致性。这也是为什么两套算法都必须完整复现，而不能只做一份。

### ttNet / Cronet

负责网络传输，决定：

- TLS 指纹；
- HTTP/2 行为；
- cronet 版本号。

这一层不生成签名头，但它决定了“这条链路像不像真实客户端”。

## 共享进程状态

原文有一句非常关键的话：

> 这些库共享同一个进程内状态——时钟起点、会话 UUID、KD 存储、token 缓存。模拟时如果各头各算各的、不共享状态，即使每个头单独看都合法，组合起来也会被判异常。

可以把它整理成一张“状态表”：

| 状态 | 谁维护 | 谁消费 | 生命周期 |
|---|---|---|---|
| 时钟起点 | MSSDK | Medusa f17、Perseus sts | 进程 / 会话 |
| 会话 UUID | MSSDK | Medusa、Perseus | 会话首请求生成，会话内固定 |
| KD | MSSDK | Perseus 校验和 | 进程内共享，跨请求持久化 |
| token 缓存 | MSSDK | SDI / Perseus | 设备 + App 版本 |
| 启动种子 | MSSDK | Perseus FL | SDK 启动时生成 |

## 对模拟实现的含义

如果你按“每个头一个独立函数”的方式实现，通常会遇到三类问题：

1. **时间不一致**：各头各自取当前时间，毫秒级差异导致签名不匹配。
2. **会话不一致**：每次请求重新生成 session_uuid，服务端看到“同一设备不断换会话”。
3. **状态不一致**：KD 每次请求独立生成，校验和的时序特征暴露。

正确的心智模型是：**一个进程内有一个共享的 SDK 状态，所有头都从它派生**。

<div class="callout note"><span class="callout-title">🔑 关键结论</span>
先设计状态容器，再实现算法。状态的生命周期（进程 / 会话 / 请求）决定了哪些值必须持久化、哪些值必须逐请求更新。
</div>

## 思考题

1. 为什么 `libbdsword.so` 和 `libbdbadger.so` 的输出要交叉比对？只做一份会怎样？
2. 如果把 MSSDK 当成无状态纯函数库，最先暴露的是哪一类特征？
3. Cronet 层不生成签名头，为什么仍然属于风控的一部分？

> 👉 下一节：[1.4 版本演进：39.4 → 41.2](./04_version_evolution.md)
