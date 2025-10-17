# Work Location Tracker

A command-line tool for tracking daily work location designations with an intuitive flag-based interface.

## TLDR - Quick Setup

```bash
# Set data directory (optional but recommended)
export SEAT_TRACKER_DATA_DIR="$HOME/.seattracker"

# Run the tracker
python3 seat-tracker.py                 # View calendar
python3 seat-tracker.py --home          # Set today as work from home
python3 seat-tracker.py --lab           # Set today as work from lab
python3 seat-tracker.py --stats 30      # View 30-day statistics
```

## Features

- **Simple flag-based CLI** - Use intuitive flags like `--home`, `--lab`, `--vacation`
- **Colored calendar display** - Color-coded designations with week numbers for easy scanning
- **Interactive mode** - Full-featured interactive shell for bulk updates
- **Statistics and reporting** - Track patterns over 30, 90, and 365-day periods
- **Data validation** - Verify data integrity with built-in validation
- **Human-readable storage** - Plain text files with full designation names
- **Multi-year support** - Automatic yearly rollover with seamless cross-year queries
- **Auto-populate weekends** - Automatically adds weekend entries when setting weekday dates

## Location Designations

| Short | Full Name | Description         | Flag         |
|-------|-----------|---------------------|--------------|
| **H** | HOME      | Work From Home      | `--home`     |
| **L** | LAB       | Work From Lab       | `--lab`      |
| **T** | TRAVEL    | Work Travel         | `--travel`   |
| **W** | WEEKEND   | Weekend             | `--weekend`  |
| **V** | VACATION  | Vacation            | `--vacation` |
| **X** | HOLIDAY   | Holiday             | `--holiday`  |
| **O** | OTHER     | Other               | `--other`    |

## Installation

No external dependencies required - uses Python 3.7+ standard library only.

```bash
chmod +x seat-tracker.py
```

## Quick Start

### View Current Calendar (Default)

```bash
python3 seat-tracker.py                      # Show current month calendar (default)
python3 seat-tracker.py --calendar           # Same as above
python3 seat-tracker.py --calendar 2025      # Full year (all 12 months)
python3 seat-tracker.py --calendar 2025-11   # Specific month
```

### Set Today's Location

```bash
python3 seat-tracker.py --home       # Work from home today
python3 seat-tracker.py --lab        # Work from lab today
python3 seat-tracker.py --vacation   # On vacation today
```

### Set Specific Date

```bash
python3 seat-tracker.py --home 2025-10-15
python3 seat-tracker.py --vacation 2025-12-25
python3 seat-tracker.py --travel 2025-11-05
```

### View Calendar

```bash
python3 seat-tracker.py --calendar           # Current month
python3 seat-tracker.py --calendar 2025      # Full year (all 12 months)
python3 seat-tracker.py --calendar 2025-11   # Specific month
python3 seat-tracker.py --calendar --no-color # Plain text (no colors)
```

Example output (with colors enabled by default):
```
       October 2025

    Mo Tu We Th Fr Sa Su
--------------------------
W40        1  2  3  4  5
           H

W41  6  7  8  9 10 11 12
              L  L  L  H

W42 13 14 15 16 17 18 19
     H  L  L  V  T  V

W43 20 21 22 23 24 25 26
     H  L  H        W  W

Location Designations:
  H - Work From Home (green)
  L - Work From Lab (blue)
  T - Work Travel (magenta)
  W - Weekend (dark gray)
  V - Vacation (yellow)
  X - Holiday (red)
  O - Other (white)
Week numbers shown in cyan, current day in bold
```

### View Statistics

```bash
python3 seat-tracker.py --stats          # Last 30 days (default)
python3 seat-tracker.py --stats 30       # Last 30 days
python3 seat-tracker.py --stats 90       # Last 90 days
python3 seat-tracker.py --stats 365      # Last 365 days
python3 seat-tracker.py --stats all      # All periods (30/90/365)
python3 seat-tracker.py --stats 7        # Any number of days
```

### View Statistics with Calendar

Combine statistics with visual calendar views to see your data:

```bash
python3 seat-tracker.py --stats 30 --with-calendar    # 30 days with calendar
python3 seat-tracker.py --stats 90 --with-calendar    # 90 days with calendar
python3 seat-tracker.py --stats 7 --with-calendar     # 7 days with calendar
python3 seat-tracker.py --stats all --with-calendar   # All periods with calendars
```

This shows:
- Statistics report (counts, percentages, breakdowns)
- Calendar view for the exact date range
- Visual representation of all designations in the period

### Other Commands

```bash
python3 seat-tracker.py --get                 # Get today's designation
python3 seat-tracker.py --get 2025-10-15      # Get specific date
python3 seat-tracker.py --work-summary        # Work days summary (30 days)
python3 seat-tracker.py --work-summary 90     # Work days summary (90 days)
python3 seat-tracker.py --work-summary 30 --with-calendar # Work summary with calendar
python3 seat-tracker.py --validate            # Validate current year data
python3 seat-tracker.py --validate 2024       # Validate specific year
```

## Interactive Mode

Start interactive mode for bulk updates and exploration:

```bash
python3 seat-tracker.py --interactive
# or short form:
python3 seat-tracker.py --i
```

Interactive commands:
```
tracker> calendar                    # Show current month
tracker> calendar 2025               # Show full year
tracker> calendar 2025-10            # Show specific month
tracker> set 2025-10-15 HOME         # Set designation (full name)
tracker> set 2025-10-16 L            # Set designation (short code)
tracker> get 2025-10-15              # Get designation
tracker> stats 30                    # Show 30-day statistics
tracker> stats all                   # Show all periods
tracker> work-summary                # Work days summary
tracker> validate                    # Validate data
tracker> help                        # Show help
tracker> quit                        # Exit
```

## Data Format

Data is stored in `data/YEAR.log` files with full designation names:

```
# Work Location Log for 2025
# Format: YYYY-MM-DD|WXX|DESIGNATION
# Week ends on Sunday, new week starts on Monday
# Valid designations: HOME(H), LAB(L), TRAVEL(T), WEEKEND(W), VACATION(V), HOLIDAY(X), OTHER(O)

2025-10-14|W42|HOME
2025-10-15|W42|LAB
2025-10-16|W42|VACATION
2025-10-17|W42|TRAVEL
```

Each line contains:
- Date in ISO format (YYYY-MM-DD)
- Week number (ISO week, WXX)
- Full designation name (e.g., HOME, LAB, VACATION)

## Short Aliases

Most commands support short aliases:

```bash
--home    →  --h
--lab     →  --l
--travel  →  --t
--vacation→  --v
--holiday →  --x
--weekend →  --w
--other   →  --o

--calendar     →  --cal, --c
--stats        →  --s
--with-calendar→  --wc
--work-summary →  --ws
--get          →  --g
--validate     →  --val
--interactive  →  --i
--no-color     →  --nocolor
```

## Automatic Features

### Auto-Populate Weekends

When you set a designation for any weekday, the tracker automatically adds Saturday and Sunday of that week as WEEKEND entries (if they don't already exist). This saves you from manually tracking weekends.

Example:
```bash
# Set Wednesday
python3 seat-tracker.py --home 2025-10-15

# Saturday and Sunday are automatically marked as WEEKEND
# Unless you've already set them to something else (like VACATION)
```

### Untracked Dates

If no designation is explicitly set for a date:
- The calendar shows **empty spaces** (no designation letter)
- The `--get` command returns "**No designation set**"
- Statistics only count **actual tracked entries**

This keeps your data clean and shows exactly what you've tracked without assumptions.

## Directory Structure

```
seat-tracker/
├── src/                        # Source code
│   ├── __init__.py
│   ├── cli.py                  # Flag-based CLI
│   ├── location_tracker.py    # Core data model
│   ├── calendar_view.py       # Compact calendar display
│   ├── statistics.py          # Statistics and reporting
│   └── interactive.py         # Interactive mode
├── data/                       # Data files (YEAR.log)
├── tests/                      # Test scripts
│   └── test_tracker.sh        # Integration test script
├── conf/                       # Configuration files
├── seat-tracker.py             # Main entry point
├── README.md
└── USAGE.md                    # Quick start guide
```

## Examples

### Daily Workflow

```bash
# Morning: Check current month (default behavior)
python3 seat-tracker.py

# Set today's location
python3 seat-tracker.py --home

# View calendar again to see the update
python3 seat-tracker.py
```

### Weekly Planning

```bash
# Plan next week
python3 seat-tracker.py --interactive

tracker> set 2025-10-20 HOME
tracker> set 2025-10-21 LAB
tracker> set 2025-10-22 LAB
tracker> set 2025-10-23 LAB
tracker> set 2025-10-24 HOME
tracker> calendar
tracker> quit
```

### Monthly Review

```bash
# Review last month's work patterns
python3 seat-tracker.py --stats 30
python3 seat-tracker.py --work-summary 30

# See statistics with visual calendar
python3 seat-tracker.py --stats 30 --with-calendar
```

### Batch Updates

Use interactive mode for efficient bulk updates:
```bash
python3 seat-tracker.py --interactive

tracker> set 2025-12-24 VACATION
tracker> set 2025-12-25 HOLIDAY
tracker> set 2025-12-26 VACATION
tracker> set 2025-12-27 VACATION
tracker> calendar 2025-12
```

## Data Management

### Custom Data Directory

By default, data files are stored in the `data/` subdirectory. You can customize this location using the `SEAT_TRACKER_DATA_DIR` environment variable:

```bash
# Set custom data directory
export SEAT_TRACKER_DATA_DIR="$HOME/.seattracker"

# Now all commands use the custom location
python3 seat-tracker.py --home
python3 seat-tracker.py --calendar

# Or use inline for a single command
SEAT_TRACKER_DATA_DIR="$HOME/.seattracker" python3 seat-tracker.py --calendar
```

The custom directory will be created automatically if it doesn't exist. You can also use the `--data-dir` flag for one-off custom locations:

```bash
python3 seat-tracker.py --data-dir /path/to/data --calendar
```

Priority order:
1. `--data-dir` command-line flag (highest priority)
2. `SEAT_TRACKER_DATA_DIR` environment variable
3. `./data` relative to package (default)

### Multi-Year Support

The tracker automatically handles multiple years:

- **Automatic file creation**: When you set a designation for a new year, the corresponding `YEAR.log` file is automatically created
- **Cross-year statistics**: Statistics commands (like `--stats 365`) automatically span multiple years
- **Historical data**: View any past year's calendar
- **Per-year validation**: Validate any year with `--validate YYYY`

Examples:
```bash
# Set designation in 2024
python3 seat-tracker.py --home 2024-12-31

# View full year 2024
python3 seat-tracker.py --calendar 2024

# View specific month in 2024
python3 seat-tracker.py --calendar 2024-12

# Get statistics spanning 2024-2025
python3 seat-tracker.py --stats 365

# Validate 2024 data
python3 seat-tracker.py --validate 2024
```

### Color Output

By default, the calendar uses colors to improve readability:
- **Week numbers**: Cyan
- **HOME**: Green
- **LAB**: Blue
- **TRAVEL**: Magenta
- **WEEKEND**: Dark gray
- **VACATION**: Yellow
- **HOLIDAY**: Red
- **OTHER**: White
- **Current day**: Bold

To disable colors (for piping or non-color terminals):
```bash
python3 seat-tracker.py --calendar --no-color
python3 seat-tracker.py --interactive --nocolor
```

### Validation

Always validate after manual edits:
```bash
python3 seat-tracker.py --validate          # Current year
python3 seat-tracker.py --validate 2024     # Specific year
```

### Manual Editing

You can directly edit `.log` files in the `data/` directory. The format is simple and human-readable. Use full designation names (HOME, LAB, VACATION, etc.) in the file.

### Backup

Simply copy the `data/` directory to back up all your location history.

## Calendar View with Statistics

The `--with-calendar` flag enhances statistics reports by showing visual calendar views of the exact date range being analyzed. This helps you see patterns at a glance:

### Example Output

```bash
python3 seat-tracker.py --stats 30 --with-calendar
```

Shows:
1. **Statistics Report**: Numerical breakdown with counts and percentages
2. **Date Range Header**: Exact date range and total days covered
3. **Calendar View**: Visual representation of all months in the period
4. **Legend**: Color-coded designation guide

### Use Cases

**Weekly Review**:
```bash
python3 seat-tracker.py --stats 7 --with-calendar
```
See last week's work pattern with a compact one-month calendar.

**Monthly Analysis**:
```bash
python3 seat-tracker.py --stats 30 --with-calendar
```
View the last 30 days with calendars showing 1-2 months.

**Quarterly Review**:
```bash
python3 seat-tracker.py --stats 90 --with-calendar
```
See 90 days across 3-4 months with full calendar views.

**Annual Review**:
```bash
python3 seat-tracker.py --stats 365 --with-calendar
```
Full year of data with all 12 months displayed.

**Compare All Periods**:
```bash
python3 seat-tracker.py --stats all --with-calendar
```
Shows 30, 90, and 365-day statistics, each with their respective calendar views.

### Benefits

- **Visual context** for numerical statistics
- **Spot patterns** across weeks and months
- **Identify gaps** in your data easily
- **Cross-reference** numbers with calendar view
- **Better understanding** of work location trends

### Works with Work Summary Too

The `--with-calendar` flag also works with `--work-summary`:

```bash
python3 seat-tracker.py --work-summary 30 --with-calendar
python3 seat-tracker.py --ws 90 --wc  # Using short aliases
```

This provides visual context for work days analysis, showing the calendar alongside the work/non-work day breakdown.

## Tips

1. **Use flags for daily updates** - Quick and intuitive: `--home`, `--lab`, `--vacation`
2. **Use interactive mode for planning** - Set multiple dates efficiently
3. **Check your patterns** - Run `--stats` monthly to understand your work patterns
4. **Visualize with calendars** - Add `--with-calendar` to statistics for visual context
5. **Short codes work everywhere** - Use H, L, T, V, X, W, O in interactive mode
6. **Calendar shows everything** - Colored single-letter codes make patterns instantly visible
7. **Weekends auto-populate** - Just set weekdays, weekends are added automatically
8. **Full year view** - Use `--cal 2025` to see the entire year at once
9. **Colors improve readability** - Use `--no-color` only when needed for piping

## Testing

Run the integration test script to verify the installation:

```bash
./tests/test_tracker.sh
```

The test script exercises the main functionality:
- Setting designations for different dates
- Getting designations for specific dates
- Displaying the calendar
- Validating data integrity
- Viewing statistics

## Acknowledgements

This project was developed with assistance from
[Claude](https://docs.claude.com).

## License

MIT License
