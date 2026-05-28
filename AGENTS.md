# AGENTS.md — Student Dropout Prediction

## Setup

- Virtual env at `env/` (Python 3.14). Activate: `source env/bin/activate`
- Install: `pip install -r requirements.txt`

## Entrypoint

- `python main.py` — runs ETL only, outputs `data/processed/dataset_final_ia.csv`
- `python main.py --train` — ETL + train model, saves `models/modelo_rf.pkl`
- `python main.py --train --no-optimize` — skip RandomizedSearchCV hyperparameter tuning

All commands must run from repo root. Paths resolve relative to `src/config.py` or `src/etl.py` (both use `__file__`-relative `ROOT`).

## Data requirements (ETL will fail without these)

ETL hardcodes two source files in `data/raw/`:
- `ENCUESTA_UPECISTA (200 datos).xlsx` — UPC student survey (Spanish)
- `dataset_internacional.csv` — international academic dataset

Both are gitignored but `.gitkeep` files preserve the `data/raw/` directory. The ETL concatenates both, aligns columns, and writes the unified CSV.

## Architecture

```
main.py          → CLI orchestration (ETL always runs first)
src/etl.py       → Load, clean, merge both datasets
src/train.py     → Random Forest pipeline (OrdinalEncoder + SimpleImputer + RF)
src/predict.py   → Load model dict `{"modelo": ..., "threshold": ...}` and predict
src/config.py    → Shared paths, column lists, model params, grid
src/schemas.py   → Pydantic models (fastapi stubs)
api/routes.py    → FastAPI stub (not implemented yet)
```

Key detail: the trained model file is a `joblib` dict, not a raw pipeline object — `load_model()` in `predict.py` handles both cases.

## Conventions

- All code, comments, and variable names are in Spanish
- No tests, no linter, no CI, no formatter, no type checker
- No `pyproject.toml` or `setup.py` — dependency management is just `requirements.txt`
- Feature columns (16 total): 10 categorical + 6 numerical (see `src/config.py` for the exact lists)
