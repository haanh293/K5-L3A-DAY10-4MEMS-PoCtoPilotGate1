# Repository Guidelines

## Project Structure & Module Organization

`lab10/` contains the Python simulation, command-line workflows, gates, and monitors. Most framework files are locked; contributor code is limited primarily to `lab10/guards.py` and `lab10/monitors.py`. Operational and acceptance settings live in `config/`, while deterministic fixtures are in `data/`. Public `unittest` coverage is under `tests/`. Complete the team worksheets in `templates/`, record incident work in `incidents/`, and use `submission/` only for the final collected deliverables. Consult `README.md` for the lab flow and `docs/guide.md` for troubleshooting.

## Build, Test, and Development Commands

This project uses the Python standard library and requires no build step.

- `python3 -m unittest discover -s tests -v`: run all public tests (use `python` on Windows if needed).
- `python3 -m lab10.eval --suite base --stage base --note "baseline"`: run and record a baseline evaluation.
- `python3 -m lab10.trace --suite base --ticket T-002 --seed 55`: inspect one deterministic ticket execution.
- `python3 -m lab10.grade --incident S1`: validate the three required stages for an assigned incident.
- `python3 -m lab10.check_submission --collect`: assemble and verify final submission artifacts.

Run commands from the repository root so Python can import `lab10`.

## Coding Style & Naming Conventions

Follow the existing Python style: four-space indentation, standard-library imports before local imports, `snake_case` for functions and variables, `UPPER_CASE` for constants, and short module docstrings. Add type hints where they clarify gate or monitor inputs and outputs. Keep JSON keys consistent with the surrounding configuration. There is no configured formatter or linter; preserve the compact style already present and avoid unrelated reformatting.

## Testing Guidelines

Tests use `unittest`; name new files `test_*.py`, classes `Test*`, and methods `test_*`. Keep cases deterministic by using the repository's fixed suites and seeds. Before submitting, run the public suite and the incident grader. Existing baseline behavior must not regress.

## Commit & Pull Request Guidelines

History currently contains only `Initial commit`, so no established convention exists. Use concise, imperative subjects such as `Add refund approval guard`. Keep commits focused and never commit generated `runs/` output. Pull requests should summarize the changed gate/configuration, identify the incident and validation commands, link any issue, and include relevant before/after metrics or trace excerpts.

## Protected Artifacts & Secrets

Do not edit locked framework files or checkpoint snapshots such as `lab10/guards_round1.py`, `config/operating_gates.round1.json`, and `config/round1.lock`. Never commit API keys, tokens, or customer data; follow `RULES.md` and `SUBMISSION.md` before collection.
