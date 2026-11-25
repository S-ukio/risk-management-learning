# 附录 A：术语表

> 按首字母 / 拼音粗排，便于查阅。

| 术语 | 全称 / 含义 | 备注 |
|---|---|---|
| **Badger** | `libbdbadger.so` 实现的加密组件 | 输出 `dtrait_pk1` |
| **BadgerCipher** | Badger 的加密算法 | 用于 `dtrait` 表单 |
| **cdid** | 客户端生成的安装级标识 | UUID 大写 |
| **Cronet** | Chromium 网络栈 | 影响 TLS / HTTP/2 指纹 |
| **device_id** | 服务端分配的设备级标识 | 14～19 位纯数字 |
| **dtrait** | Badger 表单编码的设备信息 | 与 SDI 交叉验证 |
| **empty** | 请求成功但返回空页 | 新设备冷启正常阶段 |
| **f17** | Medusa 报告中的时钟槽 | 含 `f17_base_ns`、`ticks`、请求序号 |
| **field13** | Medusa 报告中的请求摘要哈希 | 输入 52B，输出 20B |
| **FL** | Perseus 的启动特征链 | 9 元素 + `thread_word` |
| **iid** | 服务端分配的安装级标识 | install_id |
| **KD** | SDK 进程内的键值状态 | 参与 Perseus 会话校验 |
| **khronos** | 秒级时间戳 / 签名时间锚点 | `X-Khronos` 头 |
| **license_id** | App 的固定常量 | 41.x 抖音为 `1588093228` 系 |
| **lp** | Perseus 报告内的路径链 | 生成规则原文未展开 |
| **MSSDK** | `libmetasec_ml.so` 实现的 SDK | 采集、token、七神签名 |
| **Medusa** | 设备状态长帧报告 | `X-Medusa` 头 |
| **msg52** | field13 的 52 字节输入 | `query_sm3(32B) + body_md5(16B) + khronos_le(4B)` |
| **openudid** | 客户端生成的设备级标识 | 首次注册上报 |
| **Perseus** | 41.1 启用的设备报告 | `X-Perseus` 头 |
| **REE / TEE** | 普通世界 / 可信执行环境 | TicketGuard 的两套 P-256 密钥 |
| **SDI** | 设备采集 / token 体系 | SDI body、SDI token |
| **sec_device_token** | 服务端签发的设备级凭证 | 长期有效 |
| **slot** | field13 / 分支算法的索引 | 旧版 0–15，新版由 khronos 决定 |
| **Sword** | `libbdsword.so` 实现的编码 | `SwordCipher`、`stats_collect` |
| **TicketGuard** | P-256 密钥体系 | 每设备 REE / TEE 两套密钥 |
| **TrustChain** | 服务端设备信任积累机制 | pre-register、搜索前预热 |
| **X-Argus** | 核心设备签名头 | protobuf 加密体 |
| **X-Gorgon** | 请求级校验签名头 | 绑定 body / URL / khronos / 上下文 |
| **X-Helios** | 辅助校验头 | 原文未展开 |
| **X-Khronos** | 时间锚点头 | 所有签名头的公共输入 |
| **X-Ladon** | 轻量签名头 | 随 khronos 刷新 |
| **X-Medusa** | 设备状态长帧头 | field13、f17、会话结构 |
| **X-Perseus** | 设备报告头 | FL、KD、protobuf |
| **X-SS-STUB** | 请求体 MD5（hex） | Gorgon 的输入 |
| **X-SS-REQ-TICKET** | 请求票据 | 单调递增 |
| **族（family）** | 哈希分支的分类 | 旧版三族，新版四族 |
| **归一化** | search_field13 的前处理 | 原文未展开 |

> 📌 术语以原文用法为准；本表只做索引，不替代各章节的上下文说明。
