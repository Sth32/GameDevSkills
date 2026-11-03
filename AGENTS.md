# Repository Agent Rules

## Design changes

Before durable workflow, document-model, stage-gate or review changes, read [principles](docs/skill-development/principles.md) and the relevant specification. Principles are the sole short list of recurring decision rules; put mechanisms, exceptions and examples in the relevant specification.

## CI closure

Every Agent-originated change includes validation and CI closure:

1. Run relevant local checks. After pushing, inspect every relevant Actions run, including runs on automated follow-up commits.
2. On failure, inspect jobs/logs and fix clear, local, low-risk, verifiable causes; rerun affected checks. Uncertain or high-impact fixes require reporting the workflow, failed step, root-cause evidence and decision/blocker.
3. Do not claim completion while relevant runs are queued, running, failed, cancelled or unresolved. A later green run supersedes a failure only through an identified fix or intentional generated follow-up whose final CI is green.

When monitoring, investigate new CI failures under this same rule rather than only forwarding notifications.

## Inherited Agent/bot attribution

When materially continuing, correcting or refactoring another Agent/bot's work, retain known producer attribution in the commit subject: `... (by <producer>)`. Name all material producers; use reliable workflow provenance, not a human/shared Git author identity. Omit unknown attribution and unrelated neighboring edits. This suffix does not replace Git author/committer metadata or applicable `Co-authored-by` trailers.
