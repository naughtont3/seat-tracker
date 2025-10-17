"""
Interactive mode for work location tracking.
"""

from datetime import date, datetime
from typing import Optional
from .location_tracker import LocationDesignation, LocationTracker
from .calendar_view import CalendarView
from .statistics import LocationStatistics


class InteractiveMode:
    """Interactive mode for viewing and editing work location data."""

    def __init__(self, tracker: LocationTracker, use_color: bool = True):
        """Initialize interactive mode with a location tracker."""
        self.tracker = tracker
        self.calendar_view = CalendarView(tracker, use_color=use_color)
        self.statistics = LocationStatistics(tracker)
        self.running = True
        self.force_mode = False
        self.use_color = use_color

    def display_main_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 60)
        print("Work Location Tracker - Interactive Mode")
        print("=" * 60)
        print()
        print("Commands:")
        print("  calendar [YYYY|YYYY-MM] - Show calendar for current, year, or month")
        print("  set <date> <des>    - Set designation for a date (YYYY-MM-DD)")
        print("  get <date>          - Get designation for a date (YYYY-MM-DD)")
        print("  stats [days]        - Show statistics (default: 30; options: 30, 90, 365, all, or any number)")
        print("  work-summary [days] - Show work days summary (default: 30)")
        print("  validate [year]     - Validate data file (default: current year)")
        print("  force [on|off]      - Toggle force mode (skip overwrite prompts)")
        print("  help                - Show this help message")
        print("  quit                - Exit interactive mode")
        print()
        force_status = "ON" if self.force_mode else "OFF"
        print(f"Force mode: {force_status}")
        print()

    def parse_date(self, date_str: str) -> Optional[date]:
        """Parse a date string in YYYY-MM-DD format."""
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print(f"Error: Invalid date format '{date_str}'. Use YYYY-MM-DD.")
            return None

    def parse_designation(self, des_str: str) -> Optional[LocationDesignation]:
        """Parse a designation string (full name or short code)."""
        des_str = des_str.upper()

        # Try full name first
        try:
            return LocationDesignation[des_str]
        except KeyError:
            pass

        # Try short code
        try:
            return LocationDesignation.from_short_code(des_str)
        except ValueError:
            print(f"Error: Invalid designation '{des_str}'.")
            print("Valid designations:")
            for d in LocationDesignation:
                print(f"  {d.name} ({d.short_code}) - {d.description}")
            return None

    def cmd_calendar(self, args: list):
        """Show calendar for current or specified month/year."""
        if not args:
            # Show current month
            print()
            print(self.calendar_view.render_current_month_with_legend())
        elif len(args) == 1:
            # Parse YYYY or YYYY-MM
            try:
                arg = args[0]
                if '-' in arg:
                    # Year-month format
                    year, month = map(int, arg.split('-'))
                    today = date.today()
                    highlight_day = today.day if (year == today.year and month == today.month) else None
                    print()
                    print(self.calendar_view.render_month_with_legend(year, month, highlight_day))
                else:
                    # Year only format
                    year = int(arg)
                    print()
                    print(self.calendar_view.render_year_with_legend(year))
            except (ValueError, IndexError):
                print("Error: Invalid format. Use YYYY (e.g., 2024) or YYYY-MM (e.g., 2025-10)")
        else:
            print("Usage: calendar [YYYY|YYYY-MM]")

    def cmd_set(self, args: list):
        """Set designation for a date."""
        if len(args) != 2:
            print("Usage: set <date> <designation>")
            print("Example: set 2025-10-15 HOME")
            print("Short codes also work: set 2025-10-15 H")
            return

        date_obj = self.parse_date(args[0])
        if date_obj is None:
            return

        designation = self.parse_designation(args[1])
        if designation is None:
            return

        # Warn if setting a future date
        from datetime import date
        if date_obj > date.today():
            print(f"Warning: Setting designation for future date {date_obj}")

        # Check if date already has a designation
        if not self.force_mode:
            year = date_obj.year
            data = self.tracker.load_year_data(year)
            if date_obj in data:
                existing = data[date_obj]
                print(f"Warning: {date_obj} already set to {existing.short_code} - {existing.description}")
                response = input(f"Overwrite with {designation.short_code} - {designation.description}? [y/N]: ")
                if response.lower() not in ['y', 'yes']:
                    print("Cancelled.")
                    return

        self.tracker.set_designation(date_obj, designation)
        print(f"Set {date_obj} to {designation.short_code} - {designation.description}")

    def cmd_get(self, args: list):
        """Get designation for a date."""
        if len(args) != 1:
            print("Usage: get <date>")
            print("Example: get 2025-10-15")
            return

        date_obj = self.parse_date(args[0])
        if date_obj is None:
            return

        designation = self.tracker.get_designation(date_obj)
        if designation:
            print(f"{date_obj}: {designation.short_code} - {designation.description}")
        else:
            print(f"{date_obj}: No designation set")

    def cmd_stats(self, args: list):
        """Show statistics for a period."""
        from datetime import timedelta, date

        if not args:
            # Default to 30 days
            stats = self.statistics.get_30_day_stats()
            print()
            print(self.statistics.format_stats_report(stats))
        elif len(args) == 1:
            period = args[0]
            period_lower = period.lower()

            if period_lower == "all":
                # Show all periods
                print()
                print(self.statistics.generate_summary_report())
            elif period == "30":
                stats = self.statistics.get_30_day_stats()
                print()
                print(self.statistics.format_stats_report(stats))
            elif period == "90":
                stats = self.statistics.get_90_day_stats()
                print()
                print(self.statistics.format_stats_report(stats))
            elif period == "365":
                stats = self.statistics.get_365_day_stats()
                print()
                print(self.statistics.format_stats_report(stats))
            else:
                # Try to parse as a number of days
                try:
                    days = int(period)
                    if days <= 0:
                        print("Error: Number of days must be positive")
                        return

                    end_date = date.today()
                    start_date = end_date - timedelta(days=days-1)
                    stats = self.statistics.get_period_stats(start_date, end_date)
                    print()
                    print(self.statistics.format_stats_report(stats))
                except ValueError:
                    print(f"Error: Invalid period '{period}'. Use 30, 90, 365, all, or any number of days.")
        else:
            print("Usage: stats [30|90|365|all|<days>]")

    def cmd_work_summary(self, args: list):
        """Show work days summary."""
        days = 30
        if args:
            try:
                days = int(args[0])
            except ValueError:
                print("Error: Days must be a number")
                return

        end_date = date.today()
        from datetime import timedelta
        start_date = end_date - timedelta(days=days-1)
        stats = self.statistics.get_period_stats(start_date, end_date)
        print()
        print(self.statistics.generate_work_days_summary(stats))

    def cmd_validate(self, args: list):
        """Validate data file."""
        if not args:
            year = date.today().year
        else:
            try:
                year = int(args[0])
            except ValueError:
                print("Error: Year must be a number")
                return

        print(f"\nValidating data for {year}...")
        errors = self.tracker.validate_data(year)

        if not errors:
            print(f"Validation passed: No errors found in {year}.log")
        else:
            print(f"Validation failed: Found {len(errors)} error(s)")
            print()
            for error in errors:
                print(f"  - {error}")

    def cmd_help(self, args: list):
        """Show help message."""
        self.display_main_menu()

    def cmd_force(self, args: list):
        """Toggle force mode."""
        if not args:
            # Toggle
            self.force_mode = not self.force_mode
        elif args[0].lower() in ['on', '1', 'true', 'yes']:
            self.force_mode = True
        elif args[0].lower() in ['off', '0', 'false', 'no']:
            self.force_mode = False
        else:
            print("Usage: force [on|off]")
            return

        status = "ON" if self.force_mode else "OFF"
        print(f"Force mode: {status}")
        if self.force_mode:
            print("Overwrite prompts will be skipped")
        else:
            print("You will be prompted before overwriting existing dates")

    def cmd_quit(self, args: list):
        """Exit interactive mode."""
        print("\nExiting interactive mode...")
        self.running = False

    def process_command(self, command_line: str):
        """Process a command line."""
        parts = command_line.strip().split()
        if not parts:
            return

        command = parts[0].lower()
        args = parts[1:]

        # Command dispatch
        commands = {
            'calendar': self.cmd_calendar,
            'cal': self.cmd_calendar,
            'set': self.cmd_set,
            'get': self.cmd_get,
            'stats': self.cmd_stats,
            'work-summary': self.cmd_work_summary,
            'ws': self.cmd_work_summary,
            'validate': self.cmd_validate,
            'val': self.cmd_validate,
            'force': self.cmd_force,
            'help': self.cmd_help,
            'h': self.cmd_help,
            'quit': self.cmd_quit,
            'exit': self.cmd_quit,
            'q': self.cmd_quit,
        }

        if command in commands:
            try:
                commands[command](args)
            except Exception as e:
                print(f"Error executing command: {e}")
        else:
            print(f"Unknown command: {command}")
            print("Type 'help' for available commands.")

    def run(self):
        """Run the interactive mode."""
        self.display_main_menu()

        # Show current month calendar on startup
        print(self.calendar_view.render_current_month_with_legend())
        print()

        while self.running:
            try:
                command_line = input("tracker> ")
                self.process_command(command_line)
            except KeyboardInterrupt:
                print("\n\nInterrupted. Type 'quit' to exit.")
            except EOFError:
                print("\n\nExiting...")
                break
