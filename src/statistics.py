"""
Statistics and reporting for work location data.
"""

from datetime import date, timedelta
from typing import Dict
from collections import Counter
from .location_tracker import LocationDesignation, LocationTracker


class LocationStatistics:
    """Generate statistics and reports for work location data."""

    def __init__(self, tracker: LocationTracker):
        """Initialize statistics generator with a location tracker."""
        self.tracker = tracker

    def _count_designations(self, data: Dict[date, LocationDesignation]) -> Counter:
        """Count occurrences of each designation."""
        return Counter(data.values())

    def _format_percentage(self, count: int, total: int) -> str:
        """Format count as percentage."""
        if total == 0:
            return "0.0%"
        percentage = (count / total) * 100
        return f"{percentage:.1f}%"

    def get_period_stats(self, start_date: date, end_date: date) -> Dict:
        """
        Get statistics for a date range, counting only actual data entries.

        Returns:
            Dictionary with counts, percentages, and total days
        """
        # Get only actual data entries (not defaults)
        requested_days = (end_date - start_date).days + 1

        # Load actual data from files
        years_data = {}
        current_date = start_date
        actual_entries = {}

        while current_date <= end_date:
            year = current_date.year
            if year not in years_data:
                years_data[year] = self.tracker.load_year_data(year)

            # Only count if date has actual entry
            if current_date in years_data[year]:
                actual_entries[current_date] = years_data[year][current_date]

            current_date += timedelta(days=1)

        counts = self._count_designations(actual_entries)
        actual_days = len(actual_entries)

        stats = {
            'start_date': start_date,
            'end_date': end_date,
            'requested_days': requested_days,
            'actual_days': actual_days,
            'total_days': actual_days,  # Keep for backward compatibility
            'counts': {},
            'percentages': {}
        }

        for designation in LocationDesignation:
            count = counts.get(designation, 0)
            stats['counts'][designation.name] = count
            stats['percentages'][designation.name] = self._format_percentage(count, actual_days)

        return stats

    def get_30_day_stats(self, end_date: date = None) -> Dict:
        """Get statistics for the last 30 days."""
        if end_date is None:
            end_date = date.today()
        start_date = end_date - timedelta(days=29)
        return self.get_period_stats(start_date, end_date)

    def get_90_day_stats(self, end_date: date = None) -> Dict:
        """Get statistics for the last 90 days."""
        if end_date is None:
            end_date = date.today()
        start_date = end_date - timedelta(days=89)
        return self.get_period_stats(start_date, end_date)

    def get_365_day_stats(self, end_date: date = None) -> Dict:
        """Get statistics for the last 365 days."""
        if end_date is None:
            end_date = date.today()
        start_date = end_date - timedelta(days=364)
        return self.get_period_stats(start_date, end_date)

    def format_stats_report(self, stats: Dict) -> str:
        """
        Format statistics as a readable report.

        Args:
            stats: Statistics dictionary from get_period_stats

        Returns:
            Formatted report string
        """
        lines = []
        requested_days = stats.get('requested_days', stats['total_days'])
        lines.append(f"Work Location Statistics ({requested_days} days)")
        lines.append(f"Period: {stats['start_date']} to {stats['end_date']}")

        # Show actual vs requested days
        requested = stats.get('requested_days', stats['total_days'])
        actual = stats['actual_days']

        if actual < requested:
            lines.append(f"Data Coverage: {actual}/{requested} days ({self._format_percentage(actual, requested)})")
            lines.append(f"Note: Statistics based on {actual} days with actual data entries")
        else:
            lines.append(f"Total Days: {actual}")

        lines.append("")
        lines.append(f"Breakdown (percentage of all {actual} days):")
        lines.append("-" * 50)

        # Sort by count (descending)
        sorted_designations = sorted(
            LocationDesignation,
            key=lambda d: stats['counts'][d.name],
            reverse=True
        )

        for designation in sorted_designations:
            name = designation.name
            description = designation.description
            short_code = designation.short_code
            count = stats['counts'][name]
            percentage = stats['percentages'][name]

            prefix = f" ({short_code}) {description}"
            lines.append(f"{prefix:20s} Count: {count:4d}  |  {percentage:>6s}")

        lines.append("-" * 50)
        return "\n".join(lines)

    def generate_summary_report(self) -> str:
        """Generate a comprehensive summary report for 30, 90, and 365 days."""
        today = date.today()

        lines = []
        lines.append("=" * 50)
        lines.append("WORK LOCATION SUMMARY REPORT")
        lines.append(f"Generated: {today}")
        lines.append("=" * 50)
        lines.append("")

        # 30-day report
        stats_30 = self.get_30_day_stats(today)
        lines.append(self.format_stats_report(stats_30))
        lines.append("")
        lines.append("")

        # 90-day report
        stats_90 = self.get_90_day_stats(today)
        lines.append(self.format_stats_report(stats_90))
        lines.append("")
        lines.append("")

        # 365-day report
        stats_365 = self.get_365_day_stats(today)
        lines.append(self.format_stats_report(stats_365))
        lines.append("")
        lines.append("=" * 50)

        return "\n".join(lines)

    def generate_work_days_summary(self, stats: Dict) -> str:
        """
        Generate a summary focused on work days (excluding weekends/holidays/vacation).

        Args:
            stats: Statistics dictionary from get_period_stats

        Returns:
            Formatted work days summary
        """
        work_designations = ['HOME', 'LAB', 'TRAVEL']
        non_work_designations = ['WEEKEND', 'VACATION', 'HOLIDAY']

        work_days = sum(stats['counts'][d] for d in work_designations)
        total_days = stats['total_days']
        non_work_days = sum(stats['counts'][d] for d in non_work_designations)

        lines = []
        lines.append(f"Work Days Summary ({stats['start_date']} to {stats['end_date']})")
        lines.append("-" * 40)
        lines.append(f"Total Work Days: {work_days}/{total_days} ({self._format_percentage(work_days, total_days)} of all days)")
        lines.append("")
        lines.append(f"Work Breakdown (percentage of {work_days} work days only):")
        for des in work_designations:
            count = stats['counts'][des]
            if work_days > 0:
                pct = self._format_percentage(count, work_days)
                lines.append(f"  {des:6s}: {count:3d} ({pct})")
        lines.append("")
        lines.append(f"  Non-Work Days: {non_work_days:>2d}/{total_days} ({self._format_percentage(non_work_days, total_days)})")

        # Lab + Travel stats
        lt_count  = stats['counts']['LAB']
        lt_count += stats['counts']['TRAVEL']
        lth_count = stats['counts']['HOME'] + lt_count
        if work_days > 0:
            lt_pct    = self._format_percentage(lt_count, work_days)
            lth_pct   = self._format_percentage(lth_count, work_days)
            lines.append(f"   Lab + Travel: {lt_count:>2d}/{work_days} ({lt_pct})")
            lines.append(f"Lab+Travel+Home: {lth_count:>2d}/{work_days} ({lth_pct})")

        return "\n".join(lines)
