# Decisions through Shiji & Zizhi Tongjian

**Explore a difficult choice through historical decisions—with sources, costs and limits.**

[中文](README.md) · [Worked example in Chinese](examples/promotion-decision.zh-CN.md) · [Skill](skills/shiji-tongjian-decisions/SKILL.md)

An Agent Skill for career moves, collaboration, commitments and conflicts between personal values. It retrieves cases from *Shiji* and *Zizhi Tongjian*, reconstructs the options and information available at the time, then examines outcomes and hidden costs. Ancient stories suggest questions to test; they do not predict your future.

## Install

```bash
npx skills add zhuyep/shiji-tongjian-decisions --skill shiji-tongjian-decisions
```

For Codex, append `--agent codex`. The host must support Agent Skills; new online cases require its search or browser tools. The installer uses Node.js. The optional local quotation tool requires Python 3.10+ and no third-party Python packages.

Example prompt:

```text
Use $shiji-tongjian-decisions to examine this choice: …
My priorities are …, my available options are …, and my limits are …
Find structurally similar cases in the two books. Verify quotations,
compare hidden costs and counterexamples, and explain where the analogy fails.
Please answer in English while preserving original Chinese quotations.
```

Instructions and source texts are Chinese. English responses depend on the host model; cross-language behavior has not been independently evaluated.

## What makes it useful

- Separate information available at the decision point from later outcomes.
- Label source accounts, historian commentary, inference and counterfactuals.
- Track costs, who bears them, reversibility and conditions that invalidate an analogy.
- Treat the same event in both books as one event cluster, not independent confirmation.
- Check exact quotations against source snapshots with hashes, offsets and context.

The [worked example](examples/promotion-decision.zh-CN.md) compares accepting an unclear promotion, negotiating boundaries and preparing another option. It uses Fan Li, Zhang Liang and Wu Qi without assuming that a modern manager behaves like an ancient ruler. The modern scenario is fictional.

## Try quotation verification

From a local clone:

```bash
python3 skills/shiji-tongjian-decisions/scripts/corpus.py verify \
  --corpus skills/shiji-tongjian-decisions/references/sample-corpus \
  --library-id wikisource-zh-shiji-tongjian \
  --id shiji-041 --quote '君行令，臣行意。'

python3 -m unittest discover -s tests -v
```

`exact` confirms a literal match in that snapshot—not historical truth or causal validity. A punctuation-normalized match remains `normalized_only`. An empty cache search does not mean the books contain no relevant cases.

## Scope and evidence

The initial release includes excerpts from three volumes, three structured cases, thirteen quotations, twelve tool behavior tests and one example-evidence consistency test. One fictional scenario has a maker walkthrough. Independent evaluations, real decision outcomes and full-book retrieval coverage remain unverified.

The local Python tool makes no network requests. Your AI host handles prompts and online searches according to its own settings. Redact sensitive situations before sharing. This is a reasoning aid, not a substitute for current professional evidence.

## Feedback and licensing

[Report a failure or useful result](https://github.com/zhuyep/shiji-tongjian-decisions/issues) with a redacted prompt, source location and what was missing. Specific evidence is more useful than a generic rating. A Star is welcome if the skill helped you notice an overlooked option or cost.

Original code and instructions: [MIT](LICENSE). Wikisource excerpts retain their separate attribution and license in [NOTICE](NOTICE.md) and the [text license notice](skills/shiji-tongjian-decisions/references/sample-corpus/LICENSE.md). [Design influences](skills/shiji-tongjian-decisions/references/design-provenance.md) are credited; their repository snapshots are not redistributed.
