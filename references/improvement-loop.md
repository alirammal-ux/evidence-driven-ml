# The improvement loop (phase C)

Contents: 1 Diagnose · 2 Hypothesize · 3 Propose · 4 Fix the protocol · 5 Implement or prepare the run ·
6 Verify what came back · 7 Evaluate · 8 Report and judgement · Examples

The loop decides what to add to (or remove from) the pipeline. Each pass starts from measured errors, spends effort only
on ideas whose ceiling justifies it, and ends with the user's decision recorded in `DECISIONS.md`. The three stops (after 3,
after 5 when a GPU run is needed, after 8) are where the user chooses, runs and judges.

## 1. Diagnose

Use the predictions saved on disk; diagnosis should not need retraining.

- **Error decomposition.** Classify every error and count each class. For object-level tasks:
  - false positive *isolated*: a predicted object with no labelled pixel under it;
  - false positive *partial*: a fragment or a poor outline of a labelled object (overlap below the matching threshold);
  - false negative *missed*: a labelled object with no predicted pixel on it;
  - false negative *partial*: a labelled object only partly covered;
  - *merge*: one predicted object covering two or more labelled objects;
  - *boundary* error: matched objects whose outline is imprecise.
  Use the analogous classes for other tasks (confusion between specific classes, errors by subgroup, by size, by source).
- **Oracles.** For each error class, recompute the main metric as if that class were fixed perfectly. Each oracle is the
  ceiling of any method that attacks only that class; together they show where the margin is.
- **Training against validation.** Compute the same metric on the training images, with the same pipeline. Write the
  reading rule *before* computing it, e.g. "gap below 0.05 → the model does not fit its own training labels better than
  new ones: the limit is label ambiguity or capacity, not generalisation; gap above 0.10 → generalisation problem".
  Separate capacity from label ambiguity with a larger model: if it does not fit the training labels better either,
  capacity is not the limit.
- **Look at examples.** Seeded random examples of each error class, at the same scale, with the labels overlaid.
- **Label consistency** when errors concentrate on ambiguous cases: compare the measured properties (e.g. contrast) of
  labelled and unlabelled-but-predicted objects; a single feature with low separability (AUC near 0.5–0.7) and many
  "inversions" (unlabelled objects stronger than labelled ones in the same image) mean that part of the error is not
  reducible with that information.

## 2. Hypothesize

For each large error class write one or two hypotheses: the mechanism, the change that would test it, and the result
that would refute it. Prefer hypotheses that explain the largest oracle gaps.

## 3. Propose

Present a table (kept in `PROPOSALS.md`) and recommend one row; then stop and let the user choose.

| # | Proposal | Error class attacked | Ceiling (oracle) | Expected gain | Work | GPU hours | Risk | Fits the deadline |
|---|---|---|---|---|---|---|---|---|

- **Ceiling before building.** When a proposal adds a stage, estimate its best possible effect before writing it. For
  example, for a stage that adds candidate objects from a second detector: the F1 obtained if a perfect verifier added
  exactly the true candidates. Adding a group of objects raises F1 only if the group's precision exceeds F1/2, so check
  whether such a subset can plausibly be found.
- **Costs from measurements**: epochs per hour and seconds per image measured on the actual hardware.
- **Already tried**: list the earlier attempts and their results, so that nothing is proposed twice without a new reason.
- Explain the recommendation in terms of ceiling, cost and risk.

## 4. Fix the protocol before running

Write in `DECISIONS.md`, before any result exists:

- the data that select (training out-of-fold estimates) and the data that confirm (validation by default; a
  cross-validation when the user judges it worth its cost);
- the gate to reach validation, above the noise level (e.g. out-of-fold gain ≥ +0.005, not "> 0");
- the comparison (variant − adopted pipeline, paired over the same units) and the adoption rule (`decision-rules.md`);
- the guard metrics, all of them by name (a guard that is not listed will be forgotten);
- what happens if it passes: the pipeline is re-declared; whether the test is evaluated again, declared in advance.

## 5. Implement or prepare the run

- Smallest change that tests the hypothesis; new options default to the old behaviour, and the old outputs are checked to
  be reproduced exactly (`engineering.md`).
- For a GPU run, prepare a Kaggle or Colab notebook and the code package, dry-run it locally in probe mode with simulated
  paths, and give the user exact instructions: what to upload, which settings, what to download and where to put it.
  Then stop until the results come back.

## 6. Verify what came back

- The code inside the remote run equals the local code (compare the files).
- The saved configuration equals the recipe plus the declared change, and nothing else.
- The logs are complete (all epochs, the expected checkpoint epoch).
- A metric recomputed locally from the saved predictions equals the value logged remotely (to rounding).
- Predictions align by name with the labels, not by position.
Report any mismatch before evaluating anything.

## 7. Evaluate

- Run the pipeline and the metrics on the agreed data only; never on the test set.
- Compute the main metric and every guard metric the data allow (e.g. the count error whenever object counts are
  available), each with its paired-bootstrap interval (`scripts/paired_bootstrap.py`). If a guard cannot be computed
  (missing or invalid data), say so explicitly.
- If the project's rule is not at hand, state the rule you assume and ask the user to confirm it; never present it as
  the project's rule.
- Apply the rule as written, even when the result sits just below the gate.
- Label every analysis outside the protocol as descriptive; it can motivate a new pass of the loop, not a decision now.
- Explain the mechanism object by object: what was gained, what was lost and through which error class. It often shows
  that a gain comes from somewhere other than the hypothesis.

## 8. Report and judgement

Give the user: a table (variant against the adopted pipeline, with intervals), the verdict of the rule, a one-paragraph
interpretation, the limitations (a single training run, validation images already used, number of comparisons made) and
a recommendation. Then stop: the user decides. Record the result and the decision in `DECISIONS.md`, negative results included,
and update the status and the "already tried" list in `PROPOSALS.md`.

## Examples from the cell-segmentation project

Illustrations from a past project, to show how the method works. Never cite them as facts about the user's project.


- **Where the margin was.** 86% of the object errors were yes/no decisions on faint cells. Oracles: removing every
  isolated false positive would raise F1 from 0.802 to 0.899, finding every missed cell to 0.873, fixing every partial
  segmentation to 0.831. Outlines were already at the precision of the hand-drawn polygons (about 1 px), so boundary
  losses were not pursued.
- **Training against validation.** F1 0.827 on the training images against 0.791 on validation (gap below the 0.05 fixed
  beforehand) with identical pixel Dice; a network with 4× the parameters did not fit the training labels better.
  Conclusion: label ambiguity, not generalisation or capacity; autoencoder pre-training and stronger augmentation were
  dropped before spending GPU time on them.
- **Ceiling before building.** Candidates from a classical detector added to the network's objects: perfect-verifier
  ceiling +0.012 to +0.042 F1, but only 3–5% of the candidates were true and the break-even precision was about 0.42.
  The verifier found no useful subset (+0.0001) and the idea was closed.
- **A gate must exceed the noise.** A gate written as "gain > 0" let a +0.0001 gain through to validation; later gates
  used ≥ +0.005.
- **Small validation sets mislead.** A variant passed the rule on 43 validation images (F1 +0.019, interval
  [+0.006, +0.034]); the 5-fold cross-validation on 212 images, declared before its results, gave +0.001
  [−0.007, +0.010]. Not adopted: the validation result did not replicate, and with one training run per variant the
  variability between runs was never measured.
- **Parsimony.** A block holding 62% of the reference architecture's parameters brought no demonstrable gain on this
  data. Before the pipeline-level comparison the rule was written as "adopt the lighter network unless demonstrably
  worse"; the result was F1 −0.002 [−0.012, +0.008], and the lighter network was adopted.
- **Mechanism, object by object.** A loss change meant to reduce merges gained 24 cells and lost 5 on validation. Object
  by object, the network's merges did not decrease (cells inside merges 24 → 25), while fragments halved (21 → 11): the
  metric improved, but not for the hypothesised reason.
- **Applying the rule as written.** Test-time augmentation gave +0.0048 on the training images against a gate of +0.005:
  closed, validation never looked at.
