# Topic 9 — Data Analytics Using Python (Superstore)

A small, modular pipeline that loads the Kaggle **Superstore** dataset, runs
basic analysis with **pandas**, visualizes total sales by region with
**Matplotlib**, and generates a 7-slide **PowerPoint** report.

## Project structure

```
superstore/
├── data/
│   └── superstore.csv          # dataset (UTF-8), already placed for you
├── reports/                    # generated chart + deck land here
├── superstore/                 # the package
│   ├── config.py               # all paths, column names, styling, presenter info
│   ├── environment.py          # detects installed library versions
│   ├── data_loader.py          # encoding-tolerant CSV loading + validation
│   ├── analysis.py             # pure analysis functions + AnalysisResult
│   ├── visualization.py        # Matplotlib bar-chart rendering
│   ├── reporting.py            # terminal report formatting
│   ├── slides.py               # slide content (what goes on each slide)
│   ├── deck.py                 # python-pptx rendering (how slides are drawn)
│   └── pipeline.py             # orchestrates the whole workflow
├── tests/                      # unit tests for analysis + loading
├── main.py                     # command-line entry point
└── requirements.txt
```

Each module has a single responsibility, and no file exceeds 300 lines.

## Setup

```bash
# From this folder
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Verify the install (Activity Step 1):

```bash
python -c "import pandas as pd, matplotlib; \
print('Pandas version:', pd.__version__); \
print('Matplotlib version:', matplotlib.__version__)"
```

## Run

```bash
python main.py                     # analysis + chart  (Steps 2-7)
python main.py --deck              # also build the PowerPoint report (Step 8)
python main.py --show              # also display the chart interactively
python main.py --deck --name "Pariss Youngblood" \
  --course "Intro to Programming" --instructor "Prof. Smith"
```

Outputs are written to `reports/`:

- `sales_by_region.png` — the "Total Sales by Region" bar chart
- `topic9_report.pptx` — the 7-slide report (with `--deck`)

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## How it maps to the Activity Guide

| Activity step | Where it happens |
| --- | --- |
| 1. Install & verify libraries | `requirements.txt`, `environment.py` |
| 2. Load the dataset | `data_loader.py` |
| 3. Explore (head/info/describe/nulls) | `reporting.py` |
| 4. Basic analysis (totals, averages) | `analysis.py` |
| 5. Visualization (sales by region) | `visualization.py` |
| 6. Run & evaluate | `python main.py` |
| 7. Report out (7-slide deck) | `slides.py`, `deck.py` |

The dataset ships in Windows-1252 encoding, so `data_loader.py` tries UTF-8
first and falls back automatically — no manual re-saving required.
