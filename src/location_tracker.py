"""
Work location tracking system.
Maintains daily work location designations in a text file.
"""

from datetime import datetime, timedelta, date
from enum import Enum
from pathlib import Path
from typing import Dict, Optional
import os
import re


class LocationDesignation(Enum):
    """Valid work location designations."""
    HOME = ("H", "Work From Home")
    LAB = ("L", "Work From Lab")
    TRAVEL = ("T", "Work Travel")
    WEEKEND = ("W", "Weekend")
    VACATION = ("V", "Vacation")
    HOLIDAY = ("X", "Holiday")
    OTHER = ("O", "Other")

    def __init__(self, short_code, description):
        self.short_code = short_code
        self.description = description

    @classmethod
    def from_short_code(cls, code: str):
        """Get designation from single-letter short code."""
        for designation in cls:
            if designation.short_code == code.upper():
                return designation
        raise ValueError(f"Unknown short code: {code}")


class LocationTracker:
    """Manages work location data storage and retrieval."""

    def __init__(self, data_dir: Path = None):
        """Initialize tracker with data directory.

        Args:
            data_dir: Optional data directory path. If not provided, uses:
                      1. SEAT_TRACKER_DATA_DIR environment variable
                      2. Falls back to ./data relative to package
        """
        if data_dir is None:
            # Check environment variable first
            env_dir = os.environ.get('SEAT_TRACKER_DATA_DIR')
            if env_dir:
                # Expand environment variables and user home directory
                env_dir = os.path.expandvars(env_dir)
                data_dir = Path(env_dir).expanduser()
            else:
                # Fall back to default ./data directory
                data_dir = Path(__file__).parent.parent / "data"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_data_file(self, year: int) -> Path:
        """Get the data file path for a given year."""
        return self.data_dir / f"{year}.log"

    def _get_default_designation(self, date: datetime.date) -> LocationDesignation:
        """Get default designation based on day of week."""
        weekday = date.weekday()  # Monday=0, Sunday=6

        if weekday in [0, 4]:  # Monday or Friday
            return LocationDesignation.HOME
        elif weekday in [1, 2, 3]:  # Tuesday, Wednesday, Thursday
            return LocationDesignation.LAB
        else:  # Saturday or Sunday
            return LocationDesignation.WEEKEND

    def _get_week_number(self, date: datetime.date) -> int:
        """Get ISO week number for a date."""
        return date.isocalendar()[1]

    def _parse_log_line(self, line: str) -> Optional[tuple]:
        """
        Parse a log line into (date, designation, week_number).
        Expected format: YYYY-MM-DD|WXX|DESIGNATION_NAME
        """
        line = line.strip()
        if not line or line.startswith('#'):
            return None

        pattern = r'^(\d{4}-\d{2}-\d{2})\|W(\d{2})\|([A-Z]+)$'
        match = re.match(pattern, line)

        if not match:
            return None

        date_str, week_str, designation_str = match.groups()

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            week_num = int(week_str)
            designation = LocationDesignation[designation_str]
            return (date, designation, week_num)
        except (ValueError, KeyError):
            return None

    def _format_log_line(self, date: datetime.date, designation: LocationDesignation) -> str:
        """Format a log line for writing."""
        week_num = self._get_week_number(date)
        return f"{date.isoformat()}|W{week_num:02d}|{designation.name}"

    def load_year_data(self, year: int) -> Dict[datetime.date, LocationDesignation]:
        """Load all data for a given year."""
        data_file = self._get_data_file(year)
        data = {}

        if not data_file.exists():
            return data

        with open(data_file, 'r') as f:
            for line in f:
                parsed = self._parse_log_line(line)
                if parsed:
                    date, designation, _ = parsed
                    data[date] = designation

        return data

    def save_year_data(self, year: int, data: Dict[datetime.date, LocationDesignation]):
        """Save all data for a given year, sorted by date."""
        data_file = self._get_data_file(year)

        # Sort dates
        sorted_dates = sorted(data.keys())

        with open(data_file, 'w') as f:
            f.write(f"# Work Location Log for {year}\n")
            f.write("# Format: YYYY-MM-DD|WXX|DESIGNATION\n")
            f.write("# Week ends on Sunday, new week starts on Monday\n")
            f.write("# Valid designations: HOME(H), LAB(L), TRAVEL(T), WEEKEND(W), VACATION(V), HOLIDAY(X), OTHER(O)\n\n")

            for date in sorted_dates:
                line = self._format_log_line(date, data[date])
                f.write(line + '\n')

    def get_designation(self, date: datetime.date) -> LocationDesignation:
        """Get designation for a specific date, returning default if not set."""
        year = date.year
        data = self.load_year_data(year)

        if date in data:
            return data[date]
        else:
            return self._get_default_designation(date)

    def _auto_populate_weekend(self, date: datetime.date, data: Dict[datetime.date, LocationDesignation]):
        """
        Auto-populate weekend entries for the week containing the given date.
        Only adds weekend entries if they don't already exist.
        """
        # Find the start of the week (Monday)
        days_since_monday = date.weekday()  # Monday=0, Sunday=6
        week_start = date - timedelta(days=days_since_monday)

        # Calculate Saturday and Sunday of this week
        saturday = week_start + timedelta(days=5)  # Saturday is 5 days after Monday
        sunday = week_start + timedelta(days=6)    # Sunday is 6 days after Monday

        # Add weekend entries if they don't exist
        if saturday not in data:
            data[saturday] = LocationDesignation.WEEKEND
        if sunday not in data:
            data[sunday] = LocationDesignation.WEEKEND

    def set_designation(self, date: datetime.date, designation: LocationDesignation, auto_weekend: bool = True):
        """
        Set designation for a specific date.

        Args:
            date: Date to set designation for
            designation: Location designation to set
            auto_weekend: If True, automatically populate weekend entries for the week
        """
        year = date.year
        data = self.load_year_data(year)
        data[date] = designation

        # Auto-populate weekend entries for this week if enabled
        if auto_weekend:
            self._auto_populate_weekend(date, data)

        self.save_year_data(year, data)

    def delete_designation(self, date: datetime.date) -> bool:
        """
        Delete designation for a specific date.

        Args:
            date: Date to delete designation for

        Returns:
            True if the date was deleted, False if it didn't exist
        """
        year = date.year
        data = self.load_year_data(year)

        if date in data:
            del data[date]
            self.save_year_data(year, data)
            return True
        return False

    def get_date_range_data(self, start_date: datetime.date, end_date: datetime.date) -> Dict[datetime.date, LocationDesignation]:
        """Get designations for a date range."""
        result = {}
        current_date = start_date

        # Group by year for efficient loading
        years_data = {}

        while current_date <= end_date:
            year = current_date.year
            if year not in years_data:
                years_data[year] = self.load_year_data(year)

            if current_date in years_data[year]:
                result[current_date] = years_data[year][current_date]
            else:
                result[current_date] = self._get_default_designation(current_date)

            current_date += timedelta(days=1)

        return result

    def validate_data(self, year: int) -> list:
        """
        Validate data for a given year.
        Returns list of validation errors.
        """
        errors = []
        data_file = self._get_data_file(year)

        if not data_file.exists():
            return errors

        with open(data_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parsed = self._parse_log_line(line)
                if not parsed:
                    errors.append(f"Line {line_num}: Invalid format - {line}")
                    continue

                date, designation, week_num = parsed
                expected_week = self._get_week_number(date)

                if week_num != expected_week:
                    errors.append(
                        f"Line {line_num}: Week number mismatch for {date} "
                        f"(expected W{expected_week:02d}, got W{week_num:02d})"
                    )

                if date.year != year:
                    errors.append(
                        f"Line {line_num}: Date {date} doesn't belong in {year}.log"
                    )

        return errors
