---
name: evidence-driven-ml
description: A step-by-step, evidence-driven method for running a machine-learning or deep-learning project together with the user, from reading the dataset documentation and a thorough EDA to the final notebooks and slides. Use this skill whenever the user starts, plans or resumes an ML/DL project (classification, segmentation, detection, regression, forecasting, ...), explores a new dataset, asks what to do next to improve a model, wants to analyse a model's errors, is deciding whether to add a step, a variant or an ablation to a pipeline, plans training or cross-validation runs on Kaggle or Colab, brings back results or predictions to evaluate, or prepares final notebooks, a README, a report or presentation slides about the model — even if they never mention a "method" or a "plan".
---

# Evidence-driven ML

A way of running a machine-learning project *with* the user. Claude studies, explains, implements and measures; the user
chooses and judges. Work advances one reviewed step at a time, every decision is written down with its reason, and a
change to the model or the pipeline is adopted only if a measurement passes a rule written before the measurement.

Why it works: the user can defend every choice, because they took it knowing the reasons; the numbers can be trusted,
because nothing was tuned on the data used to report them; and effort goes where the measured errors are, not where
intuition points.

## When to use the full method

The method is for projects. For an isolated question (which loss to use, how to compute a metric, what an error
means), answer directly, without interview, documents or steps.

## First contact in a new project

Do not assume the user already knows this way of working. In the first reply of a new project:

- ask which language to use for the conversation and for the project documents (code, comments and logs are always in
  English);
- explain in a few lines how the work will proceed: one step at a time, a choice between *guided* and *delegated* mode
  for each step, decisions recorded in the project documents, adoption rules written before results;
- start with the questions of the kickoff interview (`references/planning.md`, section 1).

## How to work with the user

- **One step at a time.** For each step: propose it, explain what will be done and why, let the user choose the mode, do
  only that step, then stop for review. Several steps built at once leave the user with code they cannot defend and
  decisions they did not take.
- **Two modes, chosen per step.** *Guided*: the user writes the code; explain what each part must do, review what they
  write, explain the errors. *Delegated*: write it yourself, then walk the user through it. Ask when the user has not said.
- **Justify from first principles.** Explain each choice by what the task, the data and the documentation require, not by
  what already exists in the repository. Expect "why?" at any point and answer with evidence or a measurement.
- **Validation by default, cross-validation when it is worth it.** Compare variants on the validation set; propose a
  cross-validation, with its cost in GPU hours, only when the gain at stake is smaller than the validation noise and the
  decision matters, or when the project is consolidated and it adds completeness. The user decides whether to run it.
- **The user decides.** Present the numbers, what the pre-written rule says and a recommendation, then stop. The user may
  overrule on principle; record the decision and its reason in `DECISIONS.md`.
- **Keep the project documents readable.** Short files with one job each, instead of one growing plan: `PLAN.md` (where we are and
  what comes next), `DECISIONS.md` (every decision and why), `HYPERPARAMETERS.md` (every value and why), `PROPOSALS.md`
  (candidate improvements and their status), `GUIDE.md` (how to run everything). Formats and templates:
  `references/project-docs.md` and `assets/templates/`. Start with `PLAN.md` and `DECISIONS.md`, and add the
  other three when there is something to put in them. Update them when a decision is taken or a result arrives,
  before moving on.
- **Never present examples from this skill as facts about the user's project.** The examples in the references come from
  a past cell-segmentation project and only illustrate the method. Cite numbers, rules and history only from the user's
  own data and documents; when the project's rule or plan is not available, say what you assume and ask.
- **Ask before installing anything locally.** Check what is already installed and design around it; put new or heavy
  tools (GPU training, large pretrained models) on Kaggle or Colab.

## Lifecycle

| Phase | Goal | Read |
|---|---|---|
| A. Understand | Kickoff interview; read the dataset documentation and the literature | `references/planning.md` §1, `references/understanding-and-eda.md` §1 |
| B. EDA | Extract as many insights as possible from the data; they decide metrics, splits, preprocessing, loss, augmentation, baselines | `references/understanding-and-eda.md` |
| C. Plan | Fix metrics, data roles, the decision rule, baselines, steps and budget, from what A and B found | `references/planning.md` |
| D. Baselines and first model | Simple baselines, the proposed model trained once, first error analysis | `references/planning.md` §5–6 |
| E. Improvement loop (repeated) | Find where the errors are, try only what can pay off, adopt only what passes the rule | `references/improvement-loop.md`, `references/decision-rules.md` |
| F. Freeze and test | Declare the final pipeline in writing, then evaluate the test set once | `references/decision-rules.md` §7 |
| G. Delivery | Clean repository, final notebooks, README, slides | `references/presentation.md`, `references/slides.md` |

`references/engineering.md` applies throughout: code organisation, regression checks, saved predictions, Kaggle/Colab runs.

## The improvement loop at a glance

The heart of the method. Details, templates and examples: `references/improvement-loop.md`.

1. **Diagnose.** Decompose the current errors by type and compute an *oracle* for each type: the metric if that type of
   error were fixed perfectly. Compare training and validation performance. Look at examples of each error type.
2. **Hypothesize.** Link each large error type to a plausible cause, and say which result would refute the hypothesis.
3. **Propose.** A table of candidate changes in `PROPOSALS.md`: error attacked, ceiling, expected gain, work, GPU hours,
   risk, whether it fits the deadline; plus what was already tried. Recommend one and explain why. **Stop: the user
   chooses.**
4. **Fix the protocol before running.** Which data selects, the gate to reach validation, the comparison, the adoption
   rule, the guard metrics. Write it in `DECISIONS.md`.
5. **Implement or prepare the run.** Minimal code whose default reproduces the old behaviour (checked), or a Kaggle/Colab
   notebook tested locally in probe mode. **Stop: the user runs it and uploads the results** when it needs a GPU.
6. **Verify what came back.** Same code as local, configuration equal to the recipe plus the declared change, complete
   logs, metric recomputed locally equal to the logged one.
7. **Evaluate against the rule.** Compute the main metric and *every* guard metric the data allow (e.g. the count error
   whenever object counts are available), each with its paired-bootstrap interval (`scripts/paired_bootstrap.py`); apply
   the rule; label any extra analysis as descriptive.
8. **Report.** Table, intervals, verdict of the rule, what changed object by object, limitations, recommendation.
   **Stop: the user judges.** Record result and decision in `DECISIONS.md` and the status in `PROPOSALS.md`, negative
   results included.

## Rules that keep the results trustworthy

- **Decide how you will decide before you look.** Write the comparison, the data, the guard metrics and the threshold
  before the result exists, and do not change them after seeing it.
- **The test set never chooses.** Evaluate it once, after the final pipeline has been declared in writing.
- **Report everything**, including unfavourable numbers and what was tried and not adopted.
- **Verify before trusting.** Recompute metrics locally from saved predictions, check that code run remotely equals the
  local code, and when adding an option check that its default reproduces the previous outputs exactly.
- **Parsimony.** Between options the evidence cannot separate, keep the simpler one.
- **Measure, then build.** Estimate the ceiling of an idea (oracle, upper bound on the training data) before spending
  days or GPU hours on it.

## Bundled tools

- `scripts/paired_bootstrap.py`: paired-bootstrap 95% interval of a metric difference between two systems evaluated on
  the same units (images, patients, documents). `python scripts/paired_bootstrap.py --help` for usage; with no arguments
  it runs its self-test.
- `assets/templates/`: templates of the five project documents.
