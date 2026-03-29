# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the script

```bash
poetry run python plot_emakler.py
```

Or install and use the entry point:

```bash
poetry install
poetry run plot-emakler
```

## Data format

`eMAKLER_portfel_wyceny_historyczne.Csv` is a CP1250-encoded export from mBank eMAKLER (IKE brokerage account). It contains multiple date blocks separated by `Data;Wycena` headers. Each block lists holdings with columns: `Papier;Giełda;Liczba;Blokada;Udział %;Wartość;Waluta`.

Historical exports are archived in year-based directories (`2025-11/`, `2026-03/` etc) alongside the current export at the repo root.

## Architecture

`plot_emakler.py` is a single-file script with no classes:

1. **Parsing** — `parse_block(block)` splits a raw text block into a date and a DataFrame.
2. **Loading** — the file is split on `\nData;Wycena\n` and all blocks are concatenated into `portfolio_df`.
3. **Pivoting** — three pivot tables are derived: `pivot_value_per_unit`, `pivot_quantity`, `pivot_value_total` (with a `Total` column appended).
4. **Plotting** — two charts rendered via matplotlib using explicit `fig, ax = plt.subplots()` so pandas `.plot()` draws into the correct figure rather than creating orphan figures.

Dependencies: `pandas`, `matplotlib` (see `pyproject.toml`).
