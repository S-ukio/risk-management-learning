# 5.3 Compliance, Ethics and Research Boundaries

> 🎯 *"Being able to understand is not the same as being allowed to abuse."*

## Why this section must exist

This note analyzes the risk-control parameters of a real platform. It is inherently dual-use:

- **Defensive perspective**: understanding how the platform identifies anomalous devices and how it designs signatures and state machines;
- **Abusive perspective**: bypassing risk control, bulk registration, traffic inflation, fraud.

This note serves only the former. The following boundaries are not "disclaimer boilerplate"; they are preconditions for the research to remain sustainable, lawful, and responsible.

## Four bottom lines

### 1. Experiment only in authorized environments

- devices, accounts, apps, and networks that you own or have explicit written authorization for;
- in-house corporate compliance testing, vulnerability bounty programs, CTFs, teaching labs;
- do not target real users' accounts, devices, or data.

### 2. No bulk abuse

- no bulk account registration;
- no account nurturing, traffic inflation, fake comments, or fake orders;
- no circumvention of platform billing, risk control, or content moderation;
- do not treat "85% success rate" as a reproducible target.

### 3. Do not touch personal data

- do not collect, store, or distribute other people's personal information;
- do not scrape contacts, location, device identifiers, or other sensitive data;
- tokens, device_id, and session_uuid in analysis samples should be treated as sensitive data and redacted before citation.

### 4. Responsible disclosure

- for exploitable security issues found, report first through the platform / vendor disclosure process;
- do not publish directly exploitable full chains on public channels;
- give vendors a reasonable remediation window.

## Legal and terms risk

| Risk | Description |
|---|---|
| Platform terms of service | bypassing risk control and bulk registration usually violate the ToS and may lead to account bans and civil claims |
| Computer crime laws | unauthorized access to or interference with computer information systems may constitute a criminal offense |
| Personal information protection | collecting and processing personal information requires a lawful basis |
| Copyright | use of the source and technical materials must respect the original author's rights |

> ⚠️ Laws differ by country and region. This section does not constitute legal advice; consult legal counsel for specific projects.

## Pre-experiment checklist

Before starting any dynamic experiment, confirm each item:

- [ ] I have explicit authorization for the device / account / network;
- [ ] the experiment will not affect real users;
- [ ] I will not bulk register or nurture accounts;
- [ ] I will not collect or distribute personal information;
- [ ] identifiers in samples will be redacted;
- [ ] I know how to contact the vendor / platform for disclosure;
- [ ] I understand the relevant platform terms and legal risks.

## Citation boundaries for the source

- copyright in the source's technical content belongs to the original author;
- this note is a study compilation, private by default;
- do not use the source content for commercial training, paid communities, or selling "tutorials";
- when citing, attribute the source and retain the original's "for exchange and study only" statement.

<div class="callout note"><span class="callout-title">🔑 The final principle</span>
If a piece of research only holds under the premise of "not being discovered", it has probably already crossed legal and ethical boundaries. Genuine research should withstand public discussion and peer review.
</div>
