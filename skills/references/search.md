# Search CLI Reference

Use `kaggle search` to run a unified search across Kaggle competitions,
datasets, notebooks, models, users, and discussions from a single command.

## Prerequisites

- Python 3.11+ with the `kaggle` package installed.
- Kaggle credentials.

## Command Hierarchy

```text
kaggle search "<query>"
```

## `kaggle search`

Searches across Kaggle content types and returns one ranked result list.
Unlike the per-command `-s/--search` flags (for example
`kaggle datasets list --search`), this command searches multiple content types
in a single request and can also find users and discussions.

By default it searches all CLI-supported content types (competition, dataset,
notebook, model, user, discussion, benchmark) — not every backend document type;
types the CLI cannot render usefully (comments, blogs, courses, etc.) are
excluded. Ordering uses the backend's canonical cross-content ranking.

**Usage:**

```bash
kaggle search "<query>" [options]
```

**Options:**

- `query`: Term(s) to search for (required).
- `-t, --type <TYPES>`: Comma-separated content types to restrict to. Valid: `competition`, `dataset`, `notebook`, `model`, `user`, `discussion`, `benchmark`. Omit to search all of these CLI-supported types.
- `-m, --mine`: Restrict the search to your own content.
- `--sort-by <SORT_BY>`: One of `relevance` (default), `hotness`, `votes`, `dateCreated`, `dateUpdated`, `totalComments`, `lastViewed`.
- `--page-size <SIZE>`: Results per page (default 20, max 100).
- `--page-token <TOKEN>`: Page token for paging.
- `-v, --csv`: Print CSV instead of a table.
- `--format <FORMAT>`: `csv`, `table`, or `json`; supports projection, e.g. `--format 'json(type,ref)'`.

**Examples:**

```bash
kaggle search "weather"
kaggle search "diffusion" --type dataset,model
kaggle search "andrew ng" --type user
kaggle search "baseline" --mine --sort-by dateUpdated
kaggle search "titanic" --format json
```

**Purpose:** Discover content across the whole platform when you don't know the
content type in advance, or when you want results from several types at once.

## Output

Results are a table with columns `type`, `ref`, `title`, `owner`, and `votes`.
The `ref` value is reusable with other commands: `owner/slug` for datasets,
notebooks, and models; the bare slug for competitions and users. For example,
a `dataset` result's `ref` can be passed to `kaggle datasets download`, and a
`competition` result's `ref` to `kaggle competitions files`.
