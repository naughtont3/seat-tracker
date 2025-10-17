"""
Work Location Tracker

A tool for tracking daily work location designations.
"""

from .location_tracker import LocationTracker, LocationDesignation
from .calendar_view import CalendarView
from .statistics import LocationStatistics
from .interactive import InteractiveMode

__version__ = '1.0.1'
__all__ = [
    'LocationTracker',
    'LocationDesignation',
    'CalendarView',
    'LocationStatistics',
    'InteractiveMode',
]
