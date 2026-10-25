# The project documents

One long plan becomes unreadable as a project grows. Keep five short documents in the repository, each with one job, in
the language the user chose. Templates: `assets/templates/`. Update them when something changes, before moving on, and
keep them short: a reader should find the current state in a minute.

Start with `PLAN.md` and `DECISIONS.md`. Add `HYPERPARAMETERS.md` when the first values are fixed (usually after the
EDA), `PROPOSALS.md` at the first error diagnosis, and `GUIDE.md` when the first scripts exist.

| File | Answers | Updated when |
|---|---|---|
| `PLAN.md` | Where are we, what comes next? | A step starts or ends, the plan changes |
| `DECISIONS.md` | What was decided, when, why, on which evidence, by whom? | Any decision (including "not adopted") |
| `HYPERPARAMETERS.md` | What is every value of the pipeline, and why that value? | A value is set or changed |
| `PROPOSALS.md` | What could improve the model, at what cost, and what happened to each idea? | After a diagnosis; when a proposal is tried |
| `GUIDE.md` | How do I run each script, where are the files? | A script or a path is added or changed |

## PLAN.md

- At most about one page: context in two sentences, constraints, the current pipeline in one block, the numbered steps
  with a one-line status each (✅ done with date / ▶ in progress / ☐ to do), the next step.
- No experiment details and no long reasoning: link to the entry in `DECISIONS.md` instead.

## DECISIONS.md

- An append-only log, newest at the bottom, one entry per decision:
  `### D12 — 2026-10-03 — Watershed with seeds ≥ 20 px: adopted`, then four short lines:
  **Decision**, **Why** (the reason in one or two sentences), **Evidence** (numbers with intervals, the file that holds
  them), **Decided by** (the user, or the pre-written rule).
- Protocols fixed before an experiment are entries too ("D11 — protocol for the watershed comparison"), so that the
  result can be checked against what was written before it.
- Decisions taken on principle by the user are recorded with their reason, like the measured ones.

## HYPERPARAMETERS.md

- One table per area (data and splits, model, training, post-processing, evaluation):
  | Hyperparameter | Value | Chosen | Why |
  where *Chosen* is "a priori", "from the EDA" or "measured (D12)".
- Each "why" is one or two sentences with the number behind it; longer arguments go in `DECISIONS.md`.

## PROPOSALS.md

- Where the margin is: the error decomposition and the oracles that motivate the proposals.
- One table: | ID | Proposal | Error attacked | Ceiling | Expected gain | Feasibility | Work | GPU | Status |
  with the status kept current ("not started", "running", "done, adopted (D12)", "done, not adopted (D14)", "rejected:
  reason").
- A short "already tried" list, so that nothing is proposed twice without a new reason.

## GUIDE.md

- Paths of the important files and folders; shortcuts for long arguments.
- The steps to follow for a new run, in order.
- One table per area: | Script | What it does | Command |, with the expected running time when it is long.
