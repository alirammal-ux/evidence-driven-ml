'''Synthetic input files for the test cases of the evidence-driven-ml skill (fixed seeds).'''
import csv
import sys
from pathlib import Path

import numpy as np

W = Path(sys.argv[1])


def spread(total, weights, rng):
    '''Split an integer total over the images in proportion to weights.'''
    return rng.multinomial(total, weights / weights.sum())


# case 2: per-image errors on 43 validation images; totals TP 550, FP 115 isolated + 25 partial, FN 100 missed + 35 partial
rng = np.random.default_rng(11)
cells = rng.integers(2, 40, 43).astype(float)
cols = {"tp": spread(550, cells, rng), "fp_isolated": spread(115, cells, rng), "fp_partial": spread(25, cells, rng),
        "fn_missed": spread(100, cells, rng), "fn_partial": spread(35, cells, rng)}
merges = np.minimum(cols["fp_partial"], spread(10, cells, rng))
with open(W / "evals/error-analysis-proposals/files/val_errors.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["image", "n_true", "n_pred", "tp", "fp_isolated", "fp_partial", "fn_missed", "fn_partial", "merges"])
    for i in range(43):
        tp, fpi, fpp, fnm, fnp = (int(cols[k][i]) for k in ("tp", "fp_isolated", "fp_partial", "fn_missed", "fn_partial"))
        w.writerow([f"val_{i:03d}.png", tp + fnm + fnp, tp + fpi + fpp, tp, fpi, fpp, fnm, fnp, int(merges[i])])

# case 3: adopted pipeline and a variant on the same 43 images (object counts and pixel counts)
rng = np.random.default_rng(5)
px_rng = np.random.default_rng(6)                                  # pixel counts: own generator
rows = []
for i in range(43):
    n_true = int(rng.integers(3, 40))
    tp = int(rng.binomial(n_true, 0.82))
    fp = int(rng.poisson(0.22 * n_true))
    rng.normal(700, 60)                                              # draw kept: object counts stay as before
    area = int(n_true * px_rng.normal(700, 80))                      # annotated area, the same for both systems
    px_tp = int(area * px_rng.uniform(0.72, 0.86))
    rows.append([f"val_{i:03d}.png", tp, fp, n_true - tp, tp + fp, n_true, px_tp, int(fp * px_rng.normal(450, 60) + px_tp * px_rng.uniform(0.04, 0.12)), area - px_tp])
rng = np.random.default_rng(14)                                  # the variant's own changes
variant = []
for r in rows:
    name, tp, fp, fn, n_pred, n_true, px_tp, px_fp, px_fn = r
    d_tp = int(np.clip(rng.integers(-1, 4), -tp, fn))          # a few more cells found, sometimes fewer
    d_fp = int(max(-fp, rng.integers(-1, 3)))                    # and a few more false positives
    tp2, fp2 = tp + d_tp, fp + d_fp
    rng.normal(0, 400)                                               # draw kept: object counts stay as before
    area = px_tp + px_fn
    px_tp2 = int(np.clip(px_tp + d_tp * px_rng.normal(600, 80) + px_rng.normal(0, 300), 0, area))
    px_fp2 = int(max(0, px_fp + d_fp * px_rng.normal(450, 60) + px_rng.normal(0, 200)))
    variant.append([name, tp2, fp2, n_true - tp2, tp2 + fp2, n_true, px_tp2, px_fp2, area - px_tp2])
header = ["image", "tp", "fp", "fn", "n_pred", "n_true", "px_tp", "px_fp", "px_fn"]
for name, data in (("adopted_counts.csv", rows), ("variant_counts.csv", variant)):
    with open(W / "evals/evaluate-uploaded-variant/files" / name, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data)
