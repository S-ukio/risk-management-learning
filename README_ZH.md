# 某音 App 风控参数解析

> 从设备指纹到请求签名：一份可继续补充的中英双语学习笔记。

本项目参考 [Haozhe-Xing/agent_learning](https://github.com/Haozhe-Xing/agent_learning) 的组织方式，用 mdBook 把公众号文章《某音App风控参数分析》重新整理为分篇、分章、可导航的学习站。

## 这是什么 / 不是什么

- **是**：对公开文章的结构化抄录、术语统一、版本对照和问题清单；原文缺失处明确标注。
- **不是**：批量注册 / 养号教程，也不是绕过平台风控的操作手册。
- 所有实验仅应在你拥有明确授权的设备、账号与环境中进行。

## 内容结构

| 部分 | 章节 | 主题 |
|---|---|---|
| 第一部分 | 风控体系 | 三层模型、七神签名头、SDK 组件、版本演进 |
| 第二部分 | 设备身份与指纹 | 设备标识四件套、静态/动态指纹、加密载体、决策状态 |
| 第三部分 | 设备注册流程 | 时钟基准、注册链路、注册体、token、养号链路、TrustChain |
| 第四部分 | 核心请求参数 | `x-common-params-v2`、Khronos、Medusa field13、Perseus、Gorgon、版本矩阵 |
| 第五部分 | 复盘与延伸 | 实验复盘、待研究问题、研究伦理 |
| 附录 | 速查 | 术语表、参数速查、来源说明 |

中文源在 `src/zh/`，英文镜像在 `src/en/`。

## 本地构建

依赖：[mdBook](https://rust-lang.github.io/mdBook/) 0.4.40+。

```powershell
winget install Rustlang.mdBook

# 构建中英双语 + 首页
.\serve.ps1

# 本地预览
.\serve.ps1 -Action serve-zh   # http://localhost:3000
.\serve.ps1 -Action serve-en   # http://localhost:3001
```

Git Bash / macOS / Linux：

```bash
./serve.sh build
./serve.sh serve-zh
./serve.sh serve-en
```

同样的检查也跑在 CI 中：`.github/workflows/build-check.yml` 会构建中英双语、检查相对链接，并校验两个 `SUMMARY.md` 的条目数一致。

## 贡献与补充

新增或修改页面时，必须同时更新**中英两棵树**和两个 `SUMMARY.md`。一致性清单、缺图标注意项与研究边界见 [CONTRIBUTING.md](CONTRIBUTING.md)。

直接使用 mdBook：

```bash
mdbook build                 # 中文 -> book/zh
mdbook serve -p 3000
```

英文版需要临时替换配置（mdBook 没有 `--config` 参数）：

```bash
cp book.toml book.toml.zh_bak && cp book-en.toml book.toml
mdbook build                 # 英文 -> book/en
cp book.toml.zh_bak book.toml && rm book.toml.zh_bak
```

## 进度

- [x] v0.1 —— 原文结构化抄录（中文）
- [x] v0.1 —— 英文镜像
- [x] 每种语言 4 张原创 SVG 示意图
- [x] mdBook 中英双语构建验证
- [x] 相对链接检查 + SUMMARY 条目一致性检查
- [ ] 补全原文缺失图（§2.3、§3.1、§4.3）
- [ ] 动态验证笔记
- [ ] 扩充术语表与版本矩阵

本仓库默认 **私有**。原文内容版权归原作者所有；在改变可见性或转载前，请先阅读 [NOTICE.md](NOTICE.md)。

原文缺失处用 **原文缺图** 提示框标出，**不臆造内容**。

## 来源与版权

原文：**《某音App风控参数分析》**
<https://mp.weixin.qq.com/s?__biz=MzkxNjczODUwMw==&mid=2247484942&idx=1&sn=3385ed001056c0ab6fb1384de51e30ec>

- 技术内容源自上述文章，本仓库仅为个人学习整理。
- 原文版权归原作者所有；第三方内容不授予任何许可证。
- 如作者希望删除或修改内容，请提 issue。
- 禁止将本资料用于未授权访问、批量注册、欺诈或违反平台条款与法律的活动。

详见 [NOTICE.md](NOTICE.md)。
