# book-comps-verifier

## What it does

Use this skill to verify comparable titles and positioning claims for research nonfiction proposals, pitches, grants, fellowships, and press planning.

It checks whether each comp is real, current enough, and actually comparable by topic, audience, method, form, or press category.

## When to use it

Use it before sending a proposal, pitch, query, grant application, or press packet that names comparable titles or makes audience, market, timeliness, or positioning claims.

Use it when the comps sound plausible but have not been checked.

## Good inputs

- Comparable-title list or proposal section.
- Book premise, audience, method, form, and target press category.
- Known source pointers for title, author, publisher, year, or edition.
- Audience, market, why-now, or positioning claims that need review.

## Example requests

```text
Verify these comparable titles for my research nonfiction proposal.
```

```text
Check whether these comps fit by topic, audience, method, form, and press category.
```

```text
Flag stale, mismatched, fabricated, or unverified comps in this proposal section.
```

## Typical output

Expect a comparable-title verification table, positioning notes, source basis, stale or mismatched comp flags, audience and market claim checks, and missing verification tasks.

## Procedure

Follow the shared procedure in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Quality checks

Apply the shared quality checks in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; keep any skill-specific caveats visible in the output.

## Failure modes

Use the shared failure modes in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; call out the skill-specific failure most relevant to the request.

## Files/folders it may read

Follow the shared read boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Files/folders it may write

Follow the shared write boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## What it must not do

Follow the shared prohibitions in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Best next steps

After this skill, use `book-proposal-scholarship` to fold verified comps into the proposal. Use `rights-privacy-release-auditor` before sending the proposal packet outside the project.
