# Part 4: Requests and Signatures

> This part is the algorithmic core of the book, and the place most prone to "every header is right on its own, but the combination is wrong".

## What this part covers

- [Chapter 4: Core Request Parameters Dissected](./chapter_params/README.md)
  - 4.1 x-common-params-v2
  - 4.2 X-Khronos and suite alignment
  - 4.3 X-Medusa: two generations and field13
  - 4.4 f17 clock slot, session structure, and the eight-branch question
  - 4.5 X-Perseus: the FL feature chain
  - 4.6 X-Perseus: KD, checksum, and protobuf
  - 4.7 X-Gorgon
  - 4.8 Version differences and implementation constraints

## Suggested reading order

| Goal | Order |
|---|---|
| Big picture first | 4.1 → 4.2 → 4.3 → 4.8 |
| Dig into Medusa | 4.3 → 4.4 → 4.8 |
| Dig into Perseus | 4.5 → 4.6 → 4.8 |
| Reproduce request binding | 4.1 → 4.7 → 4.8 |

## After reading, you should be able to

- explain each part of `msg52 = query_sm3(32B) || body_md5(16B) || khronos_le(4B)`;
- compare the old "content selects the branch" scheme with the new "khronos selects the branch" scheme;
- state why Perseus's FL chain can be reproduced offline;
- explain why KD must be "shared process-wide and persisted across sessions";
- describe how Gorgon binds the request body to the signature.

> ⚠️ **The most important conclusion**: the two generations of the Medusa algorithm cannot be mixed. Version number, branch selection, constant derivation, and output assembly must all come from the same configuration.
