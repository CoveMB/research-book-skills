# Research Book Skills

Version: 1.0.0

Research Book Skills is a local Agent Skills plugin for people writing scholarly nonfiction, research monographs, long-form essays, or book proposals. It turns loose research work into concrete artifacts: a research agenda, source discovery log, literature map, thesis tree, chapter brief, claim ledger, citation audit, continuity review, and proposal.

The plugin assumes a person is still doing the research. It can sort, pressure-test, and clean up the work, but it will not pretend that model memory verifies a source. It asks what kind of claim you are making, what evidence can support it, where the argument is too strong, and what an expert reader would challenge.

## Install in 30 seconds

You need Python 3 and an app that can load local Agent Skills plugins.

From the unzipped folder:

```bash
./install.sh
```

On Windows PowerShell:

```powershell
.\install.ps1
```

The installer validates the plugin, copies it to your local plugin directory, and updates your personal marketplace file. Restart the app after installation, then enable **Research Book Skills** from the plugin directory.

Preview the install first:

```bash
./install.sh --dry-run
```

Full manual install paths are in [`docs/INSTALLATION.md`](docs/INSTALLATION.md). The manual guide covers personal marketplace install, repo marketplace install, direct skill-folder install, upload notes for single-skill environments, validation, and uninstall steps.

## Try it first

Use `research-intent-router` when the next skill is unclear:

```text
Use research-intent-router. I want to write a research book about urban climate adaptation. Route this request and tell me the smallest useful next step.
```

For a full project plan:

```text
Use research-book-orchestrator. I am writing a research nonfiction book about urban climate adaptation. Build a staged research and writing workflow with quality gates.
```

For an existing draft:

```text
Use claim-evidence-ledger. Audit this chapter for unsupported claims, overclaiming, and citation needs.
```

For citation problems:

```text
Use citation-integrity-auditor. Check whether the citations in this draft support the claims they are attached to.
```

## What it helps with

Reach for this plugin when you need help with research structure, source discipline, argument design, or manuscript repair. It is useful before drafting, while drafting, and after a draft exists.

Typical jobs:

- turn a broad book idea into research questions, scope boundaries, and contribution claims
- design a repeatable source search instead of collecting sources randomly
- map a literature into schools, debates, gaps, and usable chapter logic
- build a thesis tree with warrants, assumptions, evidence, and counterarguments
- audit claims for evidence strength, citation needs, and overstatement
- check citation/source fit without inventing page numbers or fake references
- keep chapters consistent across concepts, tone, thesis, and structure
- shape a research book proposal around the actual argument and source base

## Recommended paths

| Situation | Start here | Then use |
|---|---|---|
| You have a topic but no plan | `research-intent-router` | `scholarly-research-agenda`, then `systematic-source-discovery` |
| You want a full book workflow | `research-book-orchestrator` | Follow the staged plan it returns |
| You need sources | `systematic-source-discovery` | `annotated-bibliography-builder`, then `literature-review-mapper` |
| You have sources but no argument | `literature-review-mapper` | `argument-architecture` |
| You have a chapter outline | `chapter-architecture` | `claim-evidence-ledger`, then `scholarly-prose-editor` |
| You have a draft | `claim-evidence-ledger` | `counterargument-peer-review`, then `citation-integrity-auditor` |
| You have several chapters | `manuscript-continuity-editor` | `chapter-architecture` for chapters that need rebuilding |
| You need a proposal | `book-proposal-scholarship` | `citation-integrity-auditor` for factual and source claims |

## Workflows included

| Workflow | Best for | Main output |
|---|---|---|
| [`research-intent-router`](skills/research-intent-router/README.md) | Choosing the smallest useful skill for a research request | Route, mode, source access status, next step |
| [`research-book-orchestrator`](skills/research-book-orchestrator/README.md) | Planning or restarting a whole book project | Staged workflow plan |
| [`scholarly-research-agenda`](skills/scholarly-research-agenda/README.md) | Turning a broad idea into a research agenda | Research questions, scope, contribution, evidence plan |
| [`systematic-source-discovery`](skills/systematic-source-discovery/README.md) | Planning a source search | Query bank, inclusion rules, search log |
| [`literature-review-mapper`](skills/literature-review-mapper/README.md) | Making sense of a body of sources | Literature map, debates, gaps, thesis implications |
| [`annotated-bibliography-builder`](skills/annotated-bibliography-builder/README.md) | Taking structured notes on sources | Annotated bibliography entries |
| [`methodology-source-auditor`](skills/methodology-source-auditor/README.md) | Checking whether a source is strong enough for a claim | Source credibility and method audit |
| [`claim-evidence-ledger`](skills/claim-evidence-ledger/README.md) | Extracting claims from a draft and testing support | Claim/evidence ledger |
| [`argument-architecture`](skills/argument-architecture/README.md) | Building the book-level argument | Thesis tree and argument dependencies |
| [`counterargument-peer-review`](skills/counterargument-peer-review/README.md) | Stress-testing a thesis or chapter | Objections, rival explanations, revision priorities |
| [`chapter-architecture`](skills/chapter-architecture/README.md) | Designing or repairing a chapter | Chapter brief |
| [`scholarly-prose-editor`](skills/scholarly-prose-editor/README.md) | Editing research prose without adding facts | Revised passage and style notes |
| [`citation-integrity-auditor`](skills/citation-integrity-auditor/README.md) | Checking citations, quotes, page needs, and source fit | Citation integrity audit |
| [`manuscript-continuity-editor`](skills/manuscript-continuity-editor/README.md) | Reviewing multiple chapters together | Continuity review |
| [`case-study-integration`](skills/case-study-integration/README.md) | Using cases without cherry-picking or weak analogy | Case study integration plan |
| [`book-proposal-scholarship`](skills/book-proposal-scholarship/README.md) | Writing a serious nonfiction or scholarly book proposal | Proposal draft and submission risks |

Every skill folder also has its own `README.md` with example requests, useful inputs, expected outputs, and common failure modes.

## Mode and automation summary

This package does not install scheduled background jobs. Its "automation" is routing: the router and orchestrator decide which workflow should run, how deep the source lookup should go, and what artifact should come next.

| Mode | Primary skill | Use it for | Output |
|---|---|---|---|
| `research-route` | `research-intent-router` | Default routing when the next skill is unclear | Research route |
| `research-route-normal` | `research-intent-router` | Plan-first routing with lookup only when justified | Research route and verification limits |
| `research-route-deep` | `research-intent-router` | Routing plus source lookup attempt where tools and access allow it | Deep route with source access labels |
| `orchestrate` | `research-book-orchestrator` | Full project planning | Staged workflow plan |
| `agenda` | `scholarly-research-agenda` | Research questions, scope, and contribution | Book research agenda |
| `source-discovery` | `systematic-source-discovery` | Search strategy and source collection plan | Source discovery log |
| `literature-map` | `literature-review-mapper` | Schools, debates, methods, gaps | Literature map |
| `argument-architecture` | `argument-architecture` | Book-level thesis and claim structure | Thesis tree |
| `counterargument-review` | `counterargument-peer-review` | Strong objections and rival explanations | Peer-review style critique |
| `chapter-architecture` | `chapter-architecture` | Chapter logic and section order | Chapter brief |
| `claim-ledger` | `claim-evidence-ledger` | Claim extraction and support checks | Claim/evidence ledger |
| `citation-audit` | `citation-integrity-auditor` | Citation accuracy and source/claim fit | Citation integrity audit |
| `continuity-audit` | `manuscript-continuity-editor` | Whole-manuscript coherence | Continuity review |
| `proposal` | `book-proposal-scholarship` | Press or agent-facing proposal work | Research book proposal |
| `annotated-bibliography` | `annotated-bibliography-builder` | Source notes | Annotated bibliography |
| `source-audit` | `methodology-source-auditor` | Source quality review | Source methodology audit |
| `case-study` | `case-study-integration` | Case selection and comparison | Case study integration plan |
| `prose-edit` | `scholarly-prose-editor` | Style, clarity, and structure edits | Revised passage |

See `MODE_REGISTRY.md` for the full registry and [`docs/ROUTING_MATRIX.md`](docs/ROUTING_MATRIX.md) for routing rules.

## Source lookup modes

Normal mode is the default. It classifies the task and chooses the smallest useful skill before doing any deep lookup. It escalates only when source finding, source existence, quote/page verification, current facts, or high-risk claims make lookup necessary.

Deep mode always attempts lookup after routing, but it still has limits. If lookup tools, source access, or full text are unavailable, the result stays marked as unverified.

Use these prompts:

```text
Use research-intent-router in normal mode. Route this research request first.
```

```text
Use research-intent-router in deep mode. Route this request and attempt source lookup where available.
```

## Artifacts and examples

The plugin includes a shared book artifact schema at [`shared/contracts/book/book_artifact.schema.json`](shared/contracts/book/book_artifact.schema.json). Example artifacts live in [`examples/book_artifacts/`](examples/book_artifacts/):

- `book-research-agenda.json`
- `source-discovery-log.json`
- `literature-map.json`
- `thesis-tree.json`
- `chapter-brief.json`
- `claim-evidence-ledger.json`
- `continuity-review.json`
- `book-proposal.json`

These artifacts are useful when a project needs to survive across sessions, tools, or chapter drafts.

## Limits

Research Book Skills is strict about source truth:

- no fabricated citations, page numbers, quotes, DOI metadata, or bibliographic claims
- no model memory treated as source verification
- no claims about field consensus without a representative source set or lookup result
- no overwriting manuscript files, source files, bibliography databases, or plugin files unless you ask for that directly

It also does not replace a researcher, editor, advisor, peer reviewer, or fact checker.

## Package layout

```text
scholarly-research-book-plugin/
  .codex-plugin/plugin.json
  skills/
    research-intent-router/
    research-book-orchestrator/
    scholarly-research-agenda/
    ...
  docs/
  examples/
  shared/
  scripts/
```

The package works as a local plugin and as a portable collection of `SKILL.md` folders.

## Validate

Run the full local check:

```bash
./validate.sh
```

Or run the checks one by one:

```bash
python3 scripts/validate_plugin.py .
python3 scripts/check_book_artifact_contract.py --path .
python3 -m unittest discover -s scripts -p 'test_*.py'
```

## Useful docs

- [`docs/INSTALLATION.md`](docs/INSTALLATION.md): manual install options and uninstall steps
- [`docs/SKILL_INDEX.md`](docs/SKILL_INDEX.md): all skills and when to use them
- [`docs/WORKFLOW_PLAYBOOK.md`](docs/WORKFLOW_PLAYBOOK.md): practical book workflows
- [`docs/QUALITY_STANDARD.md`](docs/QUALITY_STANDARD.md): source, claim, and citation standards
- [`docs/SOURCE_LIMITS.md`](docs/SOURCE_LIMITS.md): what counts as verified source access
- [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md): common setup and routing issues

## License

MIT. See [`LICENSE`](LICENSE).
