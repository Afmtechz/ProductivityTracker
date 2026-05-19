"""
Helper utility functions for common operations.
Includes date handling, streak calculations, and formatting.
"""

from datetime import datetime, timedelta, date
from typing import List, Dict, Tuple
from .constants import HabitFrequency, TaskPriority, XP_REWARDS, PRIORITY_MULTIPLIERS


def get_week_dates(reference_date: date = None) -> Tuple[date, date]:
    """
    Get Monday and Sunday of the week containing reference_date.

    Args:
        reference_date: Date to get week for (default: today)

    Returns:
        Tuple of (Monday, Sunday) dates
    """
    if reference_date is None:
        reference_date = date.today()

    # Get Monday (0 = Monday)
    monday = reference_date - timedelta(days=reference_date.weekday())
    sunday = monday + timedelta(days=6)

    return monday, sunday


def get_month_dates(reference_date: date = None) -> Tuple[date, date]:
    """
    Get first and last day of the month containing reference_date.

    Args:
        reference_date: Date to get month for (default: today)

    Returns:
        Tuple of (1st, last day) of month
    """
    if reference_date is None:
        reference_date = date.today()

    # First day of month
    first_day = date(reference_date.year, reference_date.month, 1)

    # Last day of month
    if reference_date.month == 12:
        last_day = date(reference_date.year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(reference_date.year, reference_date.month + 1, 1) - timedelta(days=1)

    return first_day, last_day


def get_date_range_for_frequency(frequency: str, count: int = 1, reference_date: date = None) -> Tuple[date, date]:
    """
    Get date range based on frequency type.

    Args:
        frequency: Type of frequency (daily, weekly, monthly)
        count: Number of periods
        reference_date: Reference date for calculation

    Returns:
        Tuple of (start_date, end_date)
    """
    if reference_date is None:
        reference_date = date.today()

    if frequency == HabitFrequency.DAILY:
        start = reference_date - timedelta(days=count)
        end = reference_date
    elif frequency == HabitFrequency.WEEKLY:
        monday, sunday = get_week_dates(reference_date)
        start = monday - timedelta(weeks=count - 1)
        end = sunday
    elif frequency == HabitFrequency.MONTHLY:
        first, last = get_month_dates(reference_date)
        start = date(first.year if reference_date.month > 1 else first.year - 1,
                     first.month - 1 if reference_date.month > 1 else 12, 1)
        if count > 1:
            start = start - timedelta(days=30 * (count - 1))
        end = last
    else:
        start = reference_date
        end = reference_date

    return start, end


def calculate_streak(
    completion_dates: List[date],
    frequency: str = HabitFrequency.DAILY
) -> Tuple[int, int]:
    """
    Calculate current and longest streak from completion dates.

    Args:
        completion_dates: List of dates when habit was completed
        frequency: Habit frequency (daily, weekly, monthly)

    Returns:
        Tuple of (current_streak, longest_streak)
    """
    if not completion_dates:
        return 0, 0

    completion_dates = sorted(completion_dates, reverse=True)
    today = date.today()

    # Calculate current streak
    current_streak = 0
    current_date = today

    for i in range(100):  # Check last 100 periods
        if frequency == HabitFrequency.DAILY:
            check_date = current_date - timedelta(days=i)
        elif frequency == HabitFrequency.WEEKLY:
            check_date = current_date - timedelta(weeks=i)
            check_date, _ = get_week_dates(check_date)
        elif frequency == HabitFrequency.MONTHLY:
            # Simplified month calculation
            check_date = current_date - timedelta(days=30 * i)
        else:
            break

        if check_date in completion_dates:
            current_streak += 1
        elif i > 0:  # Allow one day gap for tolerance
            break

    # Calculate longest streak
    longest_streak = 0
    temp_streak = 1

    for i in range(len(completion_dates) - 1):
        current = completion_dates[i]
        next_date = completion_dates[i + 1]

        if frequency == HabitFrequency.DAILY:
            diff = (current - next_date).days
        elif frequency == HabitFrequency.WEEKLY:
            diff = (current - next_date).days // 7
        elif frequency == HabitFrequency.MONTHLY:
            diff = (current.year - next_date.year) * 12 + (current.month - next_date.month)
        else:
            diff = 1

        if diff == 1:
            temp_streak += 1
        else:
            longest_streak = max(longest_streak, temp_streak)
            temp_streak = 1

    longest_streak = max(longest_streak, temp_streak)

    return current_streak, longest_streak


def calculate_xp_for_task(priority: str, base_xp: int = None) -> int:
    """
    Calculate XP earned for completing a task based on priority.

    Args:
        priority: Task priority level
        base_xp: Base XP value (default from constants)

    Returns:
        XP reward for task completion
    """
    if base_xp is None:
        base_xp = XP_REWARDS.get("task_completion_medium", 50)

    multiplier = PRIORITY_MULTIPLIERS.get(priority, 1.0)
    return int(base_xp * multiplier)


def get_level_from_xp(total_xp: int) -> Tuple[int, int]:
    """
    Calculate user level and progress to next level from total XP.

    Args:
        total_xp: Total XP earned

    Returns:
        Tuple of (current_level, xp_to_next_level)
    """
    from .constants import BASE_XP_PER_LEVEL, XP_SCALING_FACTOR

    level = 1
    xp_used = 0

    while True:
        xp_for_level = int(BASE_XP_PER_LEVEL * (XP_SCALING_FACTOR ** (level - 1)))
        if xp_used + xp_for_level <= total_xp:
            xp_used += xp_for_level
            level += 1
        else:
            break

    # XP needed for next level
    next_level_xp = int(BASE_XP_PER_LEVEL * (XP_SCALING_FACTOR ** (level - 1)))
    xp_progress = total_xp - xp_used
    xp_to_next = next_level_xp - xp_progress

    return level, xp_to_next


def format_duration(minutes: int) -> str:
    """
    Format duration in minutes to readable string.

    Args:
        minutes: Duration in minutes

    Returns:
        Formatted duration string (e.g., "1h 30m")
    """
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    mins = minutes % 60
    if mins == 0:
        return f"{hours}h"
    return f"{hours}h {mins}m"


def calculate_completion_percentage(completed: int, total: int) -> float:
    """
    Calculate completion percentage safely.

    Args:
        completed: Number of completed items
        total: Total number of items

    Returns:
        Completion percentage (0-100)
    """
    if total == 0:
        return 0.0
    return min(100.0, (completed / total) * 100)


def get_week_heatmap_data(completion_dates: List[date]) -> Dict[str, int]:
    """
    Generate week heatmap data from completion dates.

    Args:
        completion_dates: List of completion dates

    Returns:
        Dictionary with day names as keys and 0 or 1 as values
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap = {day: 0 for day in days}

    monday, sunday = get_week_dates()

    for i, day in enumerate(days):
        current_date = monday + timedelta(days=i)
        if current_date in completion_dates:
            heatmap[day] = 1

    return heatmap
