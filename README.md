# Research book skills plugin

Version: 1.0.0

A local Agent Skills plugin for serious research nonfiction and research book writing. It bundles 16 focused `SKILL.md` workflows: research intent routing, research agenda design, systematic source discovery, literature review mapping, source auditing, argument architecture, chapter structure, prose editing, citation integrity, manuscript continuity, case-study integration, and book proposal development.

The package now follows a staged book workflow with architecture docs, a mode registry, an artifact contract, examples, and validation scripts.

## What this is

This plugin has this structure:

```text
scholarly-research-book-plugin/
  .codex-plugin/plugin.json
  skills/
    research-book-orchestrator/SKILL.md
    scholarly-research-agenda/SKILL.md
    ...
  docs/
  examples/
  scripts/
```

It works as a local plugin and as a portable collection of `SKILL.md` folders.

## Fast install for Codex local plugin use

From the unzipped folder:

```bash
python3 scripts/install_codex_plugin.py
```

On Windows PowerShell:

```powershell
py scripts\install_codex_plugin.py
```

The installer validates the plugin, copies it to your local plugin directory, and creates or updates a personal marketplace file so Codex can discover it.

## Manual install options

See `docs/INSTALLATION.md` for:

- Codex personal marketplace install
- Codex repo marketplace install
- Direct local skill folder install
- ChatGPT upload notes
- Validation commands

## Skills included

See `docs/SKILL_INDEX.md` for the skill list and use cases.

## Quick skill summary

Each skill folder now includes a `README.md` with plain-language guidance, book-process timing, useful inputs, example requests, expected outputs, and suggested next steps.

| Skill | Use it when |
|---|---|
| [`research-intent-router`](skills/research-intent-router/README.md) | A research prompt needs automatic intent detection, smallest-useful-skill routing, and a decision on whether deep source lookup is justified. |
| [`research-book-orchestrator`](skills/research-book-orchestrator/README.md) | The project needs a staged plan, a next-step diagnosis, or routing across several research and writing tasks. |
| [`scholarly-research-agenda`](skills/scholarly-research-agenda/README.md) | A broad idea needs research questions, scope boundaries, contribution claims, terms, and an evidence plan. |
| [`systematic-source-discovery`](skills/systematic-source-discovery/README.md) | The book needs a repeatable source search, query bank, inclusion rules, citation-chaining plan, or search log. |
| [`literature-review-mapper`](skills/literature-review-mapper/README.md) | Sources need to be grouped into schools, debates, methods, consensus, gaps, and thesis implications. |
| [`annotated-bibliography-builder`](skills/annotated-bibliography-builder/README.md) | Individual sources need structured notes on argument, method, evidence, relevance, limits, and chapter placement. |
| [`methodology-source-auditor`](skills/methodology-source-auditor/README.md) | The author needs to know whether sources are credible enough for the claims they are asked to support. |
| [`claim-evidence-ledger`](skills/claim-evidence-ledger/README.md) | A draft, outline, or thesis needs claim extraction, evidence status, citation needs, risk labels, and safer wording. |
| [`argument-architecture`](skills/argument-architecture/README.md) | The book needs a thesis tree, warrants, assumptions, counterarguments, dependencies, and chapter-level argument sequence. |
| [`counterargument-peer-review`](skills/counterargument-peer-review/README.md) | A thesis, chapter, outline, or proposal needs strong objections, rival explanations, missing literatures, and revision strategy. |
| [`chapter-architecture`](skills/chapter-architecture/README.md) | A chapter needs a central question, claim, section sequence, evidence placement, transitions, and revision risks. |
| [`scholarly-prose-editor`](skills/scholarly-prose-editor/README.md) | Research prose needs clearer style, rhythm, structure, precision, or compression without adding unsupported facts. |
| [`citation-integrity-auditor`](skills/citation-integrity-auditor/README.md) | A draft needs checks for unsupported claims, citation-source mismatch, quote integrity, page needs, and bibliography issues. |
| [`manuscript-continuity-editor`](skills/manuscript-continuity-editor/README.md) | Multiple chapters need review for thesis coherence, repetition, contradictions, concept tracking, tone, and chapter order. |
| [`case-study-integration`](skills/case-study-integration/README.md) | Cases or examples need careful selection, comparison, counter-cases, source limits, and safer claim wording. |
| [`book-proposal-scholarship`](skills/book-proposal-scholarship/README.md) | The project needs a proposal with thesis, contribution, audience, source base, chapter summaries, and submission risks. |

## Architecture and modes

- `docs/ARCHITECTURE.md` describes the stage flow, skill graph, quality gates, artifact levels, and package structure.
- `MODE_REGISTRY.md` lists modes and outputs.
- `shared/contracts/book/book_artifact.schema.json` defines the JSON artifact contract used by examples under `examples/book_artifacts/`.

Router modes: `research-route-normal` and `research-route-deep`. See `MODE_REGISTRY.md` for mode behavior.

## Recommended first workflow

Use `research-intent-router` when the next skill is unclear. For a new research book with no route ambiguity, use:

1. `scholarly-research-agenda`
2. `systematic-source-discovery`
3. `literature-review-mapper`
4. `argument-architecture`
5. `chapter-architecture`
6. `claim-evidence-ledger`
7. `counterargument-peer-review`
8. `citation-integrity-auditor`
9. `manuscript-continuity-editor`

## Suggested next steps

Skill responses may end with an optional `## Suggested next step` only when one follow-on skill reduces a named scholarly risk. This is not a default footer. See `docs/AUTO_SELECTION_GUARDRAILS.md` and `docs/ROUTING_MATRIX.md` for the full gate.

## Quality standard

This plugin is meant to make the agent more rigorous. It repeatedly asks:

- What kind of claim is this?
- What source type can support it?
- What would an expert object to?
- Is the claim stronger than the evidence?
- Are citations real, relevant, and accurately used?

## Validation

```bash
python3 scripts/validate_plugin.py .
python3 scripts/check_book_artifact_contract.py --path .
python3 scripts/test_check_book_artifact_contract.py
```

## License

MIT. See `LICENSE`.
