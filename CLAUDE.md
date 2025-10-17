# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python-based CLI tool for tracking daily work location designations. Users can mark days as HOME, LAB, TRAVEL, WEEKEND, VACATION, HOLIDAY, or OTHER, and view them in a colored calendar with statistics.

## Core Architecture

The project follows a modular architecture with clear separation of concerns:

- **location_tracker.py** - Core data model and storage
  - `LocationDesignation` enum defines all valid designations (H/L/T/W/V/X/O)
  - `LocationTracker` class handles all data persistence and retrieval
  - Data stored in year-based log files (`data/YEAR.log`)
  - Auto-populates weekends when setting weekday designations
  - Supports custom data directories via `SEAT_TRACKER_DATA_DIR` env var or `--data-dir` flag

- **calendar_view.py** - Visual calendar rendering
  - `CalendarView` class generates colored month/year calendars
  - Uses ANSI color codes (can be disabled with `--no-color`)
  - Supports single month, full year, and date range views
  - Shows week numbers (ISO week format) and highlights current day

- **statistics.py** - Statistics and reporting
  - `LocationStatistics` class generates reports for various time periods
  - Supports 30/90/365-day reports and arbitrary date ranges
  - Only counts actual data entries, not defaults
  - Can combine with calendar views using `--with-calendar`

- **interactive.py** - Interactive shell mode
  - `InteractiveMode` class provides a command-line shell interface
  - Commands: calendar, set, get, stats, work-summary, validate, force, help, quit
  - Includes force mode to skip overwrite confirmations

- **cli.py** - Flag-based command-line interface
  - Main entry point for the application
  - Flag-based design: `--home`, `--lab`, `--stats`, etc.
  - Supports both long and short flags (e.g., `--calendar` or `--c`)
  - Default behavior: shows current month calendar when no args provided

## Data Storage Format

Log files use a pipe-delimited format:
```
YYYY-MM-DD|WXX|DESIGNATION_NAME
```

Example:
```
2025-10-14|W42|HOME
2025-10-15|W42|LAB
```

- One file per year: `data/YEAR.log`
- Files include header comments with format documentation
- Week numbers are ISO week numbers (Monday-Sunday weeks)
- Designations stored as full names (HOME, LAB, etc.), not short codes

## Development Commands

### Running the Application
```bash
# Main entry point
python3 seat-tracker.py

# Common operations
python3 seat-tracker.py --home              # Set today as HOME
python3 seat-tracker.py --lab 2025-10-15    # Set specific date
python3 seat-tracker.py --calendar          # View current month
python3 seat-tracker.py --stats 30          # View 30-day statistics
python3 seat-tracker.py --interactive       # Start interactive mode
```

### Testing
```bash
# Run integration test
./tests/test_tracker.sh

# Manual testing with temp data directory
TEST_DIR=$(mktemp -d)
python3 seat-tracker.py --data-dir "$TEST_DIR" --home
```

### Data Management
```bash
# Custom data directory (priority order):
python3 seat-tracker.py --data-dir /path    # 1. Command-line flag (highest)
export SEAT_TRACKER_DATA_DIR="$HOME/.seattracker"  # 2. Environment variable
# (default: ./data relative to package)      # 3. Default location

# Validation
python3 seat-tracker.py --validate          # Validate current year
python3 seat-tracker.py --validate 2024     # Validate specific year
```

## Key Implementation Details

### No Default Designations
The tracker does not assume default designations for dates without explicit entries:
- Untracked dates show as blank in calendar views
- `get_designation()` returns `None` for dates without data
- Only actual data entries are displayed or counted in statistics

### Auto-Weekend Population
When setting any weekday designation via `set_designation()`, the tracker automatically adds WEEKEND entries for Saturday and Sunday of that week (if not already set). This is controlled by the `auto_weekend` parameter (default: True).

### Week Number Handling
- Uses ISO 8601 week numbering via `date.isocalendar()[1]`
- Weeks start on Monday, end on Sunday
- Week numbers are validated during data validation
- Each log entry includes the week number for the date

### Color Support
- ANSI color codes defined in `CalendarView` class
- Color mappings: HOME=green, LAB=blue, TRAVEL=magenta, WEEKEND=gray, VACATION=yellow, HOLIDAY=red, OTHER=white
- Week numbers shown in cyan, current day in bold
- Disable with `--no-color` flag or `use_color=False` parameter

### Multi-Year Support
The tracker seamlessly handles data across multiple years:
- `load_year_data()` loads specific year files on demand
- `get_date_range_data()` handles ranges spanning multiple years
- Statistics commands automatically load multiple year files as needed
- Calendar views can display adjacent months from different years

### Command-Line Parsing
The CLI uses mutually exclusive argument groups:
- Location designation flags: `--home`, `--lab`, `--travel`, etc.
- Action flags: `--calendar`, `--stats`, `--work-summary`, etc.
- Supports both full flags (`--calendar`) and short aliases (`--c`)
- Optional date parameters default to 'TODAY' when not provided

## Important Conventions

- All date handling uses Python's `datetime.date` objects
- Date strings in YYYY-MM-DD format (ISO 8601)
- Designation names stored as uppercase (HOME, not home)
- Short codes are single letters (H, L, T, W, V, X, O)
- Log files are always sorted by date when saved
- Version number maintained in `src/__init__.py`
