"""
Calendar view for displaying monthly work location data.
"""

import calendar
from datetime import datetime, date
from typing import Dict, Optional
from .location_tracker import LocationDesignation, LocationTracker


class CalendarView:
    """Displays a textual calendar with work location designations."""

    # ANSI color codes
    COLOR_RESET = "\033[0m"
    COLOR_BOLD = "\033[1m"
    COLOR_WEEK = "\033[36m"      # Cyan for week numbers
    COLOR_HEADER = "\033[1;37m"   # Bold white for headers
    COLOR_HOME = "\033[32m"       # Green for HOME
    COLOR_LAB = "\033[34m"        # Blue for LAB
    COLOR_TRAVEL = "\033[35m"     # Magenta for TRAVEL
    COLOR_WEEKEND = "\033[90m"    # Dark gray for WEEKEND
    COLOR_VACATION = "\033[33m"   # Yellow for VACATION
    COLOR_HOLIDAY = "\033[31m"    # Red for HOLIDAY
    COLOR_OTHER = "\033[37m"      # White for OTHER

    def __init__(self, tracker: LocationTracker, use_color: bool = True):
        """Initialize calendar view with a location tracker.

        Args:
            tracker: LocationTracker instance
            use_color: Whether to use ANSI colors (default: True)
        """
        self.tracker = tracker
        self.use_color = use_color

    def _get_designation_color(self, designation: LocationDesignation) -> str:
        """Get ANSI color code for designation."""
        if not self.use_color:
            return ""

        color_map = {
            LocationDesignation.HOME: self.COLOR_HOME,
            LocationDesignation.LAB: self.COLOR_LAB,
            LocationDesignation.TRAVEL: self.COLOR_TRAVEL,
            LocationDesignation.WEEKEND: self.COLOR_WEEKEND,
            LocationDesignation.VACATION: self.COLOR_VACATION,
            LocationDesignation.HOLIDAY: self.COLOR_HOLIDAY,
            LocationDesignation.OTHER: self.COLOR_OTHER,
        }
        return color_map.get(designation, "")

    def _get_designation_display(self, designation: LocationDesignation) -> str:
        """Get short display string for designation."""
        return designation.short_code

    def render_month(self, year: int, month: int, highlight_day: Optional[int] = None) -> str:
        """
        Render a month calendar with work location designations.

        Args:
            year: Year to display
            month: Month to display (1-12)
            highlight_day: Day to highlight (1-31), typically today

        Returns:
            String representation of the calendar
        """
        from datetime import timedelta

        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]

        # Build header
        lines = []
        # Center month/year above the calendar (now 26 chars wide with week numbers)
        header = f"{month_name} {year}".center(26)
        lines.append(header)
        lines.append("")

        # Day headers - each cell is 3 chars wide, plus W## prefix
        day_headers = "    Mo Tu We Th Fr Sa Su"
        lines.append(day_headers)
        lines.append("-" * 26)

        # Get the first day of the month to calculate dates for previous month days
        first_day = date(year, month, 1)

        # Load data for current year and potentially previous/next year
        current_year_data = self.tracker.load_year_data(year)
        prev_year_data = {}
        next_year_data = {}

        if month == 1:
            # January might show December from previous year
            prev_year_data = self.tracker.load_year_data(year - 1)
        if month == 12:
            # December might show January from next year
            next_year_data = self.tracker.load_year_data(year + 1)

        # Build calendar rows - two lines per week (days, then designations)
        for week_idx, week in enumerate(cal):
            # Calculate actual dates for this week (including prev/next month days)
            week_dates = []

            # Find first non-zero day to anchor our calculations
            first_month_day = next((d for d in week if d != 0), None)

            if first_month_day:
                # Start from this known date and work backwards/forwards
                anchor_date = date(year, month, first_month_day)
                anchor_weekday = anchor_date.weekday()  # 0=Monday

                # Calculate dates for all 7 days of the week
                for day_idx in range(7):
                    days_offset = day_idx - anchor_weekday
                    actual_date = anchor_date + timedelta(days=days_offset)
                    week_dates.append(actual_date)
            else:
                # Empty week (shouldn't happen)
                week_dates = [None] * 7

            # Get week number from first valid date
            week_num = None
            for d in week_dates:
                if d:
                    week_num = d.isocalendar()[1]
                    break

            day_row = []
            des_row = []

            for day_idx, (day, actual_date) in enumerate(zip(week, week_dates)):
                if actual_date is None:
                    # Empty cell
                    day_row.append("   ")
                    des_row.append("   ")
                else:
                    # Determine which year's data to use
                    if actual_date.year < year:
                        year_data = prev_year_data
                    elif actual_date.year > year:
                        year_data = next_year_data
                    else:
                        year_data = current_year_data

                    # Check if this is today (for highlighting)
                    today = date.today()
                    is_today = (actual_date == today)

                    # Check if this is the current month (for dimming)
                    is_current_month = (actual_date.month == month)

                    # Day number (right-aligned in 2 chars, plus 1 space)
                    day_num = actual_date.day
                    if is_today:
                        # Bold and underline current day
                        if self.use_color:
                            day_cell = f"{self.COLOR_BOLD}\033[4m{day_num:2d}{self.COLOR_RESET} "
                        else:
                            day_cell = f"\033[1m\033[4m{day_num:2d}\033[0m "
                    else:
                        day_cell = f"{day_num:2d} "

                    # Designation letter (aligned under the rightmost digit)
                    if actual_date in year_data:
                        designation = year_data[actual_date]
                        des_str = self._get_designation_display(designation)
                        if self.use_color:
                            color = self._get_designation_color(designation)
                            des_cell = f" {color}{des_str}{self.COLOR_RESET} "
                        else:
                            des_cell = f" {des_str} "
                    else:
                        # No data for this day - show empty
                        des_cell = "   "

                    day_row.append(day_cell)
                    des_row.append(des_cell)

            # Add week number prefix to day row
            if week_num:
                if self.use_color:
                    week_prefix = f"{self.COLOR_WEEK}W{week_num:02d}{self.COLOR_RESET} "
                else:
                    week_prefix = f"W{week_num:02d} "
            else:
                week_prefix = "    "

            lines.append(week_prefix + "".join(day_row))
            lines.append("    " + "".join(des_row))  # Empty prefix for designation row
            #lines.append("")  # Blank line between weeks

        return "\n".join(lines)

    def render_current_month(self, highlight_today: bool = True) -> str:
        """
        Render the current month with today highlighted.

        Args:
            highlight_today: Whether to highlight today's date

        Returns:
            String representation of the current month
        """
        today = date.today()
        highlight_day = today.day if highlight_today else None
        return self.render_month(today.year, today.month, highlight_day)

    def get_legend(self) -> str:
        """Get a compact legend explaining the designations."""
        lines = []

        # Short names for compact display
        short_names = {
            LocationDesignation.HOME: "Home",
            LocationDesignation.LAB: "Lab",
            LocationDesignation.TRAVEL: "Travel",
            LocationDesignation.WEEKEND: "Weekend",
            LocationDesignation.VACATION: "Vacation",
            LocationDesignation.HOLIDAY: "Holiday",
            LocationDesignation.OTHER: "Other",
        }

        # Build compact designation list
        if self.use_color:
            # Colored version
            parts = []
            for designation in LocationDesignation:
                color = self._get_designation_color(designation)
                short_name = short_names[designation]
                parts.append(f"{color}{designation.short_code}{self.COLOR_RESET}={short_name}")
            designations_line = "Designations: " + ", ".join(parts)
        else:
            # Plain version
            parts = []
            for designation in LocationDesignation:
                short_name = short_names[designation]
                parts.append(f"{designation.short_code}={short_name}")
            designations_line = "Designations: " + ", ".join(parts)

        lines.append("")
        lines.append(designations_line)

        if self.use_color:
            lines.append(f"Current day shown in {self.COLOR_BOLD}bold{self.COLOR_RESET}")
        else:
            lines.append("Current day shown in \033[1mbold\033[0m")

        return "\n".join(lines)

    def render_month_with_legend(self, year: int, month: int, highlight_day: Optional[int] = None) -> str:
        """Render month calendar with legend."""
        calendar_str = self.render_month(year, month, highlight_day)
        legend_str = self.get_legend()
        return f"{legend_str}\n{calendar_str}"

    def render_current_month_with_legend(self) -> str:
        """Render current month with legend and today highlighted."""
        calendar_str = self.render_current_month(highlight_today=True)
        legend_str = self.get_legend()
        return f"{legend_str}\n{calendar_str}"

    def render_year(self, year: int) -> str:
        """
        Render a full year calendar with all 12 months.

        Args:
            year: Year to display

        Returns:
            String representation of the full year calendar
        """
        lines = []

        # Year header
        lines.append("")
        year_header = f"{year}".center(26)
        lines.append(year_header)
        lines.append("=" * 26)
        lines.append("")

        today = date.today()

        # Render each month
        for month in range(1, 13):
            # Highlight current day only if viewing current month
            highlight_day = None
            if year == today.year and month == today.month:
                highlight_day = today.day

            month_calendar = self.render_month(year, month, highlight_day)
            lines.append(month_calendar)
            lines.append("")  # Extra space between months

        return "\n".join(lines)

    def render_year_with_legend(self, year: int) -> str:
        """Render full year calendar with legend."""
        calendar_str = self.render_year(year)
        legend_str = self.get_legend()
        return f"{legend_str}\n{calendar_str}"

    def render_date_range(self, start_date: date, end_date: date) -> str:
        """
        Render calendar view for a date range, showing all months that overlap.

        Args:
            start_date: Start date of the range
            end_date: End date of the range

        Returns:
            String representation of calendars covering the date range
        """
        lines = []

        # Determine which months to display
        current = date(start_date.year, start_date.month, 1)
        end_month = date(end_date.year, end_date.month, 1)

        today = date.today()

        # Render each month that overlaps with the range
        while current <= end_month:
            # Highlight current day only if viewing current month
            highlight_day = None
            if current.year == today.year and current.month == today.month:
                highlight_day = today.day

            month_calendar = self.render_month(current.year, current.month, highlight_day)
            lines.append(month_calendar)
            lines.append("")  # Extra space between months

            # Move to next month
            if current.month == 12:
                current = date(current.year + 1, 1, 1)
            else:
                current = date(current.year, current.month + 1, 1)

        return "\n".join(lines)

    def render_date_range_with_legend(self, start_date: date, end_date: date) -> str:
        """
        Render calendar view for a date range with legend.

        Args:
            start_date: Start date of the range
            end_date: End date of the range

        Returns:
            String representation of calendars with legend
        """
        legend_str = self.get_legend()
        calendar_str = self.render_date_range(start_date, end_date)

        # Add range header
        range_header = f"\nDate Range: {start_date} to {end_date}"
        range_header += f" ({(end_date - start_date).days + 1} days)\n"

        return f"{legend_str}\n{range_header}\n{calendar_str}"
