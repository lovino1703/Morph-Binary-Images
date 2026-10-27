# Morphological Erosion and Dilation on Binary Images

Group project – Image Processing course.

## Structure
```
src/       source code (morphology.py, io_utils.py)
tests/     unit tests (pytest)
images/    input images
results/   output images / figures for the article
```

## Setup
```bash
# Option A: conda
conda env create -f environment.yml
conda activate morph-binary

# Option B: venv + pip
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run tests
```bash
pytest -q
```

## Git workflow
- `main` is protected by convention: do not push directly.
- Each member works on a branch: `feature/<member>-<task>` (e.g. `feature/m3-erosion`).
- Open a Pull Request, have at least one teammate review, then merge.
- Commit messages: `T0X: short description`.

## Team
| Member | Role |
|---|---|
| M1 | |
| M2 | Repo & environment (T03) |
| M3 | Test images & Otsu binarisation (T08) |
| M4 | Article template (T04) |
