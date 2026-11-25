# 4.1 x-common-params-v2

> 🎯 *“UA 之外的另一份设备 / 版本声明。”*

## 它是什么

原文的定义：

> 30 键固定结构的公共参数，UA 之外的另一份设备 / 版本声明。

它通常出现在 query 或公共参数里，包含设备、版本、系统、语言、时区等信息。原文列出的核心键包括：

```text
aid / app_name / channel / version_code / version_name / device_platform
device_type / device_brand / device_id / iid / openudid / cdid
os_version / os_api / resolution / dpi / language / tz
first_launch_timestamp / _rticket / cdid / host_abi / cpu_support64
...
```

> 📌 原文以代码块形式列出，实际是 30 个键的固定结构；上面是其中可读的核心键。完整键表需要在后续版本中补齐。

## 一致性约束

原文的总结：

> 约束：与 UA、注册体、query 参数三处完全一致。

可以画成一张“同一事实、四处声明”的表：

| 事实 | 注册体 | UA | `x-common-params-v2` | query |
|---|---|---|---|---|
| 机型 / 品牌 | ✓ | ✓ | ✓ | ✓ |
| 系统版本 / API | ✓ | ✓ | ✓ | ✓ |
| App 版本 | ✓ | ✓ | ✓ | ✓ |
| 分辨率 / dpi | ✓ | — | ✓ | ✓ |
| device_id / iid | ✓ | — | ✓ | ✓ |

任何一处不同，都会被服务端交叉比对发现。

## `version_name` 的显式校验

原文特别指出：

> version_name 在签名入口有显式校验——query 声明的版本与设备模板版本不符时直接拒绝签名（避免生成自相矛盾的请求）。

这句话有两层含义：

1. **校验发生在签名入口**，不是业务层；
2. 目的是**避免生成自相矛盾的请求**——如果版本声明不一致，签名本身就没有意义。

实践含义：

- 不要只改 query 里的 `version_name`，而忘了设备模板；
- 也不要把设备模板升级了，却继续用旧版本的 query；
- 版本是全局配置，不是单个字段。

## 30 键结构的工程含义

固定结构意味着：

- 键的顺序、数量、命名都可能是校验点；
- 少一个键、多一个键、改一个键名，都可能被识别；
- 不能把它当成“随手拼的 query”。

建议把它当作一个**结构体**来维护：

```text
CommonParams
├─ app: aid, app_name, channel, version_code, version_name
├─ device: device_platform, device_type, device_brand, device_id, iid
├─ identity: openudid, cdid
├─ system: os_version, os_api, resolution, dpi, language, tz
├─ time: first_launch_timestamp, _rticket
└─ cpu: host_abi, cpu_support64
```

## 自查清单

- [ ] 30 个键齐全，命名与顺序稳定；
- [ ] `version_name` / `version_code` 与设备模板、注册体一致；
- [ ] `device_id` / `iid` 与注册结果一致；
- [ ] `resolution` / `dpi` 与静态指纹一致；
- [ ] `os_version` / `os_api` 与 ROM 声明一致；
- [ ] `first_launch_timestamp` 与时钟基准一致；
- [ ] `_rticket` 单调递增；
- [ ] `host_abi` / `cpu_support64` 与 ABI / CPU 拓扑一致。

<div class="callout warn"><span class="callout-title">⚠️ 最常见的错误</span>
只对齐 UA 和 query，忘了注册体与 `x-common-params-v2`。服务端比对的是四处，不是两处。
</div>

## 思考题

1. 为什么 `version_name` 的校验要放在签名入口，而不是业务层？
2. 如果 30 键结构少了一个键，可能在哪一层被发现？
3. `_rticket` 单调递增与 `X-SS-REQ-TICKET` 的单调递增，是不是同一件事？

> 👉 下一节：[4.2 X-Khronos 与 suite 对齐](./02_khronos.md)
