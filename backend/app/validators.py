"""
Input validation utilities for tasks, habits, and user data.
"""

import re
from datetime import datetime, date
from typing import Optional, List
from .constants import TaskPriority, TaskStatus, RecurrenceType, HabitFrequency


def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength.
    Requirements: At least 8 characters, 1 uppercase, 1 lowercase, 1 number.

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"

    return True, ""


def validate_task_data(title: str, priority: str = None, status: str = None) -> tuple[bool, List[str]]:
    """
    Validate task input data.

    Args:
        title: Task title
        priority: Task priority level
        status: Task status

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    if not title or len(title.strip()) == 0:
        errors.append("Title cannot be empty")
    elif len(title) > 255:
        errors.append("Title cannot exceed 255 characters")

    if priority and priority not in [p.value for p in TaskPriority]:
        errors.append(f"Invalid priority. Must be one of: {', '.join([p.value for p in TaskPriority])}")

    if status and status not in [s.value for s in TaskStatus]:
        errors.append(f"Invalid status. Must be one of: {', '.join([s.value for s in TaskStatus])}")

    return len(errors) == 0, errors


def validate_habit_data(name: str, frequency: str = None) -> tuple[bool, List[str]]:
    """
    Validate habit input data.

    Args:
        name: Habit name
        frequency: Habit frequency

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    if not name or len(name.strip()) == 0:
        errors.append("Habit name cannot be empty")
    elif len(name) > 100:
        errors.append("Habit name cannot exceed 100 characters")

    if frequency and frequency not in [f.value for f in HabitFrequency]:
        errors.append(f"Invalid frequency. Must be one of: {', '.join([f.value for f in HabitFrequency])}")

    return len(errors) == 0, errors


def validate_date_range(start_date: date, end_date: date) -> tuple[bool, str]:
    """
    Validate that end_date is after start_date.

    Args:
        start_date: Start date
        end_date: End date

    Returns:
        Tuple of (is_valid, error_message)
    """
    if end_date <= start_date:
        return False, "End date must be after start date"
    return True, ""


def validate_duration(duration_minutes: int) -> tuple[bool, str]:
    """
    Validate task duration.

    Args:
        duration_minutes: Duration in minutes

    Returns:
        Tuple of (is_valid, error_message)
    """
    if duration_minutes <= 0:
        return False, "Duration must be positive"
    if duration_minutes > 1440:  # 24 hours
        return False, "Duration cannot exceed 24 hours (1440 minutes)"
    return True, ""


def validate_percentage(percentage: float) -> tuple[bool, str]:
    """
    Validate percentage value (0-100).

    Args:
        percentage: Percentage value

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not 0 <= percentage <= 100:
        return False, "Percentage must be between 0 and 100"
    return True, ""


def sanitize_string(text: str, max_length: int = 255) -> str:
    """
    Sanitize string input.

    Args:
        text: Text to sanitize
        max_length: Maximum length

    Returns:
        Sanitized string
    """
    # Remove leading/trailing whitespace
    text = text.strip()
    # Remove multiple spaces
    text = ' '.join(text.split())
    # Truncate to max length
    text = text[:max_length]
    return text
