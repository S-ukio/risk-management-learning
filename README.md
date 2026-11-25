# Risk Management Learning

> A bilingual, chapter-by-chapter study of Douyin App risk-control parameters — from device fingerprints to request signatures.

This repository reorganizes the public WeChat article **《某音App风控参数分析》** into a navigable mdBook, following the structure and engineering-first style of [Haozhe-Xing/agent_learning](https://github.com/Haozhe-Xing/agent_learning).

## What this is — and what it is not

- **It is** a structured study copy: terminology normalized, chapters split by topic, version differences compared, and every gap in the source marked explicitly.
- **It is not** a mass-registration / account-nurturing tutorial, nor an operational manual for bypassing platform controls.
- All experiments must be performed only on devices, accounts, and environments for which you have explicit authorization.

## Book structure

| Part | Chapter | Focus |
|---|---|---|
| 1 | Risk-control framework | Three-layer model, seven signature headers, SDK components, version evolution |
| 2 | Device identity & fingerprints | Four device IDs, static/dynamic fingerprints, encrypted carriers, decision states |
| 3 | Device registration flow | Clock baseline, registration chain, payload, tokens, nurture chain, TrustChain |
| 4 | Request parameters | `x-common-params-v2`, Khronos, Medusa field13, Perseus, Gorgon, version matrix |
| 5 | Review & open questions | Experimental results, unresolved questions, research ethics |
| App. | Reference | Glossary, quick reference, sources |

The Chinese source is in `src/zh/`; the English mirror is in `src/en/`.

## Build locally

Requirements: [mdBook](https://rust-lang.github.io/mdBook/) 0.4.40+.

```powershell
winget install Rustlang.mdBook

# Build both languages and the landing page
.\serve.ps1

# Live preview
.\serve.ps1 -Action serve-zh   # http://localhost:3000
.\serve.ps1 -Action serve-en   # http://localhost:3001
```

On Git Bash / macOS / Linux:

```bash
./serve.sh build
./serve.sh serve-zh
./serve.sh serve-en
```

The same commands are available in CI via `.github/workflows/build-check.yml`, which builds both languages, checks relative links, and enforces SUMMARY parity.

## Publish with GitHub Pages

1. Push `main` to GitHub.
2. In **Settings → Pages**, set **Source** to **GitHub Actions**.
3. Open **Actions → Deploy mdBook to GitHub Pages** and run it once if needed.

The workflow builds the Chinese book at `/zh/`, the English book at `/en/`, and the language selector at the repository root.

## Contributing

When adding or revising a page, update **both** language trees and both `SUMMARY.md` files. See [CONTRIBUTING.md](CONTRIBUTING.md) for the parity checklist, source-gap conventions, and scope boundaries.

Direct mdBook commands:

```bash
mdbook build                 # Chinese -> book/zh
mdbook serve -p 3000
```

For English, temporarily swap the config (mdBook has no `--config` flag):

```bash
cp book.toml book.toml.zh_bak && cp book-en.toml book.toml
mdbook build                 # English -> book/en
cp book.toml.zh_bak book.toml && rm book.toml.zh_bak
```

## Status

- [x] v0.1 — faithful restructure of the source article (Chinese)
- [x] v0.1 — English mirror
- [x] 4 original SVG diagrams per language
- [x] mdBook build verified (zh + en)
- [x] Relative link check + SUMMARY parity check
- [ ] Fill source gaps (missing figures in §2.3, §3.1, §4.3)
- [ ] Dynamic verification notes
- [ ] Expand glossary and version matrix

This repository is **private by default**. The source content belongs to its original author; see [NOTICE.md](NOTICE.md) before changing visibility or redistributing.

Gaps in the original article are marked with **原文缺图 / source gap** callouts. They are intentionally *not* filled with guesses.

## Source & copyright

Original article: **《某音App风控参数分析》**
<https://mp.weixin.qq.com/s?__biz=MzkxNjczODUwMw==&mid=2247484942&idx=1&sn=3385ed001056c0ab6fb1384de51e30ec>

- Technical content derives from the original article. This repository is a personal study reorganization.
- The original author retains all rights to the source content. No license is granted for third-party material.
- If you are the author and want content removed or amended, please open an issue.
- Do not use this material for unauthorized access, mass registration, fraud, or any activity that violates platform terms or applicable law.

See [NOTICE.md](NOTICE.md) for details.
