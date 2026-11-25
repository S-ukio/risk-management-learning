# Preface

> 🎯 *"This roughly analyzes the different versions between 39.4 and 41.2; starting from 41.1, the algorithm changed somewhat."*

## Why this note exists

This is a **study note**, not a new paper.

The original article, "Douyin App Risk Control Parameter Analysis", compressed a large amount of information into a single long piece: the three-layer risk control system, device fingerprints, the registration chain, the seven signature headers, Medusa's field13, Perseus's FL chain, Gorgon's request binding... The information density is high, but a long article is not convenient for repeated reference or for adding notes by topic.

So, following the build approach of [agent_learning](https://github.com/Haozhe-Xing/agent_learning), this project splits the original into:

- **Parts**: risk control system → identity fingerprint → registration flow → core parameters → review and extensions;
- **Chapters**: one topic per chapter, with each chapter further split into sections;
- **Bilingual**: Chinese source plus an English mirror, with consistent terminology;
- **Extensible**: source gaps, unclear semantics, and points that need measurement all get explicit markers and question lists.

## Editorial principles

1. **Faithful transcription**: technical facts, parameter names, tables, and example vectors follow the original as closely as possible; conclusions are not rewritten.
2. **No invention**: where the original has "nothing after a colon", the spot is marked <span class="badge gap">source gap</span> and is not filled in by guessing.
3. **Distinguish sources**: original conclusions, note derivations, and questions to be verified are labeled separately.
4. **Principles only, no operational guidance**: no steps for bulk registration, account nurture, or bypassing risk control; dynamic experiments are performed only in authorized environments.

## What the source covers

| Dimension | Scope |
|---|---|
| App version | 39.4 – 41.2 |
| Key versions | 41.1 / 41.2 (algorithm change boundary) |
| Core components | MSSDK, Medusa, Perseus, Gorgon, SDI, TicketGuard, Badger |
| Network stack | ttNet / Cronet, TLS fingerprint, HTTP/2 |

The original says relatively little about 39.4 – 41.0 and focuses on **the changes from 41.1 onward**; this note keeps that bias and separates version differences into their own section.

## How to read

- First read: start with the [Reading Guide](./reading-guide.md) and pick a route.
- For a quick global picture: Chapter 1 → Chapter 2 → Chapter 5.
- To understand the algorithms: go straight to Chapter 4 and read 4.2 → 4.3 → 4.4 → 4.5 → 4.6 in order.
- To add content: check the [open questions list](./chapter_reflection/02_open_questions.md) first, which lists where the source has gaps and unclear semantics.

## Sources and disclaimer

- Original: **"Douyin App Risk Control Parameter Analysis"**, a WeChat official account article, retrieved 2026-11-25.
- Original link and citation details are in [Appendix C](./appendix/sources.md).
- Copyright in the technical content belongs to the original author; this repository is a personal study compilation, private by default, and does not grant permission to republish.
- This material is for **authorized security research and study** only. Do not use it for unauthorized access, bulk registration, platform abuse, or any illegal activity.

> 📌 **Current status**: v0.1 — structured transcription of the source and the English mirror are complete; source gaps and items to be verified are not yet filled.
