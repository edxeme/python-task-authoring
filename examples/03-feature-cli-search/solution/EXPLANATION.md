# Feature walk-through — `search` subcommand

Spec → red tests → implementation, the same loop used to generate
human-data training trajectories.

## 1. Spec → testable claims

| Spec sentence | Test |
| :--- | :--- |
| prints every note containing *term*, case-insensitively | `test_search_is_case_insensitive` |
| substring semantics | `test_search_matches_substring` |
| no matches → print nothing, exit 0 | `test_search_no_match_returns_empty` |
| empty *term* matches everything | `test_search_empty_term_matches_all` |
| storage order preserved | `test_search_preserves_storage_order` |
| `notes search <term>` parses | `test_parser_accepts_search_with_term` |

## 2. Red

In task state the suite cannot even collect: `search_notes` does not
exist, so `from src.cli import build_parser, search_notes` raises
`ImportError`. That is the clearest possible red — the missing feature is
the missing symbol.

## 3. Implementation choices

- **`casefold()`, not `lower()`** — `casefold` is the Unicode-correct
  case-insensitive comparison (e.g. German `ß` → `ss`); `lower()` misses it.
- **Pure helper** — `search_notes` touches no globals and no I/O, mirroring
  the existing `add_note` / `list_notes` pattern; `main` stays a thin
  dispatcher. This keeps the function trivially unit-testable and matches
  how the module docstring says new subcommands should be added.
- **Wiring** — the subparser registers `term` as a required positional, and
  `main` reuses the same print-one-per-line loop as `list`, so output
  formatting stays consistent across commands.
- **Empty term** — with `needle = ""` the membership test `"" in s` is
  always `True`, so the spec's "empty term matches everything" falls out
  of the implementation for free. No special case.

## 4. Green

After the patch all six tests pass, and the pre-existing behavior is
untouched (the patch only adds — it never edits an existing line).
