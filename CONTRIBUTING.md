# Contributing

[中文说明](CONTRIBUTING.zh-CN.md)

Consistent with the design principle underlying this skill, its intended
evolution is driven by documented, concrete cases rather than by unverified
general heuristics. Contributions of the following kinds are particularly
valuable:

## Reporting an observed failure mode

If, in the course of using this skill, a specific incorrect claim reached a
final deliverable despite the mandatory fact-check pass — or a class of
research question was handled poorly — please open an issue describing:

1. The research question or task given to the model.
2. The specific claim or output that was incorrect, and why.
3. Where in the workflow (which stage in `SKILL.md`, or which file under
   `references/`) the check should plausibly have caught it but did not.

Concrete, reproducible failure cases are the primary mechanism by which this
skill improves; general suggestions without a specific observed case are
harder to act on but still welcome for discussion.

## Proposing changes

Pull requests are welcome for:

- Extending `references/` with guidance for a data type, statistical method,
  or repository not currently covered (e.g., proteomics, single-cell data,
  a repository other than GEO).
- Improving or extending the scripts under `scripts/` — provided the change
  preserves their role as adaptable components rather than turning them into
  a rigid, one-size-fits-all pipeline.
- Refining the wording of `SKILL.md` itself, particularly where a stated
  requirement could be made clearer about the reasoning behind it rather than
  stated as an unexplained rule.

When submitting a pull request, please describe the concrete scenario that
motivates the change — the same standard the skill itself applies to
biomedical claims applies here: a traceable rationale is preferred over an
unsubstantiated general improvement.

## Scope

This skill governs an analytical workflow, not a specific biomedical domain.
Contributions that make the workflow more rigorous, more general, or more
clearly explained are in scope. Contributions that hard-code assumptions
specific to a single disease area or dataset are likely out of scope unless
generalized into a `references/` guide applicable beyond that one case.
