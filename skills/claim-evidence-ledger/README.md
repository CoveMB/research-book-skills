# claim-evidence-ledger

## What it does

Use this skill to turn a chapter, outline, thesis, or draft into a ledger of claims. It extracts the claims that carry the argument, classifies each one, checks evidence status, flags overclaiming, and suggests safer wording.

This is one of the best safeguards against research prose that sounds confident but outruns the evidence. It helps the author see which sentences are interpretive, which need citations, which need stronger evidence, and which should be narrowed.

## When to use it in the book writing process

Use it before polishing prose and before citation integrity review. It works well after a chapter draft exists, after an argument architecture has been built, or before sending a chapter to readers.

Use it when a draft has too many broad claims, causal claims, predictions, historical claims, or field-specific statements that may need support.

## Good inputs

- A chapter draft, section draft, outline, or thesis tree.
- Available sources or notes, if any.
- The intended audience and level of evidentiary rigor.
- Questions about which claims are too strong or unsupported.

## Example requests

```text
Extract the major claims from this chapter and build a claim-evidence ledger.
```

```text
Tell me which claims need citations, which are interpretive, and which are overstated.
```

```text
Rewrite the risky claims in safer language without weakening the argument too much.
```

## Typical output

Expect a table with claim, claim type, evidence status, current support, evidence needed, risk, and safer wording. The output also lists high-risk claims, claims that can remain interpretive or normative, source priorities, and the next best skill.

## Best next steps

After this skill, use `citation-integrity-auditor` to verify citation placement, source-claim fit, quotes, page numbers, and bibliography issues. Use `scholarly-prose-editor` once the claim support is stable.
