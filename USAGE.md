# Quick Start Guide

## TL;DR

```bash
# View current month calendar (default behavior)
python3 seat-tracker.py

# Set today's location
python3 seat-tracker.py --home
python3 seat-tracker.py --lab
python3 seat-tracker.py --vacation

# View calendar (compact, single-letter codes)
python3 seat-tracker.py --calendar

# Get stats
python3 seat-tracker.py --stats
```

## Installation

```bash
cd seat-tracker
chmod +x seat-tracker.py
```

## Quick Examples

### Daily Updates (Most Common)

```bash
# Working from home today
python3 seat-tracker.py --home

# Working from lab today
python3 seat-tracker.py --lab

# On vacation today
python3 seat-tracker.py --vacation
```

### Set Specific Date

```bash
python3 seat-tracker.py --home 2025-10-15
python3 seat-tracker.py --vacation 2025-12-25
```

### View Calendar (Colored with Week Numbers)

```bash
python3 seat-tracker.py --calendar           # Current month
python3 seat-tracker.py --calendar 2025      # Full year
python3 seat-tracker.py --calendar 2025-11   # Specific month
python3 seat-tracker.py --calendar --no-color # Plain text
```

### View Statistics with Calendar

Combine statistics with visual calendar views:

```bash
python3 seat-tracker.py --stats 30 --with-calendar    # 30-day stats with calendar
python3 seat-tracker.py --stats 90 --with-calendar    # 90-day stats with calendar
python3 seat-tracker.py --stats 7 --with-calendar     # 7-day stats with calendar
python3 seat-tracker.py --stats all --with-calendar   # All periods with calendars
```

Example output shows:
- Statistics report (counts, percentages)
- Date range covered
- Calendar view of all months in the period
- Visual representation of your work patterns

This is especially useful for:
- **Weekly reviews** (7 days)
- **Monthly analysis** (30 days)
- **Quarterly planning** (90 days)
- **Annual summaries** (365 days)

Output shows colored single-letter codes with ISO week numbers:
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
```

Where:
- **H** = Home (green)
- **L** = Lab (blue)
- **T** = Travel (magenta)
- **V** = Vacation (yellow)
- **X** = Holiday (red)
- **W** = Weekend (dark gray)
- **O** = Other (white)
- **WXX** = ISO week number (cyan)
- Current day shown in **bold**

### Interactive Mode

For bulk updates, use interactive mode:

```bash
python3 seat-tracker.py --interactive
```

Then use commands like:
```
tracker> calendar                # Current month
tracker> calendar 2025           # Full year
tracker> calendar 2025-10        # Specific month
tracker> set 2025-10-15 HOME
tracker> set 2025-10-16 L        # Short codes work!
tracker> get 2025-10-15
tracker> stats 30
tracker> stats all               # All periods
tracker> quit
```

## Location Designations

| Code | Full Name | Flag         | When to Use              |
|------|-----------|--------------|--------------------------|
| H    | HOME      | `--home`     | Working from home        |
| L    | LAB       | `--lab`      | Working from lab/office  |
| T    | TRAVEL    | `--travel`   | Work travel              |
| V    | VACATION  | `--vacation` | Vacation days            |
| X    | HOLIDAY   | `--holiday`  | Public holidays          |
| W    | WEEKEND   | `--weekend`  | Weekends                 |
| O    | OTHER     | `--other`    | Other situations         |

## Common Workflows

### Morning Routine

```bash
# Check current month (default)
python3 seat-tracker.py

# Set today's location
python3 seat-tracker.py --home

# View updated calendar
python3 seat-tracker.py
```

### Weekly Planning

```bash
python3 seat-tracker.py --interactive

tracker> set 2025-10-20 H
tracker> set 2025-10-21 L
tracker> set 2025-10-22 L
tracker> set 2025-10-23 L
tracker> set 2025-10-24 H
tracker> calendar
```

### Monthly Review

```bash
# View calendar (default)
python3 seat-tracker.py

# Check statistics
python3 seat-tracker.py --stats 30

# Check statistics with visual calendar
python3 seat-tracker.py --stats 30 --with-calendar
```

### Vacation Planning

```bash
python3 seat-tracker.py --interactive

tracker> set 2025-12-24 V
tracker> set 2025-12-25 X
tracker> set 2025-12-26 V
tracker> set 2025-12-27 V
tracker> calendar 2025-12
```

## All Commands

### Set Location

```bash
--home [DATE]         # Work from home
--lab [DATE]          # Work from lab
--travel [DATE]       # Work travel
--vacation [DATE]     # Vacation
--holiday [DATE]      # Holiday
--weekend [DATE]      # Weekend
--other [DATE]        # Other

# Examples:
python3 seat-tracker.py --home              # Today
python3 seat-tracker.py --lab 2025-10-15    # Specific date
```

### View & Query

```bash
--calendar [YEAR|MONTH]  # Show calendar
--get [DATE]             # Get designation
--stats [PERIOD]         # Show statistics (30/90/365/all/number)
--with-calendar          # Show calendar with statistics (use with --stats or --work-summary)
--work-summary [DAYS]    # Work days summary
--validate [YEAR]        # Validate data file
--no-color               # Disable colored output

# Examples:
python3 seat-tracker.py --calendar          # Current month
python3 seat-tracker.py --calendar 2025     # Full year 2025
python3 seat-tracker.py --calendar 2025-11  # November 2025
python3 seat-tracker.py --calendar --no-color # Plain text
python3 seat-tracker.py --get               # Today
python3 seat-tracker.py --get 2025-10-15    # Specific date
python3 seat-tracker.py --stats 30          # Last 30 days
python3 seat-tracker.py --stats 30 --with-calendar # Last 30 days with calendar view
python3 seat-tracker.py --stats all         # All periods
python3 seat-tracker.py --stats all --with-calendar # All periods with calendar views
python3 seat-tracker.py --stats 7 --with-calendar # Last 7 days with calendar
python3 seat-tracker.py --work-summary 90   # Last 90 days
python3 seat-tracker.py --work-summary 30 --with-calendar # Work summary with calendar
```

### Interactive Mode

```bash
--interactive            # Start interactive mode
python3 seat-tracker.py --i   # Short form
```

## Short Aliases

Save typing with short aliases:

```bash
python3 seat-tracker.py --h              # --home
python3 seat-tracker.py --l              # --lab
python3 seat-tracker.py --v 2025-12-25   # --vacation
python3 seat-tracker.py --c              # --calendar
python3 seat-tracker.py --s 30           # --stats 30
python3 seat-tracker.py --s 30 --wc      # --stats 30 --with-calendar
python3 seat-tracker.py --g              # --get
```

## Interactive Mode Commands

Once in interactive mode (`python3 seat-tracker.py --interactive`):

```
calendar [YYYY|YYYY-MM] - Show calendar (current/year/month)
set <date> <des>        - Set designation (use full name or short code)
get <date>              - Get designation
stats [30|90|365|all|N] - Show statistics
work-summary [days]     - Show work days summary
validate [year]         - Validate data file
force [on|off]          - Toggle overwrite prompts
help                    - Show help
quit                    - Exit
```

## Data Format

Data is stored in `data/YEAR.log` with readable full names:

```
2025-10-14|W42|HOME
2025-10-15|W42|LAB
2025-10-16|W42|VACATION
2025-10-17|W42|TRAVEL
```

- Calendar displays use single letters (H, L, V, T)
- Data files use full names (HOME, LAB, VACATION, TRAVEL)
- Both work in interactive mode!

## Tips

1. **Quick view**: Just run `python3 seat-tracker.py` to see the current month (default behavior)
2. **Daily use**: Set location with `python3 seat-tracker.py --home` (or `--lab`, `--vacation`)
3. **Weekly planning**: Use `--interactive` mode to set multiple dates quickly
4. **Check patterns**: Run `python3 seat-tracker.py` to see your month at a glance
5. **Short codes**: Use H, L, T, V, X, W, O in interactive mode for speed
6. **Statistics**: Run `--stats` monthly to track your work patterns

## Auto-Populate Weekends

When you set any weekday designation, the tracker automatically adds Saturday and Sunday of that week as WEEKEND (unless already set):

```bash
python3 seat-tracker.py --home 2025-10-15
# Saturday/Sunday of that week automatically set to WEEKEND
```

## Defaults

The calendar shows only actual tracked data (not defaults). Empty spaces mean no data has been entered for that date.

Smart defaults are available for statistics calculations:
- **Mon/Fri**: HOME (H)
- **Tue/Wed/Thu**: LAB (L)
- **Sat/Sun**: WEEKEND (W)

## Testing

Quick manual tests:

```bash
python3 seat-tracker.py --home
python3 seat-tracker.py --calendar
python3 seat-tracker.py --stats 30
python3 seat-tracker.py --validate
```

Or run the complete integration test suite:

```bash
./tests/test_tracker.sh
```
