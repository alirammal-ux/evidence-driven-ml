# Engineering habits (all phases)

Contents: 1 Repositories · 2 Code organisation · 3 Regression checks · 4 What every run saves ·
5 GPU runs on Kaggle or Colab · 6 Numerics

## 1. Repositories

- **Development repository**: everything — exploratory scripts, analyses, failed experiments, the project documents (`references/project-docs.md`), all runs.
  It can stay private and in the user's language for the documents.
- **Clean repository**, built near the end for the readers: only the adopted pipeline, the final notebooks, the frozen
  model files and the small result files the notebooks read; separate folders for other methods (`other_methods/`),
  the experiments that justified the choices (`experiments/`) and the GPU notebooks (`kaggle/`). English throughout.
- Scripts in the development repository may read the clean repository but must not write into it: run them with
  `python -B` (no `__pycache__`) and check `git status` afterwards.

## 2. Code organisation

- One job per file (e.g. model selection and the frozen chosen model in separate files); short functions; few options.
- No dead code kept "just in case": what was tried and abandoned lives in `DECISIONS.md`, `PROPOSALS.md` and `experiments/`.
- Each module has a small self-test in its `__main__`, with synthetic cases whose answer is known (a perfect prediction,
  an empty one, two touching objects, a float16 batch).
- Paths come from arguments, so the same code runs locally and on Kaggle or Colab.
- Before writing new code, search the repository for a function that already does the job and reuse it.

## 3. Regression checks

- A new option defaults to the previous behaviour. Before the change, save a reference (a few training batches, a smoke
  run log, the output files); after it, check that the default reproduces them exactly, byte for byte where possible.
- After a refactor, regenerate the affected outputs and compare them with the previous ones.
- When moving or copying code into the clean repository, compare the files and re-run its checks there.

## 4. What every run saves

- `config.json`: the full recipe (data split, seed, hyperparameters, normalisation statistics, options, hardware, mixed
  precision on or off).
- A CSV log per epoch; the checkpoint with what is needed to rebuild the model and normalise its input.
- Predictions on validation (and training, and later test) as compressed arrays with the unit names, so that every
  analysis, threshold sweep and bootstrap runs on CPU without retraining.
- Per-unit counts (e.g. TP, FP, FN, number predicted, number true per image) next to the metrics, for the bootstrap.

## 5. GPU runs on Kaggle or Colab

- Package the code as a dataset (a zip of the modules, splits and small checkpoints) and the data as another; the
  notebook stays thin: find the input folders, run the module commands (`!python -m train.training ...`), zip the outputs.
- A `PROBE` switch runs one epoch on a few images, to check the whole notebook in minutes before the full run.
- Dry-run the notebook locally before uploading: simulate the input folders with the exact zip, run it in probe mode, and
  check the outputs. Never make the user debug a notebook on a GPU quota.
- Fit the work in one session (Kaggle stops at 12 h); run independent jobs in parallel sessions; record the GPU hours.
- Give the user exact instructions: datasets to attach, accelerator, internet on or off, what to download and where to
  extract it.
- When the results come back: compare the code inside the run with the local code, check the configuration and the logs,
  and recompute one logged metric locally from the predictions (`improvement-loop.md`, step 6).
- Do not install heavy tools locally to avoid a GPU run; ask the user first.

## 6. Numerics

- Mixed precision (autocast with float16) speeds up training on GPU; compute the loss in float32. With float16 the
  sigmoid of a logit above about 8.3 rounds to exactly 1 and sums over millions of pixels overflow (maximum 65504).
- Have the network return logits and use the loss on logits (e.g. `BCEWithLogitsLoss`), applying the sigmoid outside the
  network at inference; plain binary cross-entropy on probabilities is not allowed inside CUDA autocast.
- Fix the seeds and use a local random generator in analysis code, so that resamples and random galleries are
  reproducible.
