# evidence-driven-ml

A [Claude Code](https://claude.com/claude-code) skill for running a machine-learning or deep-learning project together with
Claude, one reviewed step at a time and with decisions backed by measurements.

It was distilled from a real project (segmentation and counting of fluorescent cell nuclei) and captures the way of
working that made it reliable:

- **Understand before planning.** In-depth reading of the dataset documentation, the annotation protocol and the
  literature, then an EDA aimed at extracting every insight that changes a decision. Metrics, splits, preprocessing,
  loss and baselines are chosen from what these phases found.
- **One step at a time.** Claude proposes and explains each step; the user chooses whether to write the code with
  guidance or to delegate it; nothing moves on without review.
- **Rules before results.** Every change is compared with the adopted pipeline on the same data, with paired-bootstrap
  intervals, against a rule written before the run. The test set is evaluated once.
- **An error-driven improvement loop.** Diagnose the errors, compute the ceiling of each fix, propose candidates with
  their cost, let the user choose, run (locally or on Kaggle/Colab), verify, evaluate, let the user judge, record.
- **Readable project documents.** `PLAN.md`, `DECISIONS.md`, `HYPERPARAMETERS.md`, `PROPOSALS.md` and `GUIDE.md`
  instead of one ever-growing plan.
- **Clean delivery.** Simple, analytical final notebooks, a clear README, and minimal, consistent presentation slides.

## How it works

The project goes through seven phases; the improvement loop (E) repeats until the results stop paying off.

```mermaid
flowchart LR
    A["A · Understand<br/>docs, literature,<br/>kickoff interview"] --> B["B · EDA<br/>insights → decisions"]
    B --> C["C · Plan<br/>metrics, data roles,<br/>decision rule"]
    C --> D["D · Baselines<br/>and first model"]
    D --> E["E · Improvement loop<br/>(repeated)"]
    E --> E
    E --> F["F · Freeze and test<br/>test set used once"]
    F --> G["G · Delivery<br/>notebooks, README,<br/>slides"]
```

Each pass of the improvement loop starts from the measured errors and stops three times for the user (in green):

```mermaid
flowchart TD
    S1["1 · Diagnose<br/>error types and oracle ceilings"] --> S2["2 · Hypothesize<br/>cause, and what would refute it"]
    S2 --> S3["3 · Propose<br/>ceiling, expected gain, cost, risk"]
    S3 --> U1(["You choose"])
    U1 --> S4["4 · Fix the protocol<br/>rule written before running"]
    S4 --> S5["5 · Implement or prepare the run<br/>old behaviour as default, probe mode"]
    S5 --> U2(["You run it on Kaggle / Colab<br/>and upload the results"])
    S5 -. "no GPU needed" .-> S6
    U2 --> S6["6 · Verify what came back<br/>same code, same recipe, same metrics"]
    S6 --> S7["7 · Evaluate against the rule<br/>paired bootstrap, every guard metric"]
    S7 --> S8["8 · Report<br/>intervals, verdict, limitations"]
    S8 --> U3(["You judge"])
    U3 --> R["Record in DECISIONS.md<br/>and PROPOSALS.md"]
    R --> S1
    classDef user fill:#1E7A46,color:#ffffff,stroke:#1E7A46
    class U1,U2,U3 user
```

## Install

Copy the folder into your personal skills directory:

```bash
git clone <this repository> ~/.claude/skills/evidence-driven-ml
```

Claude Code loads it automatically in every project. It activates when you start or plan an ML project, explore a
dataset, analyse a model's errors, decide whether to adopt a change, or prepare notebooks and slides; you can also ask
for it by name.

## Contents

```
SKILL.md                         the method in short: roles, lifecycle, improvement loop, rules
references/
  planning.md                    kickoff interview, framing, metrics, decision rule, baselines, steps
  understanding-and-eda.md       documentation and literature, EDA for maximum insight, insights → decisions
  improvement-loop.md            the loop in eight steps, with examples
  decision-rules.md              roles of the data, paired bootstrap, gates, cross-validation, the test set
  engineering.md                 repositories, code organisation, regression checks, Kaggle/Colab runs
  project-docs.md                the five project documents
  presentation.md                final notebooks and README
  slides.md                      the slide style
assets/templates/                PLAN.md, DECISIONS.md, HYPERPARAMETERS.md, PROPOSALS.md, GUIDE.md
scripts/paired_bootstrap.py      paired-bootstrap interval of a metric difference (self-test with no arguments)
evals/                           three test cases in the `claude plugin eval` format
```

## Tests

`evals/` holds three test cases (starting a project, analysing errors, evaluating a variant). The input files of the
second and third case are synthetic and are regenerated with `python evals/make_inputs.py .` from the skill folder. With
Claude Code they run with `claude plugin eval . --allow-tools Write,Edit,Bash --scaffold`, with and without the skill.
These are real, billed model runs.

## Requirements

Python 3 with NumPy for `scripts/paired_bootstrap.py`. Nothing else is installed by the skill.

## License

MIT — see `LICENSE`.
