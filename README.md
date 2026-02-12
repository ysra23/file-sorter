# File Sorting Script

A Python script that automatically organizes files by extracting titles from content or filenames, optionally renaming them, and generating a detailed report.

## Features

- **Title Extraction**: Automatically extracts titles from:
  - File content (Markdown headers, HTML titles, document titles)
  - Filenames (cleaned and formatted)
- **Flexible Renaming**: Option to rename files based on extracted titles
- **Detailed Reports**: Generates comprehensive reports showing all processing details
- **Safe Processing**: Copies files to new location (doesn't modify originals)
- **Smart Conflict Resolution**: Handles duplicate filenames automatically

## Installation

No external dependencies required! Uses only Python standard library.

```bash
# Simply download the script
# Requires Python 3.6+
```

## Usage

### Basic Usage

1. **Configure the script** by editing these variables at the top:

```python
RENAME_FILES = False          # Set to True to rename files
SOURCE_DIRECTORY = "./files_to_sort"  # Your input folder
OUTPUT_DIRECTORY = "./sorted_files"   # Where sorted files go
REPORT_PATH = "./file_sorting_report.txt"  # Report location
```

2. **Run the script**:

```bash
python file_sorter.py
```

### Example Workflow

```bash
# 1. Create a directory with files to sort
mkdir files_to_sort
# Add your files to this directory

# 2. Run the script
python file_sorter.py

# 3. Check the results
cat file_sorting_report.txt
ls sorted_files/
```

## How It Works

### Title Extraction

The script tries to extract titles in this order:

1. **From Content** (for text files):
   - Markdown H1 headers (`# Title`)
   - `Title: ` prefix
   - HTML `<title>` tags
   - HTML `<h1>` tags
   - Underlined titles (with `===`)
   - First non-empty line (if it looks like a title)

2. **From Filename** (fallback):
   - Removes underscores, hyphens, dots
   - Removes dates (YYYY-MM-DD format)
   - Removes leading/trailing numbers
   - Converts to Title Case

### File Renaming

When `RENAME_FILES = True`:
- Uses extracted title as new filename
- Removes invalid characters
- Limits filename length to 200 characters
- Preserves file extensions
- Handles duplicates by adding `_1`, `_2`, etc.

## Report Format

The generated report includes:

```
📁 SORTED FILES REPORT
==================================================
Generated on: 2024-01-15 14:30:00

SUMMARY
--------------------------------------------------
Total Files:              25
Titles from Content:      18
Titles from Filename:     7
Files Renamed:            Yes
Source Directory:         ./files_to_sort
Output Directory:         ./sorted_files

DETAILED FILE LIST
--------------------------------------------------
Title                     Filename              Source
--------------------------------------------------
My Important Document     my_important_doc.txt  content
Project Proposal          project_proposal.md   content
...
```

## Supported File Types

- **Text files**: `.txt`, `.md`, `.markdown`
- **HTML files**: `.html`, `.htm`
- **Code files**: `.py`, `.js`, `.css`, etc.
- **Any other files**: Title extracted from filename only

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `RENAME_FILES` | `False` | Whether to rename files based on titles |
| `SOURCE_DIRECTORY` | `./files_to_sort` | Directory containing files to process |
| `OUTPUT_DIRECTORY` | `./sorted_files` | Where sorted files will be placed |
| `REPORT_PATH` | `./file_sorting_report.txt` | Path for the report |

## Advanced Usage

### Custom Title Extraction

You can modify the `extract_title_from_content()` method to add custom patterns:

```python
patterns = [
    r'^#\s+(.+)$',  # Markdown H1
    r'^Title:\s*(.+)$',  # Title: prefix
    r'YOUR_CUSTOM_PATTERN',  # Add your pattern here
]
```

### Processing Subdirectories

The script automatically processes all subdirectories in the source folder using `rglob('*')`.

## Troubleshooting

**Files not being renamed?**
- Make sure `RENAME_FILES = True`
- Check that titles are being extracted (see report)

**No titles extracted from content?**
- Script only reads first 1000 characters
- Only works with text-based files
- Check file encoding (uses UTF-8)

**Filename conflicts?**
- Script automatically adds `_1`, `_2` suffixes
- Check output directory for numbered files

## License

Free to use and modify as needed.

## Examples

### Example 1: Organize Research Papers

```python
RENAME_FILES = True
SOURCE_DIRECTORY = "./research_papers"
OUTPUT_DIRECTORY = "./organized_papers"
```

Result: PDFs and documents renamed to their actual titles.

### Example 2: Clean Up Download Folder

```python
RENAME_FILES = True
SOURCE_DIRECTORY = "~/Downloads"
OUTPUT_DIRECTORY = "~/Documents/Organized"
```

Result: Messy download filenames cleaned and organized.

### Example 3: Generate Inventory Without Renaming

```python
RENAME_FILES = False
SOURCE_DIRECTORY = "./project_files"
```

Result: Report showing all file titles without renaming.
