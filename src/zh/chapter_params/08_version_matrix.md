# 4.8 版本差异与实现约束

> 🎯 *“版本号不是装饰，而是一套算法配置的开关。”*

## 总览矩阵

| 组件 / 维度 | 旧版 ≤40.x | 新版 41.1 / 41.2 |
|---|---|---|
| Medusa 帧 | 短帧 | v412 长帧 |
| Medusa 流水线 | 异或流 → 种子异或 → 魔改 AES → 帧封装 | 长帧封装 |
| field13 slot | 52B 内容混合，取低 4 位 | `(khronos ^ 52) & 15` |
| field13 族数 | 3 族（SHA-256 / Whirlpool / MD5） | 4 族（+ BLAKE2b） |
| 族分派 | `slot % 3` | `slot & 3` |
| 分支常数 | 每分支静态常数表 | 由 khronos 旋转派生 |
| 摘要组装 | 直接 20B | 32B 折叠 16B core + 4B 尾 |
| Perseus | 未启用 | 启用（FL + KD） |
| 外层检查字 | 无 | 有（query SM3 低位 + field13 低位） |

## 版本是全局开关

原文：

> 41.1.0 起的版本配置同时决定了 Medusa 与 Perseus 走哪套链路。

这意味着版本配置至少影响：

1. Medusa 用短帧还是长帧；
2. field13 用内容选分支还是 khronos 选分支；
3. field13 用三族还是四族；
4. 常数是静态表还是运行时派生；
5. Perseus 是否启用、FL / KD 怎么走；
6. 是否有外层检查字。

所以，版本号不能只作为 query 里的一个字符串，而应该映射到一个**完整的算法配置对象**。

## 实现约束

### 1. 一个会话，一套配置

```text
Session
├─ app_version: "41.2.0"
├─ algorithm_profile: V412
├─ medusa: long_frame
├─ field13: khronos_driven
├─ perseus: enabled
└─ constants: runtime_derived
```

会话开始时确定，会话内不切换。

### 2. 不要跨版本复用向量

旧版的示例向量不能用来验证新版的实现：

- slot 选择不同；
- 族不同；
- 常数不同；
- 输出组装不同。

### 3. 回归测试要按版本分组

| 测试组 | 覆盖 |
|---|---|
| ≤40.x | 短帧、内容选分支、三族、直接 20B |
| 41.1/41.2 | 长帧、khronos 选分支、四族、折叠 + 尾 |

不要用同一组断言跑两个版本。

### 4. 常数要记录来源

- 静态常数表：记录版本、分支号；
- 运行时派生常数：记录 khronos、派生规则；
- 否则出现不一致时无法定位是“常数错”还是“输入错”。

## 常见失败模式

| 失败模式 | 现象 | 根因 |
|---|---|---|
| 版本与算法不匹配 | 签名重算不一致 | 请求声明 41.2，field13 用旧版 |
| khronos 非法 | 签名被拒 | 未满足 suite1 的 `ts & 7 == 1` |
| body / STUB 不同步 | Gorgon 校验失败 | 改了 body 没更新 STUB |
| KD 每请求生成 | Perseus 校验和时序异常 | 未做进程内共享 |
| session_uuid 重置 | 会话状态异常 | 每请求重新生成 |
| token_address 独立随机 | 环境检测异常 | 未与 module_base 保持偏移 |
| license_id 错误 | 全链路失效 | 版本常量填错 |
| 时钟回退 | f17 单调性失败 | elapsed 未持久化 |

## 验收清单

在认为“已经对齐”之前，逐项确认：

- [ ] 版本配置固定，会话内不切换；
- [ ] Medusa 与 Perseus 使用同一套版本配置；
- [ ] field13 的 slot、族、组装与版本匹配；
- [ ] khronos 在 suite1 场景满足低 3 位约束；
- [ ] body、STUB、Gorgon 三者同步；
- [ ] KD 进程内共享、按 aid 隔离、重启可恢复；
- [ ] session_uuid 会话内固定；
- [ ] token_address 与 module_base 保持偏移关系；
- [ ] license_id 与目标 App 版本匹配；
- [ ] 时钟单调、不回退、不重复；
- [ ] 用对应版本的示例向量做过逐字节验证。

<div class="callout warn"><span class="callout-title">⚠️ 最重要的一条</span>
不要用“单个头算对了”来判断成功。服务端验证的是组合一致性；一个版本配置错误会让所有头一起失效。
</div>

## 思考题

1. 为什么“版本配置”要同时控制 Medusa 和 Perseus，而不是各自独立？
2. 如果只做旧版、不做新版，最快会在哪个版本上失败？
3. 验收清单里，哪一项最容易在“看起来都对了”的情况下被忽略？

> 👉 下一章：[第5章 复盘、疑问与边界](../chapter_reflection/README.md)
