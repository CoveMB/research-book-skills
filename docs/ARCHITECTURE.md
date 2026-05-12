# Research book plugin architecture

This package is organized as a book-length research workflow, not a loose set of writing prompts. Each stage has a skill, an expected artifact, and a quality gate before the next stage.

## How to read this file

- Use the flow diagram for the high-level sequence.
- Use the stage matrix to see which skill produces which artifact.
- Check the quality gates before moving from planning to drafting or from drafting to audit.
- Use `MODE_REGISTRY.md` as the short routing reference.
- Use `shared/contracts/book/book_artifact.schema.json` when JSON artifacts are requested or examples are changed.
- Use `docs/SKILL_README_TEMPLATE.md` when adding or refreshing skill README files.

## Pipeline flow

```mermaid
flowchart TD
    Start([Book idea or manuscript material])
    Router[0. Research intent router]
    Specialists[Specialists: choose the smallest useful skill]
    Orchestrator[research-book-orchestrator]
    Agenda[1. Research agenda]
    Discovery[2. Source discovery]
    Dedupe[2.1 Discovery dedupe]
    Notes[2.2 Source notes and extraction]
    Literature[3. Literature map]
    Argument[4. Argument architecture]
    Review[5. Counterargument review]
    Chapter[6. Chapter architecture]
    Draft[7. Prose revision]
    Evidence[8. Claim-evidence ledger]
    Trace[8.1 Claim traceability]
    Citation[9. Citation integrity audit]
    Continuity[10. Manuscript continuity]
    Proposal[11. Book proposal]
    Comps[11.1 Comps verification]
    Release[12. Release audit]
    End([Book-ready artifacts])

    Start --> Router
    Router --> Specialists
    Specialists --> Orchestrator
    Specialists --> Agenda
    Orchestrator --> Agenda
    Agenda --> Discovery
    Discovery --> Dedupe
    Dedupe --> Notes
    Notes --> Literature
    Literature --> Argument
    Argument --> Review
    Review --> Chapter
    Chapter --> Draft
    Draft --> Evidence
    Evidence --> Trace
    Trace --> Citation
    Citation --> Continuity
    Continuity --> Proposal
    Proposal --> Comps
    Comps --> Release
    Release --> End

    classDef gate fill:#fff4e6,stroke:#d48806,stroke-width:2px
    class Agenda,Discovery,Dedupe,Notes,Literature,Argument,Review,Chapter,Evidence,Trace,Citation,Continuity,Proposal,Comps,Release gate
```

You can enter the workflow at any stage. The research intent router chooses the smallest useful skill first. The orchestrator handles broader multi-stage workflow planning.

## Stage matrix

| Stage | Primary skill | Artifact | Gate |
|---|---|---|---|
| 0. Intent routing | `research-intent-router` | Research intent route; non-contract routing output | Smallest useful skill chosen; deep lookup justified or declined |
| 0.1. Orchestration | `research-book-orchestrator` | Workflow plan | Correct route chosen; assumptions labeled |
| 1. Agenda | `scholarly-research-agenda` | Book Research Agenda | Question is answerable; scope has boundaries |
| 2. Source discovery | `systematic-source-discovery` | Source Discovery Log | Search venues separated from verified sources |
| 2.1. Candidate processing | `discovery-runner-deduper` | Candidate Matrix and Search-Log Update | Completed searches, candidates, duplicates, and screening decisions are separated |
| 2.2. Source notes and extraction | `annotation-to-source-note`, `extraction-table-builder` | Source Notes, Extraction Tables, Source Matrices | Notes preserve quote, paraphrase, metadata, and locator gaps before comparison |
| 3. Literature mapping | `literature-review-mapper` | Literature Map | Consensus, controversy, and gaps separated |
| 4. Argument design | `argument-architecture` | Thesis Tree | Claims, warrants, evidence needs, and dependencies explicit |
| 5. Adversarial critique | `counterargument-peer-review` | Peer-Review Style Critique | Strong rival explanations represented |
| 6. Chapter planning | `chapter-architecture` | Chapter Brief | Chapter function advances the thesis |
| 7. Prose revision | `scholarly-prose-editor` | Revised Passage or Style Sheet | No new unsupported claims added |
| 8. Evidence audit | `claim-evidence-ledger` | Claim-Evidence Ledger | High-risk claims flagged before citation polish |
| 8.1. Claim traceability | `claim-traceability-graph` | Claim Traceability Graph | Claims trace to source notes, citekeys, locators, or repair tasks |
| 9. Citation audit | `citation-integrity-auditor` | Citation Integrity Audit | Source-claim fit checked; missing locators flagged |
| 10. Continuity | `manuscript-continuity-editor` | Continuity Review | Concepts, thesis, tone, and repetition tracked across chapters |
| 11. Proposal | `book-proposal-scholarship` | Research Book Proposal | Comparable titles and positioning claims marked by verification status |
| 11.1. Comparable-title verification | `book-comps-verifier` | Comparable Title Verification | Comps, publication details, and positioning claims are checked before submission |
| 12. Release audit | `rights-privacy-release-auditor` | Rights Privacy Release Audit | Privacy, copyright, quote, license, credential, and local metadata risks are checked before sharing |

## Skill dependency graph

```mermaid
graph TD
    O[research-book-orchestrator]
    T[research-intent-router]
    Specialists[Specialists]
    A[scholarly-research-agenda]
    S[systematic-source-discovery]
    D[discovery-runner-deduper]
    U[annotation-to-source-note]
    Z[extraction-table-builder]
    L[literature-review-mapper]
    B[annotated-bibliography-builder]
    M[methodology-source-auditor]
    R[argument-architecture]
    P[counterargument-peer-review]
    C[chapter-architecture]
    K[case-study-integration]
    E[claim-evidence-ledger]
    G[claim-traceability-graph]
    Q[citation-integrity-auditor]
    Y[rights-privacy-release-auditor]
    N[manuscript-continuity-editor]
    W[scholarly-prose-editor]
    X[book-proposal-scholarship]
    V[book-comps-verifier]
    Contract[book artifact contract]

    T --> Specialists
    Specialists --> O
    Specialists --> A
    O --> A
    O --> S
    O --> D
    O --> U
    O --> Z
    O --> L
    O --> R
    O --> C
    O --> E
    O --> G
    O --> Q
    O --> Y
    O --> N
    O --> X
    O --> V
    A --> S
    S --> D
    D --> U
    U --> Z
    Z --> L
    S --> B
    B --> M
    L --> R
    R --> P
    R --> C
    C --> K
    C --> W
    C --> E
    E --> G
    G --> Q
    Q --> N
    N --> X
    X --> V
    X --> Y
    A --- Contract
    S --- Contract
    L --- Contract
    R --- Contract
    C --- Contract
    E --- Contract
    N --- Contract
    X --- Contract
```

## Data and artifact levels

| Level | Meaning | Examples |
|---|---|---|
| Raw material | User notes, drafts, source lists, excerpts, broad premises | Book idea, chapter draft, reading notes |
| Structured artifact | Stage output with stable fields | Agenda, search log, literature map, thesis tree |
| Prepared source work | Source-bound notes, extraction rows, deduped candidates, screening records | Source notes, source matrix, duplicate clusters |
| Audited artifact | Artifact after evidence or citation checks | Claim ledger, citation audit, continuity review |
| Proposal artifact | External-facing synthesis | Book proposal, sample-material plan |

JSON artifacts must use `schema_version: "book-artifact-v1"` and one artifact type listed in the contract.

## Quality gates

| Gate | Blocks on | Why it matters |
|---|---|---|
| Intent route gate | Unclear research intent, artifact stage, source access, or risk level | Prevents noisy skill chains and premature deep lookup |
| Scope gate | Vague central question or undefined audience | Prevents scope drift |
| Source gate | Unclear source strategy or undocumented search path | Prevents cherry-picking |
| Candidate gate | Completed searches, duplicate records, and screening decisions are mixed | Prevents false corpus confidence |
| Source-note gate | Quotes, paraphrases, summaries, interpretations, metadata, or locators are mixed | Prevents weak notes from becoming draft claims |
| Extraction gate | Sources are compared before extraction is even enough | Prevents premature synthesis |
| Literature gate | One-sided literature map | Prevents literature blindness |
| Argument gate | Topic outline without thesis dependency | Prevents chapters that only summarize |
| Counterargument gate | No strong rival explanation | Prevents brittle thesis framing |
| Chapter gate | Chapter has a topic but no argumentative function | Prevents chapter drift |
| Evidence gate | Claims stronger than evidence | Prevents overclaiming |
| Traceability gate | Claims do not connect to source notes, citekeys, locators, or repair tasks | Prevents orphan claims |
| Citation gate | Citation near a claim but not verified as support | Prevents source-claim mismatch |
| Continuity gate | Contradictions, repetition, or concept drift across chapters | Prevents manuscript-level incoherence |
| Proposal gate | Unverified comparable titles or overstated positioning | Prevents fabricated market claims |
| Release gate | Private notes, copied source text, missing quote locators, license problems, or credentials appear in shared artifacts | Prevents avoidable release risk |

## Package structure

```text
.
  plugin manifest directory/plugin.json
  docs/
    ARCHITECTURE.md
    SKILL_INDEX.md
    WORKFLOW_PLAYBOOK.md
    QUALITY_STANDARD.md
  examples/
    book_artifacts/
  scripts/
    check_book_artifact_contract.py
    validate_plugin.py
  shared/
    contracts/book/book_artifact.schema.json
  skills/
    research-book-orchestrator/
      SKILL.md
      agents/openai.yaml
      assets/
```

The `skills/*/assets/` folders currently hold templates or checklists. Nothing depends on that folder name today. If the package later needs academic-pipeline naming, those folders can be renamed to `templates/` in one mechanical cleanup.
