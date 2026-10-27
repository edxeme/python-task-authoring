# Python Task Authoring

**Edwin "Ed" Martinez** · [github.com/edxeme](https://github.com/edxeme) · [LinkedIn](https://www.linkedin.com/in/edxeme)

> Production-grade Python, containerized and verified. Four complete coding-task
> artifacts — failing tests in, green tests out, every solution explained.

## What each artifact demonstrates

| Skill | Artifact | Proven in production |
| :--- | :--- | :--- |
| **Python on production-grade code** | Four self-contained modules (retry/backoff, pagination, CLI, pricing) with full pytest suites | ConTech AI platform (FastAPI + Strawberry GraphQL); Toptal client work |
| **Docker** | Every artifact builds and runs its verification suite in its own container | Terminal-bench/Harbor Docker environments; Terraform + LocalStack IaC labs |
| **Git** | Solutions ship as golden unified diffs applied with `git apply` | Claude Code HFI trajectory analysis — worktrees, multi-turn sessions, diff inspection |
| **Debugging** | `02-bugfix`: failing test → root cause → minimal patch → regression reasoning | −45% DB latency via query tuning; CWE-classified security audits (8 attack vectors) |
| **Reading large codebases** | `01-comprehension`: runtime-behavior questions with verified, test-backed answers | Agentic benchmark design across 20+ Claude Opus 4.7 episode trajectories; SWE-bench full-trace |
| **Authoring + validating tasks** | Per artifact: `task.yaml` metadata, verifier suite, golden patch, written reasoning | Rubric-based model grading (bug fixes, refactors, security) across JS/TS/Java/Python; TDD human-data generation |

## What a complete task artifact contains

Every example is structured as the artifact a benchmark grader would receive:

- `README.md` — the task statement (what the model/author must do)
- `task.yaml` — machine-readable metadata: id, type, difficulty, skills, verifier
- `src/` — the module under task (buggy, incomplete, or legacy)
- `tests/` — the verifier suite that decides red vs. green
- `solution/` — the **golden patch** (`solution.patch`) or reference answer, plus the
  written reasoning a human grader (or an LLM rubric) would check

## Layout

```text
examples/
├── 01-code-comprehension   # read a retry/backoff decorator, explain runtime behavior
├── 02-bugfix-pagination    # off-by-one in total_pages — red suite, minimal fix
├── 03-feature-cli-search   # add a `search` subcommand — spec, red tests, patch
└── 04-refactor-pricing     # nested legacy pricing → guard clauses, suite stays green
```

## How to run

Requires Docker and Make.

```sh
make test     # run every suite in its own container
              # task state: 01 and 04 GREEN · 02 and 03 RED (that is the task)
make solve    # apply all golden patches, then re-run the full matrix — all green
make revert   # restore the pristine task state
```

Each example can also be run standalone:

```sh
cd examples/02-bugfix-pagination
docker build -t pta-02 . && docker run --rm pta-02
```

---

*bricks → bytes*
