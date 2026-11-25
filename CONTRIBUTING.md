# Contributing / 补充指南

This repository is a personal study book. Contributions are mainly **notes to future self**, so the rules are simple: keep both languages in sync, mark uncertainty, and never invent a missing detail.

## Adding a page / 新增一页

1. Create the page in **both** trees:
   - `src/zh/<chapter>/<nn_slug>.md`
   - `src/en/<chapter>/<nn_slug>.md`
2. Add the entry to **both** `SUMMARY.md` files, at the same position.
3. If the page uses a new image, put the localized SVG in **both**:
   - `src/zh/svg/<name>.svg`
   - `src/en/svg/<name>.svg`
4. Run the checks:

```bash
python -I scripts/check_links.py zh
python -I scripts/check_links.py en
mdbook build
./serve.sh build        # or: .\serve.ps1
```

## Writing rules / 写作规则

- **Facts need a source.** Quote the original article or a verified experiment. Do not turn a guess into a statement.
- **Mark gaps.** If the source is missing content, use:

  ```html
  <span class="badge gap">原文缺图 / source gap</span>
  ```

  and say explicitly that the note does not fill the gap by guessing.
- **Mark derivations.** If you compute something from the source's numbers, label it:

  ```html
  <div class="callout"><span class="callout-title">🧮 笔记推导（待验证）</span>
  ...
  </div>
  ```

- **Preserve identifiers exactly.** Parameter names, header names, hex values, and example vectors are data, not prose.
- **Use the glossary.** `src/zh/appendix/glossary.md` and `src/en/appendix/glossary.md` define the shared terminology.

## Parity checklist / 中英一致性

- [ ] Same section order and heading numbering
- [ ] Same tables, code blocks, and example vectors
- [ ] Same callouts and badges (translated text, identical classes)
- [ ] Same relative links and image filenames
- [ ] `SUMMARY.md` entry counts match (`build-check` enforces this)

## Source gaps / 待补清单

Before adding new material, check
[`5.2 Open Questions`](src/en/chapter_reflection/02_open_questions.md)
([中文](src/zh/chapter_reflection/02_open_questions.md)).
Resolve a question there and then update the corresponding section — avoid creating a second, disconnected note.

## Scope / 边界

This is a study resource for **authorized security research**. Do not add:

- step-by-step mass registration or account-nurturing instructions;
- ways to bypass platform controls for abuse;
- personal data, live credentials, or unredacted identifiers from real users.

See [NOTICE.md](NOTICE.md) for the full disclaimer.
