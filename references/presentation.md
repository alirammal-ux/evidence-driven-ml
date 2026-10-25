# Delivery: notebooks and README (phase G)

Contents: 1 Final notebooks · 2 Writing register · 3 README · 4 Claims about the labels. Slides: `slides.md`.

## 1. Final notebooks

- Tell the story of the adopted pipeline in a few notebooks, e.g.: `01_eda` (data, documentation, cleaning, the insights
  that drive the choices) → `02_data_and_training` (splits, recipe, model, curves) → `03_post_processing` (each step of
  the pipeline and the measurement that justified it) → `04_test` (one evaluation, comparison with other methods,
  remaining errors).
- Notebooks import the code from the repository modules (one source of truth) and run on CPU; steps that need a GPU read
  the saved results and show the command behind a `RUN_TRAINING = False` switch.
- What was tried and not adopted goes in a short "Tried and not adopted" table (variant, result that justified the
  decision, where the details are); the details live in an `experiments/` folder.
- Code in notebooks is simple: short cells, plain loops, clear names, no dense one-liners.
- Every number written in the text is checked against the cell outputs after a full run.
- Once the user has edited a notebook, never regenerate it: change only the cells that must change, keep its structure
  and the user's wording.

## 2. Writing register

- Notebooks, README and reports: analytical, paper-like register — precise and impersonal; no colloquial phrasing.
- State the measurement behind each claim, with its interval when it is a comparison.

## 3. README

- Goal and data in two sentences; the adopted pipeline as a short diagram; results on the test set in a table (main
  metric with its interval, guard metrics, the baselines and references); the structure of the repository; how to get
  the data and how to run each notebook; the environment.

## 4. Claims about the labels

Write about the labels only what the dataset documents say (protocol, datasheet, paper) or what was measured. Describe
objects as "not annotated" rather than as mistakes of the annotators, and do not attribute intentions or habits to them.
