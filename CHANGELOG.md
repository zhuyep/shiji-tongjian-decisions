# Changelog

## Unreleased

- Docs: README zh/en first screen now shows a no-clone hero contrast (`docs/hero-verify-flip.png`) of the measured `exact` / `not_found` flip (「意」→「义」), so the verify hook is visible at a glance.
- Docs: Cursor 2.5+ install path is now on the README first screen and in the Install section (`/add-plugin shiji-tongjian-decisions@https://github.com/zhuyep/shiji-tongjian-decisions`); the repo already shipped `.cursor-plugin/plugin.json`, but the path was undocumented. Not listed on the official Cursor Marketplace.
- Docs: README 30s verify now shows the measured `exact` / `not_found` JSON (change one character and it fails) so the hook is visible without cloning; no-clone reproduction lives in `examples/verify-flip.zh-CN.md`.
- Docs: discovery demo `examples/verify-second-source.zh-CN.md` — a second registered source (`shiji-055` / 「留侯行少傅事。」) also returns `exact` in the README 30s verify section (deep-linked from README zh/en, examples index, and the other verify demos).
- Docs: discovery demo `examples/verify-wrong-id.zh-CN.md` — a genuine quotation bound to the wrong registered `--id` is not `exact` (`not_found`, exit 1; deep-linked from README zh/en, examples index, verify-flip, and verify-normalized).
- Docs: discovery demo `examples/verify-normalized.zh-CN.md` — `normalized_only` is not `exact` (punctuation / de-punctuated hit; deep-linked from README zh/en, examples index, and verify-flip).
- Docs: discovery worked example `examples/partner-commitment-decision.zh-CN.md` — partnership / long-term commitment paths (accept / written exit boundaries / decline with optionality); deep-linked from README zh/en and examples index.
- Docs: discovery demo `examples/verify-flip.zh-CN.md` — exact vs one-character flip on `shiji-041` (deep-linked from README zh/en).
- Docs: optional paid single-session coaching one-pager (`docs/paid-trial-onepager.md`) — MIT skill stays free; price/deliverable/payment-recon steps for the ¥299 trial.
- Docs: README zh/en contrast table vs generic history quips (discovery).

- Add six synthetic manual regression scenarios with explicit tool conditions, acceptance criteria and a result-recording guide. Offline fixture checks do not demonstrate model behavior.
- Bind the public worked example's displayed quotations to evidence IDs and validate its actual Markdown text and source links against the registry. Add adversarial mutation checks.
- Keep the skill instructions unchanged pending actual behavior evaluations.

## v0.1.0 — 2026-09-21

- Publish the Chinese decision-comparison skill for *Shiji* and *Zizhi Tongjian*.
- Include a Python standard-library tool for attributed snapshots, keyword retrieval and exact quotation checks.
- Add three excerpt sources, three structured historical cases and a fictional modern worked example with thirteen quotations.
- Provide Chinese and English setup guides, portable tests and explicit third-party text attribution.

Independent user evaluation, full-book retrieval coverage and real decision outcomes are not established by this release.
