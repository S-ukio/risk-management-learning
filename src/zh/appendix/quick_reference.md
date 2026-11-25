# 附录 B：参数与版本速查

> 只收录原文明确出现过的值。标注「推导」的条目不是原文结论。

## 1. 头部速查

| 头部 | 类型 | 关键输入 / 作用 |
|---|---|---|
| `X-Khronos` | 签名 | 时间锚点；41.1 起决定 field13 分支 |
| `X-Argus` | 签名 | 设备参数、query、khronos |
| `X-Gorgon` | 签名 | khronos + STUB + URL 摘要 + 上下文 |
| `X-Ladon` | 签名 | khronos + license_id |
| `X-Helios` | 签名 | 请求上下文 |
| `X-Medusa` | 签名 | 采集输出、时钟槽、field13 |
| `X-Perseus` | 签名 | FL、KD、session_uuid |
| `X-SS-STUB` | 明文 | body MD5（hex） |
| `X-SS-REQ-TICKET` | 明文 | 单调递增票据 |
| `X-Tt-Dt` / `X-Tt-Store-Region` | 明文 | 分发 / 存储区域 |
| `sdk-version` / `x-tt-request-tag` | 明文 | SDK / 请求标签 |

## 2. 设备标识速查

| 标识 | 生成方 | 生命周期 | 约束 |
|---|---|---|---|
| `device_id` | 服务端 | 设备级，长期 | 14～19 位纯数字 |
| `iid` | 服务端 | 安装级 | 注册返回 |
| `openudid` | 客户端 | 设备级 | 首次上报后固定 |
| `cdid` | 客户端 | 安装级 | UUID 大写 |
| `sec_device_token` | 服务端 | 设备级，长期 | 参与 Perseus / Medusa |
| SDI token | MSSDK | 短周期 | 按 `device_id + app_version` 缓存 |

## 3. 注册链路

```text
1. device_register  → device_id / iid（klink.amemv.com）
2. device_report    → Perseus 设备报告
3. app_log          → 首启埋点（Sword 编码，不含指纹结果）
4. get_token        → SDI token
5. activate / activate_record
6. birth()          → 养号链路
```

时钟约束：

```text
boot_time ≤ first_launch ≤ app_start ≤ 请求时刻
```

## 4. 风控状态

| 状态 | 含义 | 是否可用（`search_ok`） |
|---|---|---|
| `success` | 有结果 | ✅ |
| `empty` | 正常空页 | ✅ |
| `blocked` | 验证 / 限流 | ❌ |
| `error` | 请求 / 响应异常 | ❌ |

## 5. field13 速查

```text
msg52 = query_sm3(32B) || body_md5(16B) || khronos_le(4B)
```

| 项 | 旧版 ≤40.x | 新版 41.1/41.2 |
|---|---|---|
| slot | 52B 内容混合 → 低 4 位 | `(khronos ^ 52) & 15` |
| 族数 | 3 | 4 |
| 族分派 | `slot % 3` | `slot & 3` |
| 族 | SHA-256 / Whirlpool / MD5 | SHA-256 / Whirlpool / BLAKE2b / MD5 |
| 组装 | 直接 20B | 32B → 16B core + 4B 尾 → 20B |
| 常数 | 静态表 | khronos 旋转派生 |

> 🧮 推导：若 suite1（`khronos & 7 == 1`）与新版 field13 同时生效，则 `slot ∈ {5, 13}`，`slot & 3 == 1`。待实测验证。

## 6. 八分支速查

| slot | 形态 | 特征 |
|---|---|---|
| 0 | 魔改 AES-CBC（2 轮） | S-box 异或 `0x3d` |
| 1 | 魔改 AES-CBC（2 轮） | S-box 异或 `0x33` |
| 2 | 魔改 AES-CBC（2 轮） | S-box 异或 `0x3b` |
| 3 | 魔改 AES-CBC（2 轮） | S-box 异或 `0x39` |
| 4 | 仿射 SPN（24 轮） | 固定仿射参数表 |
| 5 | 第二虚拟机核 | 主状态生成 + 两次 24 轮归约 |
| 6 | 魔改 SM4（24 轮） | S-box 异或 `0x17` |
| 7 | 魔改 SM4（24 轮） | S-box 异或 `0x1f` |

> ⚠️ 该表与 field13 的 16 分支描述冲突；归属待核对，见 5.2 Q1。
>
> 正向 19B → 32B MAC，逆向 32B → 19B；AES/SM4 分支补 13 个 `0x0d`。

## 7. Perseus 速查

FL 结构：

```text
"0|0|c0|c1|c2|c3|c4|0|0|thread_word"
```

示例向量：

```text
seed = 45884766, k = 418, flags = 511, chain_flags = 3
chain = [45884668, 4230265858, 2147978368, 974138666, 3197775088]
thread_word = 482472847
chain[0] - seed = 98 (0x62)
```

校验和：

```text
pd, fkd = F(session_uuid, kd)
```

示例：`kd=0`，`session_uuid=861775c1-...` → `pd=815239457`，`fkd=2665330607`。

## 8. 魔法数字

| 值 | 含义 | 出处 |
|---|---|---|
| `52` | field13 输入长度 / slot 异或常量 | 4.3 |
| `15` | slot 掩码 | 4.3 |
| `3` | 旧版族数 / `chain_flags` 值 | 4.3 / 4.5 |
| `4` | 新版族数 | 4.3 |
| `0x0000` | Gorgon SEED | 4.7 |
| `0x0d` | AES/SM4 分支补齐字节（13 个） | 4.4 |
| `1588093228` | 41.x 抖音 `license_id` | 3.3 |
| `1` | suite1 的 `ts & 7` 结果 | 4.2 |
| `85%` | 原文报告的成功率 | 5.1 |

> 📌 魔法数字只用于速查，具体上下文请回到对应章节。
