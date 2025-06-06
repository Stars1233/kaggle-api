# Kernels Commands

Commands for interacting with Kaggle Kernels (notebooks and scripts).

## `kaggle kernels list`

Lists available kernels.

**Usage:**

```bash
kaggle kernels list [options]
```

**Options:**

*   `-m, --mine`: Display only your kernels.
*   `-p, --page <PAGE>`: Page number for results (default: 1).
*   `--page-size <SIZE>`: Number of items per page (default: 20).
*   `-s, --search <SEARCH_TERM>`: Search term.
*   `-v, --csv`: Print results in CSV format.
*   `--parent <PARENT_KERNEL>`: Filter by parent kernel (format: `owner/kernel-slug`).
*   `--competition <COMPETITION_SLUG>`: Filter by competition.
*   `--dataset <DATASET_SLUG>`: Filter by dataset (format: `owner/dataset-slug`).
*   `--user <USER>`: Filter by a specific user.
*   `--language <LANGUAGE>`: Filter by language (`all`, `python`, `r`, `sqlite`, `julia`).
*   `--kernel-type <TYPE>`: Filter by kernel type (`all`, `script`, `notebook`).
*   `--output-type <TYPE>`: Filter by output type (`all`, `visualizations`, `data`).
*   `--sort-by <SORT_BY>`: Sort results (`hotness`, `commentCount`, `dateCreated`, `dateRun`, `relevance`, `scoreAscending`, `scoreDescending`, `viewCount`, `voteCount`). Default: `hotness`.

**Examples:**

1.  List your own kernels containing "Exercise" in the title, page 2, 5 items per page, in CSV format, sorted by run date:

    ```bash
    kaggle kernels list -m -s Exercise --page-size 5 -p 2 -v --sort-by dateRun
    ```

2.  List kernels that are children of `$KAGGLE_DEVELOPER/exercise-lists` (replace `$KAGGLE_DEVELOPER` with your username):

    ```bash
    kaggle kernels list --parent $KAGGLE_DEVELOPER/exercise-lists
    ```

3.  List the first 5 kernels for the "house-prices-advanced-regression-techniques" competition:

    ```bash
    kaggle kernels list --competition house-prices-advanced-regression-techniques --page-size 5
    ```

4.  List the first 5 kernels associated with the dataset `dansbecker/home-data-for-ml-course`:

    ```bash
    kaggle kernels list --dataset dansbecker/home-data-for-ml-course --page-size 5
    ```

5.  List Python notebooks by user `$KAGGLE_DEVELOPER` that output data:

    ```bash
    kaggle kernels list --user $KAGGLE_DEVELOPER --language python --kernel-type notebook --output-type data
    ```

**Purpose:**

This command allows you to find kernels based on various filters like ownership, associated competition/dataset, language, or type.

## `kaggle kernels files`

Lists output files for a specific kernel.

**Usage:**

```bash
kaggle kernels files <KERNEL> [options]
```

**Arguments:**

*   `<KERNEL>`: Kernel URL suffix (format: `owner/kernel-slug`, e.g., `kerneler/sqlite-global-default`).

**Options:**

*   `-v, --csv`: Print results in CSV format.
*   `--page-token <PAGE_TOKEN>`: Page token for results paging.
*   `--page-size <PAGE_SIZE>`: Number of items to show on a page (default: 20, max: 200).

**Example:**

List the first output file for the kernel `kerneler/sqlite-global-default` in CSV format:

```bash
kaggle kernels files kerneler/sqlite-global-default -v --page-size=1
```

**Purpose:**

Use this command to view the files generated by a kernel run.

## `kaggle kernels init`

Initializes a metadata file (`kernel-metadata.json`) for a new or existing kernel.

**Usage:**

```bash
kaggle kernels init -p <FOLDER_PATH>
```

**Options:**

*   `-p, --path <FOLDER_PATH>`: The path to the folder where the `kernel-metadata.json` file will be created (defaults to the current directory).

**Example:**

Initialize a kernel metadata file in the `tests/kernel` folder:

```bash
kaggle kernels init -p tests/kernel
```

**Purpose:**

This command creates a template `kernel-metadata.json` file. You need to edit this file with details like the kernel's title, ID (slug), language, kernel type, and data sources before pushing it to Kaggle.

## `kaggle kernels push`

Pushes new code/notebook and metadata to a kernel, then runs the kernel.

**Usage:**

```bash
kaggle kernels push -p <FOLDER_PATH> [options]
```

**Options:**

*   `-p, --path <FOLDER_PATH>`: Path to the folder containing the kernel file (e.g., `.ipynb`, `.Rmd`, `.py`) and the `kernel-metadata.json` file (defaults to the current directory).
*   `-t, --timeout <SECONDS>`: Maximum run time in seconds.

**Example:**

Push the kernel from the `tests/kernel` folder (assuming it contains the kernel file and `kernel-metadata.json`):

```bash
kaggle kernels push -p tests/kernel
```

**Purpose:**

This command uploads your local kernel file and its metadata to Kaggle. If the kernel specified in the metadata exists under your account, it will be updated. Otherwise, a new kernel will be created. After uploading, Kaggle will attempt to run the kernel.

## `kaggle kernels pull`

Pulls down the code/notebook and metadata for a kernel.

**Usage:**

```bash
kaggle kernels pull <KERNEL> [options]
```

**Arguments:**

*   `<KERNEL>`: Kernel URL suffix (format: `owner/kernel-slug`, e.g., `$KAGGLE_DEVELOPER/exercise-as-with`).

**Options:**

*   `-p, --path <PATH>`: Folder to download files to (defaults to current directory).
*   `-w, --wp`: Download files to the current working path.
*   `-m, --metadata`: Generate a `kernel-metadata.json` file along with the kernel code.

**Examples:**

1.  Pull the kernel `$KAGGLE_DEVELOPER/exercise-as-with` and its metadata into the `tests/kernel` folder:

    ```bash
    kaggle kernels pull -p tests/kernel $KAGGLE_DEVELOPER/exercise-as-with -m
    ```

2.  Pull the kernel `$KAGGLE_DEVELOPER/exercise-as-with` into the current working directory:

    ```bash
    kaggle kernels pull --wp $KAGGLE_DEVELOPER/exercise-as-with
    ```

**Purpose:**

This command allows you to download the source code and optionally the metadata of a kernel from Kaggle to your local machine.

## `kaggle kernels output`

Gets the data output from the latest run of a kernel.

**Usage:**

```bash
kaggle kernels output <KERNEL> [options]
```

**Arguments:**

*   `<KERNEL>`: Kernel URL suffix (e.g., `kerneler/using-google-bird-vocalization-model`).

**Options:**

*   `-p, --path <PATH>`: Folder to download output files to (defaults to current directory).
*   `-w, --wp`: Download files to the current working path.
*   `-o, --force`: Force download, overwriting existing files.
*   `-q, --quiet`: Suppress verbose output.

**Example:**

Download the output of the kernel `kerneler/using-google-bird-vocalization-model`, forcing overwrite:

```bash
kaggle kernels output kerneler/sqlite-global-default -o
```

**Purpose:**

Use this command to retrieve the files generated by a kernel run, such as submission files, processed data, or visualizations.

## `kaggle kernels status`

Displays the status of the latest run of a kernel.

**Usage:**

```bash
kaggle kernels status <KERNEL>
```

**Arguments:**

*   `<KERNEL>`: Kernel URL suffix (e.g., `kerneler/sqlite-global-default`).

**Example:**

Get the status of the kernel `kerneler/sqlite-global-default`:

```bash
kaggle kernels status kerneler/sqlite-global-default
```

**Purpose:**

This command tells you whether the latest run of your kernel is still running, completed successfully, or failed.

## `kaggle kernels delete`

Deletes a kernel from Kaggle.

**Usage:**

```bash
kaggle kernels delete <KERNEL> [options]
```

**Arguments:**

*   `<KERNEL>`: Kernel URL suffix (format: `owner/kernel-slug`, e.g., `$KAGGLE_DEVELOPER/exercise-delete`).

**Options:**

*   `-y, --yes`: Automatically confirm deletion without prompting.

**Example:**

Delete the kernel `$KAGGLE_DEVELOPER/exercise-delete` and automatically confirm:

```bash
kaggle kernels delete $KAGGLE_DEVELOPER/exercise-delete --yes
```

**Purpose:**

This command permanently removes one of your kernels from Kaggle. Use with caution.
