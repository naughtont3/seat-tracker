#!/usr/bin/env python3
"""
Command-line interface for the work location tracker.
"""

import argparse
import sys
import os
from datetime import datetime, date
from pathlib import Path
from .location_tracker import LocationTracker, LocationDesignation
from .calendar_view import CalendarView
from .statistics import LocationStatistics
from .interactive import InteractiveMode
from . import __version__


def setup_parser(full_help=False):
    """Set up command-line argument parser.

    Args:
        full_help: If True, show detailed examples and documentation
    """
    # Build the configuration section with current env var value
    env_var = os.environ.get('SEAT_TRACKER_DATA_DIR')

    if full_help:
        config_section = """
Configuration:
  Data Directory Priority:
    1. --data-dir command line option (highest priority)
    2. SEAT_TRACKER_DATA_DIR environment variable"""
        if env_var:
            config_section += f"\n       Currently set: {env_var}"
        config_section += """
    3. ./data directory (default)
"""
        epilog = config_section + """
Examples:
  # Start interactive mode
  %(prog)s

  # Set today's location
  %(prog)s --home
  %(prog)s --lab
  %(prog)s --travel

  # Set specific date
  %(prog)s --home 2025-10-15
  %(prog)s --vacation 2025-10-18

  # Delete a date entry (removes from log file)
  %(prog)s --delete 2025-10-17

  # Show current month calendar
  %(prog)s --calendar

  # Show statistics
  %(prog)s --stats

  # Validate data
  %(prog)s --validate

Removing Entries:
  Method 1: Use --delete flag (recommended)
    %(prog)s --delete 2025-10-17

  Method 2: Manually edit the data file
    Edit $SEAT_TRACKER_DATA_DIR/YYYY.log (or ./data/YYYY.log)
    Remove the line containing the date you want to delete

Designations:
  H - Work From Home      (--home)
  L - Work From Lab       (--lab)
  T - Work Travel         (--travel)
  W - Weekend             (--weekend)
  V - Vacation            (--vacation)
  X - Holiday             (--holiday)
  O - Other               (--other)
        """
    else:
        epilog = """
Quick Examples:
  %(prog)s --home                   # Set today as Work From Home
  %(prog)s --lab 2025-10-15         # Set specific date as Work From Lab
  %(prog)s --delete 2025-10-17      # Delete a date entry
  %(prog)s --calendar               # Show calendar view
  %(prog)s --stats                  # Show statistics

Designations: H=Home, L=Lab, T=Travel, W=Weekend, V=Vacation, X=Holiday, O=Other

Use --help-full for detailed examples and documentation.
        """

    parser = argparse.ArgumentParser(
        description=f'Work Location Tracker v{__version__} - Track daily work location designations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
        add_help=False  # We'll add custom help handling
    )

    # Custom help arguments
    parser.add_argument(
        '--help', '-h',
        action='store_true',
        help='Show this help message and exit'
    )
    parser.add_argument(
        '--help-full',
        action='store_true',
        help='Show detailed help with full examples and documentation'
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version information and exit'
    )

    parser.add_argument(
        '--data-dir',
        type=Path,
        help='Directory for data files (default: SEAT_TRACKER_DATA_DIR env var or ./data)'
    )

    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Force overwrite without prompting'
    )

    parser.add_argument(
        '--no-color', '--nocolor',
        action='store_true',
        help='Disable colored output'
    )

    # Location designation flags
    location_group = parser.add_mutually_exclusive_group()
    location_group.add_argument(
        '--home', '--h',
        metavar='DATE',
        nargs='?',
        const='TODAY',
        help='Set location to HOME (Work From Home)'
    )
    location_group.add_argument(
        '--lab', '--l',
        metavar='DATE',
        nargs='?',
        const='TODAY',
        help='Set location to LAB (Work From Lab)'
    )
    location_group.add_argument(
        '--travel', '--t',
        metavar='DATE',
        nargs='?',
        const='TODAY',
        help='Set location to TRAVEL (Work Travel)'
    )
    location_group.add_argument(
        '--vacation', '--v',
        metavar='DATE',
        nargs='?',
        const='TODAY',
        help='Set location to VACATION'
    )
    location_group.add_argument(
        '--holiday', '--x',
        metavar='DATE',
        nargs='?',
        const='TODAY',
        help='Set location to HOLIDAY'
    )
    location_group.add_argument(
        '--weekend', '--w',
        metavar='DATE',
        nargs='?',
        const='TODAY',
        help='Set location to WEEKEND'
    )
    location_group.add_argument(
        '--other', '--o',
        metavar='DATE',
        nargs='?',
        const='TODAY',
        help='Set location to OTHER'
    )
    location_group.add_argument(
        '--delete', '--d',
        metavar='DATE',
        help='Delete designation for a specific date (removes from log file)'
    )

    # Action flags
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        '--calendar', '--cal', '--c',
        metavar='YEAR|MONTH',
        nargs='?',
        const='CURRENT',
        help='Show calendar (optional: YYYY or YYYY-MM)'
    )
    action_group.add_argument(
        '--stats', '--s',
        metavar='PERIOD',
        nargs='?',
        const='30',
        help='Show statistics (default: 30 days; options: 30, 90, 365, all, or any number)'
    )

    parser.add_argument(
        '--with-calendar', '--wc',
        action='store_true',
        help='Show calendar view with statistics (use with --stats or --work-summary)'
    )
    action_group.add_argument(
        '--work-summary', '--ws',
        metavar='DAYS',
        nargs='?',
        const='30',
        type=str,
        help='Show work days summary (default: 30 days)'
    )
    action_group.add_argument(
        '--get', '--g',
        metavar='DATE',
        nargs='?',
        const='TODAY',
        help='Get designation for date (default: today)'
    )
    action_group.add_argument(
        '--validate', '--val',
        metavar='YEAR',
        nargs='?',
        const='CURRENT',
        help='Validate data file (default: current year)'
    )
    action_group.add_argument(
        '--interactive', '--i',
        action='store_true',
        help='Start interactive mode'
    )

    return parser


def parse_date(date_str: str) -> date:
    """Parse date string or raise ValueError."""
    if date_str == 'TODAY':
        return date.today()
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def handle_set_location(tracker: LocationTracker, designation: LocationDesignation, date_str: str, force: bool = False):
    """Handle setting a location designation."""
    try:
        date_obj = parse_date(date_str)
    except ValueError:
        print(f"Error: Invalid date format '{date_str}'. Use YYYY-MM-DD.")
        return 1

    # Warn if setting a future date
    if date_obj > date.today():
        print(f"Warning: Setting designation for future date {date_obj}")

    # Check if date already has a designation
    if not force:
        year = date_obj.year
        data = tracker.load_year_data(year)
        if date_obj in data:
            existing = data[date_obj]
            print(f"Warning: {date_obj} already set to {existing.short_code} - {existing.description}")
            response = input(f"Overwrite with {designation.short_code} - {designation.description}? [y/N]: ")
            if response.lower() not in ['y', 'yes']:
                print("Cancelled.")
                return 0

    tracker.set_designation(date_obj, designation)
    print(f"Set {date_obj} to {designation.short_code} - {designation.description}")
    return 0


def handle_calendar(tracker: LocationTracker, month_str: str, use_color: bool = True):
    """Handle calendar display."""
    calendar_view = CalendarView(tracker, use_color=use_color)

    if month_str == 'CURRENT':
        print(calendar_view.render_current_month_with_legend())
    else:
        try:
            # Check if it's a year only (YYYY) or year-month (YYYY-MM)
            if '-' in month_str:
                # Year-month format
                year, month = map(int, month_str.split('-'))
                today = date.today()
                highlight_day = today.day if (year == today.year and month == today.month) else None
                print(calendar_view.render_month_with_legend(year, month, highlight_day))
            else:
                # Year only format
                year = int(month_str)
                print(calendar_view.render_year_with_legend(year))
        except (ValueError, IndexError):
            print("Error: Invalid format. Use YYYY (e.g., 2024) or YYYY-MM (e.g., 2025-10)")
            return 1

    return 0


def handle_stats(tracker: LocationTracker, period: str, show_calendar: bool = False, use_color: bool = True):
    """Handle statistics display."""
    from datetime import timedelta

    statistics = LocationStatistics(tracker)

    # Normalize period to lowercase for case-insensitive comparison
    period_lower = period.lower()

    if period_lower == 'all':
        # For 'all', we show calendar for each period before the stats
        if show_calendar:
            calendar_view = CalendarView(tracker, use_color=use_color)

            # 30-day calendar
            stats_30 = statistics.get_30_day_stats()
            print("=" * 50)
            print("30-Day Period Calendar:")
            print("=" * 50)
            print(calendar_view.render_date_range_with_legend(stats_30['start_date'], stats_30['end_date']))
            print()

            # 90-day calendar
            stats_90 = statistics.get_90_day_stats()
            print("=" * 50)
            print("90-Day Period Calendar:")
            print("=" * 50)
            print(calendar_view.render_date_range_with_legend(stats_90['start_date'], stats_90['end_date']))
            print()

            # 365-day calendar
            stats_365 = statistics.get_365_day_stats()
            print("=" * 50)
            print("365-Day Period Calendar:")
            print("=" * 50)
            print(calendar_view.render_date_range_with_legend(stats_365['start_date'], stats_365['end_date']))
            print()

        print(statistics.generate_summary_report())
    elif period == '30':
        stats = statistics.get_30_day_stats()
        if show_calendar:
            calendar_view = CalendarView(tracker, use_color=use_color)
            print(calendar_view.render_date_range_with_legend(stats['start_date'], stats['end_date']))
            print("\n" + "=" * 50)
        print(statistics.format_stats_report(stats))
    elif period == '90':
        stats = statistics.get_90_day_stats()
        if show_calendar:
            calendar_view = CalendarView(tracker, use_color=use_color)
            print(calendar_view.render_date_range_with_legend(stats['start_date'], stats['end_date']))
            print("\n" + "=" * 50)
        print(statistics.format_stats_report(stats))
    elif period == '365':
        stats = statistics.get_365_day_stats()
        if show_calendar:
            calendar_view = CalendarView(tracker, use_color=use_color)
            print(calendar_view.render_date_range_with_legend(stats['start_date'], stats['end_date']))
            print("\n" + "=" * 50)
        print(statistics.format_stats_report(stats))
    else:
        # Try to parse as a number of days
        try:
            days = int(period)
            if days <= 0:
                print(f"Error: Number of days must be positive")
                return 1

            end_date = date.today()
            start_date = end_date - timedelta(days=days-1)
            stats = statistics.get_period_stats(start_date, end_date)
            if show_calendar:
                calendar_view = CalendarView(tracker, use_color=use_color)
                print(calendar_view.render_date_range_with_legend(stats['start_date'], stats['end_date']))
                print("\n" + "=" * 50)
            print(statistics.format_stats_report(stats))
        except ValueError:
            print(f"Error: Invalid period '{period}'. Use 30, 90, 365, all, or any number of days.")
            return 1

    return 0


def handle_work_summary(tracker: LocationTracker, days_str: str, show_calendar: bool = False, use_color: bool = True):
    """Handle work summary display."""
    from datetime import timedelta

    try:
        days = int(days_str)
    except ValueError:
        print(f"Error: Invalid number of days '{days_str}'")
        return 1

    statistics = LocationStatistics(tracker)
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    stats = statistics.get_period_stats(start_date, end_date)

    if show_calendar:
        calendar_view = CalendarView(tracker, use_color=use_color)
        print(calendar_view.render_date_range_with_legend(stats['start_date'], stats['end_date']))
        print("\n" + "=" * 50)

    print(statistics.generate_work_days_summary(stats))
    return 0


def handle_get(tracker: LocationTracker, date_str: str):
    """Handle getting a designation."""
    try:
        date_obj = parse_date(date_str)
    except ValueError:
        print(f"Error: Invalid date format '{date_str}'. Use YYYY-MM-DD.")
        return 1

    designation = tracker.get_designation(date_obj)
    print(f"{date_obj}: {designation.short_code} - {designation.description}")
    return 0


def handle_validate(tracker: LocationTracker, year_str: str):
    """Handle data validation."""
    if year_str == 'CURRENT':
        year = date.today().year
    else:
        try:
            year = int(year_str)
        except ValueError:
            print(f"Error: Invalid year '{year_str}'")
            return 1

    print(f"Validating data for {year}...")
    errors = tracker.validate_data(year)

    if not errors:
        print(f"Validation passed: No errors found in {year}.log")
        return 0
    else:
        print(f"Validation failed: Found {len(errors)} error(s)")
        print()
        for error in errors:
            print(f"  - {error}")
        return 1


def handle_delete(tracker: LocationTracker, date_str: str, force: bool = False):
    """Handle deleting a designation."""
    try:
        date_obj = parse_date(date_str)
    except ValueError:
        print(f"Error: Invalid date format '{date_str}'. Use YYYY-MM-DD.")
        return 1

    # Check if date has a designation
    year = date_obj.year
    data = tracker.load_year_data(year)

    if date_obj not in data:
        print(f"Error: No entry found for {date_obj}")
        return 1

    existing = data[date_obj]

    # Confirm deletion unless force flag is set
    if not force:
        print(f"Found entry: {date_obj} -> {existing.short_code} - {existing.description}")
        response = input(f"Delete this entry? [y/N]: ")
        if response.lower() not in ['y', 'yes']:
            print("Cancelled.")
            return 0

    # Delete the designation
    if tracker.delete_designation(date_obj):
        print(f"Deleted entry for {date_obj}")
        return 0
    else:
        print(f"Error: Failed to delete entry for {date_obj}")
        return 1


def main():
    """Main entry point."""
    # Check if --help-full is in sys.argv before parsing
    if '--help-full' in sys.argv:
        parser = setup_parser(full_help=True)
        parser.print_help()
        return 0

    # Regular parser for normal operation
    parser = setup_parser(full_help=False)
    args = parser.parse_args()

    # Handle regular --help
    if args.help:
        parser.print_help()
        return 0

    # Handle --version
    if args.version:
        print(f"Work Location Tracker v{__version__}")
        return 0

    # Initialize tracker
    tracker = LocationTracker(data_dir=args.data_dir)

    # Check for location designation flags
    if args.home:
        return handle_set_location(tracker, LocationDesignation.HOME, args.home, args.force)
    elif args.lab:
        return handle_set_location(tracker, LocationDesignation.LAB, args.lab, args.force)
    elif args.travel:
        return handle_set_location(tracker, LocationDesignation.TRAVEL, args.travel, args.force)
    elif args.vacation:
        return handle_set_location(tracker, LocationDesignation.VACATION, args.vacation, args.force)
    elif args.holiday:
        return handle_set_location(tracker, LocationDesignation.HOLIDAY, args.holiday, args.force)
    elif args.weekend:
        return handle_set_location(tracker, LocationDesignation.WEEKEND, args.weekend, args.force)
    elif args.other:
        return handle_set_location(tracker, LocationDesignation.OTHER, args.other, args.force)
    elif args.delete:
        return handle_delete(tracker, args.delete, args.force)

    # Check for action flags
    elif args.calendar:
        use_color = not args.no_color
        return handle_calendar(tracker, args.calendar, use_color=use_color)
    elif args.stats:
        use_color = not args.no_color
        return handle_stats(tracker, args.stats, show_calendar=args.with_calendar, use_color=use_color)
    elif args.work_summary:
        use_color = not args.no_color
        return handle_work_summary(tracker, args.work_summary, show_calendar=args.with_calendar, use_color=use_color)
    elif args.get:
        return handle_get(tracker, args.get)
    elif args.validate:
        return handle_validate(tracker, args.validate)
    elif args.interactive:
        use_color = not args.no_color
        interactive = InteractiveMode(tracker, use_color=use_color)
        interactive.run()
        return 0

#    # Default: start interactive mode
#    else:
#        use_color = not args.no_color
#        interactive = InteractiveMode(tracker, use_color=use_color)
#        interactive.run()
#        return 0
#
    # Default: start non-interactive mode showing calendar
    else:
        use_color = not args.no_color
        return handle_calendar(tracker, "CURRENT", use_color=use_color)


if __name__ == '__main__':
    sys.exit(main())
