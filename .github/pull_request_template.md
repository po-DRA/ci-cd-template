## What does this PR do?

<!-- Describe the change clearly. Link to an issue if one exists. -->
<!-- Example: "Fixes #12 — model now handles missing cholesterol values" -->


## Type of change

- [ ] Bug fix
- [ ] New feature / new test
- [ ] Refactoring (no behaviour change)
- [ ] Documentation update
- [ ] Dependency update (Dependabot)

## How to test

<!-- Tell reviewers exactly how to verify the change works. -->
<!-- Example: "Run pixi run test — the new test_classify_risk_boundary passes." -->


## Checklist

<!-- Complete every item before requesting a review. -->

- [ ] `pixi run test` — all tests pass
- [ ] `pixi run coverage` — coverage is still ≥ 80 %
- [ ] `pixi run lint` — no linting errors (`All checks passed!`)
- [ ] `pixi run format` — code is correctly formatted
- [ ] `pixi run typecheck` — no mypy errors (if you touched `src/`)
- [ ] Snapshots updated if output changed (`pixi run test --snapshot-update`)
- [ ] README updated if behaviour or commands changed

---

> **Teaching note:** In a professional team, every code change goes through a PR.
> The checklist above mirrors what automated CI checks on each push.
> A reviewer approves the PR only when all checks are green.
