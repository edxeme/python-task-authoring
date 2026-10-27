# 03 · Small feature — `search` subcommand for the notes CLI

The notes CLI (`src/cli.py`) supports `add` and `list`. Product asks for a
**`search`** subcommand.

## Spec

- `notes search <term>` prints every note containing *term*,
  **case-insensitively**, in storage order, one per line.
- An empty *term* matches everything.
- No matches: print nothing, exit `0`.

## Your task

Implement the feature in `src/cli.py` so the suite in `tests/` passes:

- Add a pure helper `search_notes(notes: list[str], term: str) -> list[str]`
  (same pattern as `add_note` / `list_notes`).
- Wire the `search` subcommand into `build_parser` and `main`.

## Reproduce

```sh
docker build -t pta-03 . && docker run --rm pta-03   # RED: import error
# or locally: python -m pytest tests/ -v
```

## Solution

`solution/` — the golden patch (`solution.patch`) and `EXPLANATION.md`
walking the spec → red tests → implementation loop.
