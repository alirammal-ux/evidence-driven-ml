# Understanding the data: documentation, literature and EDA (phases A and B)

Contents: 1 Reading the documentation and the literature · 2 Goals of the EDA · 3 EDA checklist ·
4 From insights to decisions · 5 Output of the phase

The plan is only as good as the understanding of the data behind it. Metrics, splits, preprocessing, loss, augmentation,
baselines and even the framing of the task are chosen *after* this phase, from what it found. A plan written before it
is a guess.

## 1. Reading the documentation and the literature

Read, in depth, everything the user provides and the primary sources of the dataset, and write a short summary in the
user's documents (what each source says that matters for the project, with the exact wording when it defines a label).

- **The dataset paper and datasheet**: how the data were collected, the acquisition settings, the splits, known noise
  sources and limitations, what the authors measured and how.
- **The annotation protocol**: what counts as a positive, how borderline cases are treated, who annotated and how many
  times, how outlines were drawn. These define what the labels can and cannot mean; every later statement about the
  labels must stay within them.
- **Metadata files**: what is recorded per image (acquisition, subject, annotator, round), what is missing.
- **Prior work on the same data**: methods, metrics, matching criteria, post-processing and the reported numbers. Check
  how their metrics are computed (read their code when it is public) before comparing with them: differences in the
  matching rule or the counting formula can make numbers incomparable.
- **The domain**: what the signal is physically or biologically (e.g. what a marker stains and why intensity varies),
  which errors matter in practice.

Example (cell-segmentation project, illustration only): the protocol said that borderline cells require "subjective
judgment" and "a conservative approach", and the datasheet named "the intrinsic subjectivity" of the task as the main
source of noise. This later explained why most remaining errors were yes/no decisions on faint cells.

## 2. Goals of the EDA

The EDA is not a set of default plots. Its goal is to extract as many insights as possible that change a decision:

- what the task really is (what is labelled, at which unit, with which difficulty);
- where the signal is and how it varies;
- how the labels behave (consistency, conventions, defects, regularities);
- what will make the task hard (imbalance, size, crowding, artefacts, domain shifts);
- what the metric and the evaluation protocol must account for.

Write each insight as a sentence with its number, and next to it the decision it supports.

## 3. EDA checklist

Run these, adapt them to the data type, and show the numbers to the user.

- **Inventory and pairing**: counts per split, every input with its label and vice versa, orphans, duplicates, file
  formats and value ranges.
- **Label integrity**: cross-check against independent sources (official counts, metadata, polygons against masks);
  defects (fragments, overlaps, holes) with an impact table per split before and after cleaning; connectivity and other
  conventions that change the number of objects.
- **Label statistics**: class balance at the levels that matter (pixels, objects, images, subjects); objects per image;
  object size and shape distributions (smallest and largest objects decide crop size, receptive field, minimum area).
- **Signal**: which channels or features carry the information, intensity of objects against background, variability
  across images and acquisition sessions (it sets normalisation and augmentation ranges).
- **Regularities and conventions in the labels**: e.g. objects at the image border, minimum size, how touching objects
  are separated. Measure them; whether to exploit them is a decision for the user.
- **Difficulty**: crowding (distance between objects), faint or borderline cases, artefacts, examples of each.
- **Leakage and shift**: same subject in several splits, differences between splits or acquisition settings.
- **Visual review**: random samples with labels overlaid, at the same scale, plus the extremes of each distribution.

Keep the EDA in a notebook with simple code and analytical text; each section ends with its insight and decision.

## 4. From insights to decisions

Close the phase with a table, copied into `HYPERPARAMETERS.md` and `DECISIONS.md`:

| Insight (with number) | Decision it supports |
|---|---|
| Objects cover 0.6% of the pixels | Loss that is insensitive to imbalance (e.g. BCE + soft Dice) |
| Objects 18–48 px in diameter | Crops of 512 px, receptive field above ~2× the largest object, minimum area |
| Signal only in the green channel, brightness varies ×0.7–1.5 across images | One global normalisation; brightness augmentation in that range |
| Up to 67 objects per image, median 12 | Splits stratified by objects per image; object-level metric with per-image resampling |
| Borderline cases are subjective (protocol) | Report the share of errors on borderline cases; do not attribute them to the model alone |

(The rows above are illustrations from a past project.)

The metrics are chosen here or in the plan, from these insights and from the use of the output — not before.

## 5. Output of the phase

- The EDA notebook and, if needed, the cleaned labels with their impact table.
- A summary of the documentation and literature (with exact quotes for label definitions).
- The insight → decision table in `HYPERPARAMETERS.md` and the decisions in `DECISIONS.md`.
- A list of open questions for the user. Then stop for review before planning.
