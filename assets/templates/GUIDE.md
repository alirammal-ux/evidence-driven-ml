# Guide to the scripts — <project name>

Run everything from the repository root with `python -m <folder>.<script>`.

```bash
# shortcuts used below
IMG=<images folder>
LBL=<labels folder>
SPLIT=<splits/split.json>
```

## Important paths
- `data/` — <...> (not in git)
- `splits/` — <...>
- `runs/<run>/` — one folder per training: checkpoint, `config.json`, `log.csv`, saved predictions

## A new run, step by step
1. <local dry run on a few images>
2. <training on Kaggle/Colab>
3. <download and extract into runs/>
4. <predictions and comparison with the adopted pipeline>

## Training (GPU)
| Script | What it does | Command |
|---|---|---|
| <...> | <...> | `<...>` |

## Evaluation (CPU)
| Script | What it does | Command |
|---|---|---|
| <...> | <...> | `<...>` |
