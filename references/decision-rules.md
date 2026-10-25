# Decision rules and the use of the data (phases C and D)

Contents: 1 Roles of the data · 2 The paired bootstrap · 3 The adoption rule · 4 Gates and multiple comparisons ·
5 When validation is too small · 6 Second-stage models · 7 The test set · 8 Reporting numbers

A rule is only useful if it is written before the result it judges. Put every rule in `DECISIONS.md` with its date, before the
run, and apply it as written; if it turns out to be badly designed, change it for the next comparison and say so.

## 1. Roles of the data

| Data | Used for | Never used for |
|---|---|---|
| Training | fitting; pre-selecting variants with out-of-fold estimates | reporting performance |
| Validation | choosing the checkpoint; confirming a few pre-selected changes | exploring many options |
| Cross-validation folds | comparisons the user judges worth the cost (see section 5) | — |
| Test | one final evaluation of a pipeline declared in advance | any choice |

Every image used to choose something is no longer an unbiased measure of that choice. Keep the number of looks at
validation small and count them.

## 2. The paired bootstrap

- Resample the *units* that were sampled independently (images, patients, documents), not pixels or objects, which are
  correlated inside a unit.
- *Paired*: both systems are evaluated on the same resampled units in each iteration. This removes the variability shared
  by the two systems (hard and easy images) and measures only the difference.
- Recompute the metric from the resampled rows in each iteration (e.g. pooled F1 from summed TP/FP/FN), with the same
  definition used for the point estimate.
- 2000 resamples and a fixed seed; the interval is the 2.5–97.5 percentile range of the differences.
- Reading: interval entirely above zero → demonstrably better; entirely below → demonstrably worse; containing zero →
  not demonstrable either way (which is not "equal").
- `scripts/paired_bootstrap.py` implements it for per-unit rows (`f1:tp,fp,fn` or `mean:<column>`); import its
  `paired_bootstrap` function for other metrics.

## 3. The adoption rule

A typical rule: a change is adopted only if the interval of the main-metric difference lies entirely above zero *and* no
guard metric is demonstrably worse. Write alongside it:

- the main metric and the guard metrics, with their direction (higher or lower is better);
- the comparison: variant − currently adopted pipeline, on the same units;
- parsimony in both directions: a more complex option must be demonstrably better; a simpler one is adopted unless it is
  demonstrably worse (decide which of the two applies before the comparison);
- what the user will be asked if the result is mixed (e.g. better precision, worse recall).

## 4. Gates and multiple comparisons

- When many options are screened on training out-of-fold estimates, only those with a gain above a gate (e.g. ≥ +0.005)
  go to validation. A gate of "> 0" lets noise through: in the cell project a +0.0001 gain passed it.
- Each extra comparison on the same validation set raises the chance of a false positive. Keep comparisons few, say how
  many were made, and treat a borderline pass as a reason to replicate (another seed, cross-validation) rather than to
  adopt.

## 5. When validation is too small

- The width of the interval shrinks roughly with the square root of the number of units: in the cell project the F1
  interval was about ±0.016 on 43 validation images and about ±0.007 with 5-fold cross-validation on 212 images.
- Validation is the default for comparisons. A k-fold cross-validation (k models trained with the same recipe, each
  unit predicted by the model that did not see it, comparisons on all units) costs k trainings: in the cell project about
  5 GPU-hours per recipe, so about 10 hours for a comparison of two recipes. Propose it, with its cost, only when it is
  worth it: the expected gain is smaller than the validation half-width and the decision matters (e.g. it changes the
  delivered pipeline), or the project is consolidated and the cross-validation adds completeness. The user decides
  whether and when to run it.
- Use the last checkpoint of each fold (the best-on-validation checkpoint would be chosen on the very images being
  compared).
- A single training run hides the run-to-run variability: a variant can win on one run by chance. Say so in the report,
  and use the cross-validation (or extra seeds) when the decision matters.

## 6. Second-stage models

A model trained on the outputs of another (a classifier of predicted objects, a calibration, a stacker) must be trained
on outputs for data the first model did not see. Predictions on the first model's own training images are too good, so
the second stage learns from easier, less numerous errors and its out-of-fold estimate is optimistic. Use out-of-fold
predictions from the cross-validation models. In the cell project the share of unannotated objects was 18% on the
network's own training images against 23% on validation; refitted on out-of-fold predictions, the classifier kept the
same validation F1 and its own estimate dropped from an optimistic 0.841 to 0.824, close to validation.

## 7. The test set

- Declare the final pipeline in `DECISIONS.md` (every component, every threshold, the frozen files) and the metrics and
  comparisons to report, before evaluating the test set.
- Run the evaluation once, report every number, then change nothing.
- If a later change needs a new test evaluation, declare it in `DECISIONS.md` beforehand and keep the earlier results; how to
  present this in the deliverables is the user's decision.

## 8. Reporting numbers

- Compute from exact values and round once, at the end: in the cell project an interval was first written as
  [+0.013, +0.022] because 0.01248 had been rounded twice.
- Report the interval next to every main number, and the unit it was resampled over.
- Report unfavourable results and options tried and not adopted, with the result that justified the decision.
