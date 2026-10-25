# Presentation slides: the style to keep (phase G)

Contents: 1 Principles · 2 Canvas and layout · 3 Typography · 4 Colour · 5 Text rules · 6 Figures and charts ·
7 A typical deck · 8 Working on the deck with the user

This is the user's own style. Keep it exactly, on every deck, unless the user asks otherwise.

## 1. Principles

- Clean and minimal: white background, one quiet sans-serif typeface, very little colour, a lot of space.
- One idea per slide: one figure or one table, few words. Speaker notes say what to tell (about one minute per slide).
- About one slide per minute of talk; ten slides for a ten-minute presentation.
- Every number comes from the README or the final notebooks; every statement about the labels stays within the dataset
  documents.

## 2. Canvas and layout

- 16:9 canvas of 1920 × 1080 px; margins 128 px left, right and top, 160 px at the bottom (content area 1664 px wide).
- **Title at the top left**, never centred, with a **thin grey line under it**: `border-bottom: 1px solid #D9D9D9`,
  about 12 px of padding below the text. Every slide except the cover has it.
- **Page number** at the bottom right: "N / total", 24 px, grey `#6B6B6B`, right-aligned, 64 px from the bottom.
- Slides with two topics get **two titles**, each with its line: stacked top and bottom (e.g. "Objective" above,
  "Challenges" below), or side by side with a thin vertical line between them (e.g. "Errors" left, "Conclusions" right).
- Cards: `1px solid #D9D9D9` border, 12 px radius, no fill. Label–value rows: grey label on the left, dark value on the
  right. Tables: no coloured fills, thin separators, grey header.
- A key rule or statement can sit in a block with a 6 px accent bar on its left, statement at about 34 px semibold, one
  grey line of detail below it at about 26 px.
- Figures aligned with the boxes or columns above them; a legend for colours in the slide text (one grey line), not
  inside the image.
- No background motifs, no coloured bands, no coloured accent under the titles (tried and rejected by the user).

## 3. Typography

- One family: Public Sans (Google Fonts, weights 400/600/700), with Arial and sans-serif as fallbacks.
- Slide title 60 px bold (`#111111`, line height about 1.15); cover title about 76 px bold; cover subtitle 32 px.
- Section titles inside a slide 28–40 px bold; body text 24–34 px; captions and legends 24 px grey. Nothing under 24 px.
- Text colours: titles `#111111`, body `#333333` or `#222222`, labels and captions `#6B6B6B`.

## 4. Colour

- One accent for what is adopted or important: green `#1E7A46` (e.g. the adopted pipeline, a key percentage).
- A second series, when a comparison needs it: orange `#E69F00` (Okabe-Ito), distinguishable from the green also with
  colour-vision deficiencies.
- Grey `#8C8C8C` for what is not adopted or secondary; dark red `#B03A2E` only for what is demonstrably worse.
- Colours in micrograph overlays follow one convention across the deck and are explained in a one-line legend (e.g.
  "Yellow: annotated cell · dashed white: unannotated object").

## 5. Text rules

- Every sentence or text item starts with a capital letter: titles, table cells, list items, captions, legends (model
  names keep their own spelling, e.g. "c-ResUNet").
- Professional, non-colloquial wording: say "retains the objects", not "keeps the stuff"; avoid spoken-style phrasing.
- Short items rather than paragraphs; numbers with their unit and, for comparisons, their interval.

## 6. Figures and charts

- Figures are produced by small scripts in the development repository (one script per slide figure), reading the
  results read-only, with checks that the plotted numbers equal the reported ones. Re-running a script must give the same
  file.
- Matplotlib, 200 dpi, Noto Sans with DejaVu Sans as fallback (for the minus sign); no top and right axes, light grid
  `#E3E3E3`, ticks and secondary text in `#6B6B6B`, main text `#333333`.
- Prefer simple forms: horizontal bars with the value written at the end of each bar, one small panel per measure with
  its own scale starting at zero (instead of a radar chart); histograms with the median or mean marked by a line and a
  label; one colour per series.
- Decisions: a forest plot of the differences with their 95% intervals, a vertical line at zero, adopted steps in green,
  not adopted in grey, demonstrably worse in red, values written only for the decisive rows, rows spaced generously.
- Pipeline: one panel per step under the boxes of the pipeline, on the same image region, with consistent outline
  colours.
- Examples of errors or of challenges: random but representative crops (fixed seed), at the same scale, explained in the
  slide text; when a crop must show something specific, say how it was chosen.
- Charts in another language: the same script with a language option, so that labels are translated and nothing else
  changes.

## 7. A typical deck

1. Cover: title, subtitle (dataset and source), author line; a figure of the path input → model → output.
2. Objective and challenges (two titles): the problem today against the automatic solution; four challenge images with
   one bold title and one line each.
3. The data: split table (images and objects per set, use of each set), three charts that support the characteristics.
4. The pipeline: one box per step with a short description, a panel per step underneath.
5. The network: architecture figure on the left, "label | value" rows for architecture and training on the right.
6. Post-processing: one card per step with the reason, an example figure below.
7. The second stage (e.g. object classifier): features and weights, the rule, examples of removed and retained objects.
8. Decision rule: the rule as a statement, a legend, the forest plot of every decision.
9. Results on the test set: table of all methods, then panels comparing the adopted pipeline with the strongest
   reference (quality, error, memory, time).
10. Errors and conclusions (two titles side by side): the main error figure and examples; result, limitations, future
   work, link to the repository.

## 8. Working on the deck with the user

- The user edits slides by hand: always re-read a slide before changing it, and keep their edits.
- Revise slide by slide, one request at a time; record figure scripts and decisions as for the rest of the project.
- When asked for a copy in another language, keep the layout identical and regenerate only the figures that contain
  text.
