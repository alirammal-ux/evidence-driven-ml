'''Paired-bootstrap 95% interval of a metric difference between two systems evaluated on the same units.

Units are the items sampled independently (images, patients, documents). Each system gives one row per unit (e.g. the
per-image TP, FP and FN counts, or a per-image score); row i of A and row i of B must refer to the same unit. Every
resample draws n units with replacement and recomputes the metric of A and of B on the SAME units, so the interval
measures the variability of the difference. The metric is recomputed from the resampled rows (a pooled F1 from summed
counts, or a mean), with the same definition as the point estimate.

As a module:
    from paired_bootstrap import paired_bootstrap, f1_from_counts, mean_of
    diff, low, high = paired_bootstrap(rows_a, rows_b, f1_from_counts(0, 1, 2))
From the command line (CSV files with a header, one row per unit; rows are matched by --key when given, else by order):
    python paired_bootstrap.py --a variant.csv --b adopted.csv --metric f1:tp,fp,fn --key image
    python paired_bootstrap.py --a variant.csv --b adopted.csv --metric mean:abs_count_error
With no arguments it runs its self-test.'''

import argparse
import csv
import sys

import numpy as np


def paired_bootstrap(rows_a, rows_b, metric, n_boot=2000, seed=0):
    '''metric(A) − metric(B) on all units, and the 2.5 and 97.5 percentiles of the difference over n_boot paired
    resamples of the units.'''
    rows_a = np.asarray(rows_a, dtype=float)
    rows_b = np.asarray(rows_b, dtype=float)
    assert len(rows_a) == len(rows_b), "A and B need one row per unit, for the same units"
    rng = np.random.default_rng(seed)
    n = len(rows_a)
    diffs = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)          # n units with replacement, the same for A and B
        diffs.append(metric(rows_a[idx]) - metric(rows_b[idx]))
    low, high = np.percentile(diffs, [2.5, 97.5])
    return metric(rows_a) - metric(rows_b), low, high


def f1_from_counts(tp, fp, fn):
    '''Pooled F1 = 2·TP / (2·TP + FP + FN) from the TP, FP and FN columns (indices); 1 when there is nothing to find.'''
    def metric(rows):
        t, p, n = rows[:, tp].sum(), rows[:, fp].sum(), rows[:, fn].sum()
        return 2 * t / (2 * t + p + n) if t + p + n > 0 else 1.0
    return metric


def mean_of(column):
    '''Mean of one column (index) over the units.'''
    def metric(rows):
        return rows[:, column].mean()
    return metric


def read_rows(path, columns, key):
    '''Rows of the named columns, as floats; with key, also the unit names in file order.'''
    with open(path, newline="") as f:
        records = list(csv.DictReader(f))
    rows = np.array([[float(r[c]) for c in columns] for r in records])
    names = [r[key] for r in records] if key else None
    return rows, names


def reading(low, high):
    if low > 0:
        return "the interval lies entirely above zero: A is demonstrably higher than B"
    if high < 0:
        return "the interval lies entirely below zero: A is demonstrably lower than B"
    return "the interval contains zero: no demonstrable difference"


def main():
    parser = argparse.ArgumentParser(description="Paired-bootstrap 95% interval of metric(A) − metric(B)")
    parser.add_argument("--a", required=True, help="CSV of system A (e.g. the variant), one row per unit")
    parser.add_argument("--b", required=True, help="CSV of system B (e.g. the adopted pipeline), same units")
    parser.add_argument("--metric", required=True, help="f1:<tp>,<fp>,<fn> or mean:<column>")
    parser.add_argument("--key", default=None, help="column with the unit name, to match rows by name")
    parser.add_argument("--n_boot", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    kind, spec = args.metric.split(":", 1)
    columns = spec.split(",")
    metric = f1_from_counts(0, 1, 2) if kind == "f1" else mean_of(0)
    assert (kind == "f1" and len(columns) == 3) or (kind == "mean" and len(columns) == 1), "bad --metric"

    rows_a, names_a = read_rows(args.a, columns, args.key)
    rows_b, names_b = read_rows(args.b, columns, args.key)
    if args.key:                                      # align B to the order of A, by unit name
        assert sorted(names_a) == sorted(names_b), "A and B do not contain the same units"
        position = {name: i for i, name in enumerate(names_b)}
        rows_b = rows_b[[position[name] for name in names_a]]

    diff, low, high = paired_bootstrap(rows_a, rows_b, metric, args.n_boot, args.seed)
    print(f"metric {args.metric}: A = {metric(rows_a):.4f}, B = {metric(rows_b):.4f}")
    print(f"A − B = {diff:+.4f}, 95% interval [{low:+.4f}, {high:+.4f}] "
          f"({len(rows_a)} units, {args.n_boot} paired resamples, seed {args.seed})")
    print(reading(low, high))


def self_test():
    rng = np.random.default_rng(1)
    base = np.column_stack([rng.integers(5, 30, 40), rng.integers(0, 6, 40), rng.integers(0, 6, 40)])   # tp, fp, fn
    f1 = f1_from_counts(0, 1, 2)

    # identical systems: zero difference, zero-width interval
    diff, low, high = paired_bootstrap(base, base, f1)
    assert diff == 0 and low == 0 and high == 0

    # B has 3 extra false positives on every unit: A demonstrably higher
    worse = base.copy()
    worse[:, 1] += 3
    diff, low, high = paired_bootstrap(base, worse, f1)
    assert diff > 0 and low > 0, (diff, low, high)

    # symmetric noise around the same system: the interval contains zero
    noisy = base.copy()
    noisy[:, 1] += rng.choice([-1, 1], 40) * (base[:, 1] > 0)
    diff, low, high = paired_bootstrap(base, noisy, f1)
    assert low < 0 < high, (diff, low, high)

    # same seed, same result; mean_of works on a single column
    assert paired_bootstrap(base, worse, f1) == paired_bootstrap(base, worse, f1)
    assert abs(mean_of(0)(base) - base[:, 0].mean()) < 1e-12
    print("self-test passed")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        self_test()
    else:
        main()
