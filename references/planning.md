# Kickoff and planning (phases A, C and D)

Contents: 1 Kickoff interview · 2 Framing from first principles · 3 Metrics · 4 Data roles and decision rule ·
5 Baselines · 6 First model and first diagnosis · 7 Steps, calendar and budget

Order matters: the kickoff interview comes first, then the documentation, the literature and the EDA
(`understanding-and-eda.md`), and only then the plan. Metrics, splits and procedures are chosen from what those phases
found. Present the plan and stop for approval before writing training code.

## 1. Kickoff interview

Ask before assuming, and ask everything that will influence the choices: the answers shape the whole project, so many
questions are better than choices built on wrong assumptions. Group the questions by theme in one message, say in a few
words why each one matters, give a proposal or a default where you have one (so that the user can simply confirm), let
the user answer in parts, and skip only what is already known from the repository, the data or the conversation.

- **Language** for the conversation and for the project documents.
- **Use of the output.** What will the predictions be used for: a count, a mask, a ranking, a decision? Which error is
  worse in practice (a miss or a false alarm)? What counts as one error, and on which unit (pixel, object, image,
  patient)?
- **Data and documentation.** Source, official splits, unlabelled data, and every document that defines the labels
  (annotation protocol, datasheet, paper). Ask for them: they are read in depth in phase A.
- **Constraints.** Deadline and the days needed for writing or presenting; compute (local CPU/GPU and RAM, Kaggle or
  Colab quotas and session limits); install policy; who launches the GPU runs.
- **Deliverables and audience.** Repository, notebooks, report, slides; who reads them.
- **Local environment.** Machine, RAM, libraries already installed, where the code will live (repositories, private
  or public).
- **Starting material and preferences.** Existing code, models and frameworks; attempts already made and their
  results; preferences on architecture or tools.

## 2. Framing from first principles

After the EDA, write in `DECISIONS.md` what the task needs and why, for example:

- per-object outlines are needed → dense prediction with an encoder–decoder and skip connections, not a regressor of
  the count;
- object size against receptive field, from the measured size distribution;
- class imbalance (fraction of positive pixels or samples) → choice of loss and of sampling;
- where the signal is (channels, modalities, time window).

Keep the discarded alternatives, each with a one-line reason; they come back as questions later.

## 3. Metrics

Choose them from the use of the output and from the EDA insights, and record the reasons in `DECISIONS.md`.

- One main metric (e.g. object F1 with IoU > 0.5 for counting cells) and the guard metrics that must not get worse
  (e.g. pixel Dice, count MAE and bias). List every guard metric explicitly: a guard that is not listed will be forgotten.
- The unit of resampling for the confidence intervals (images, patients), from the structure of the data.
- Pooled over the units (sums of counts) or averaged per unit: decide and write it down.
- Implement them with small synthetic tests: perfect prediction → 1; empty prediction on a non-empty truth → 0; two
  touching objects predicted as one → F1 below 1; empty truth and empty prediction → a defined value.
- When comparing with prior work, use their matching rule as a secondary view only after checking their code.

## 4. Data roles and decision rule

Write both in `DECISIONS.md` before any training; details in `decision-rules.md`.

- Training: fitting and pre-selection (with out-of-fold estimates whenever a second stage is trained on first-stage
  outputs).
- Validation: checkpoint choice and confirmation of a few pre-selected changes.
- Cross-validation: proposed, with its cost, only when it is worth it (validation too small for the gain at stake and an
  important decision, or a consolidated project where it adds completeness); the user decides. Estimate the width of
  the validation interval early, so that this can be judged.
- Test: once, at the end.

Rule, for example: "a change is adopted only if the 95% paired-bootstrap interval of the difference in the main metric
lies entirely above zero and no guard metric gets demonstrably worse".

## 5. Baselines, from simple to strong

- A trivial or classical baseline gives meaning to the numbers and exposes the difficulty (illustration from a past
  project: Otsu thresholding reached object F1 0.13, which made the imbalance visible; a robust threshold, median + k·MAD
  with k chosen on the training images, reached 0.51).
- The proposed model.
- A strong external reference when one exists (e.g. a large pretrained generalist model, zero-shot and fine-tuned on the
  same training images), evaluated with the same metrics and the same post-processing. It tells whether the remaining
  gap comes from the model or from the task. Exclude pretrained weights that may have seen the evaluation data.

## 6. First model and first diagnosis (phase D)

- Overfit one tiny batch first (the loss must go to about 0) to catch pipeline bugs; then a short run to measure time and
  memory; then the full run.
- Train once with the planned recipe and check that training and validation curves are sane.
- Save the predictions on validation (and on training) to disk, so every later analysis runs on CPU without retraining.
- Then start the improvement loop with a diagnosis (`improvement-loop.md`).

## 7. Steps, calendar and budget

- Numbered steps small enough to review in one sitting, each with its goal, mode (guided or delegated), outputs and how
  it will be verified; they go in `PLAN.md`, one line each.
- GPU hours per step estimated from measured times (time one epoch early), a stop date for experiments, and days
  reserved for writing.
- Present the plan and stop for approval.
