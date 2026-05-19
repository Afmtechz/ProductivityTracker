"""
Application-wide constants for gamification, priorities, and statuses.
"""

from enum import Enum
from typing import Dict, Tuple


# Task Priority Levels
class TaskPriority(str, Enum):
    """Enum for task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


# Task Status
class TaskStatus(str, Enum):
    """Enum for task status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


# Recurrence Types
class RecurrenceType(str, Enum):
    """Enum for task recurrence patterns."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


# Habit Frequency
class HabitFrequency(str, Enum):
    """Enum for habit tracking frequency."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


# XP Rewards for Actions
XP_REWARDS: Dict[str, int] = {
    "task_completion_low": 30,
    "task_completion_medium": 50,
    "task_completion_high": 75,
    "task_completion_urgent": 100,
    "habit_completion": 30,
    "achievement_unlock": 200,
    "level_up": 500,
    "streak_milestone_7": 100,
    "streak_milestone_30": 300,
    "streak_milestone_100": 1000,
}

# Priority Multipliers for XP
PRIORITY_MULTIPLIERS: Dict[str, float] = {
    TaskPriority.LOW: 0.8,
    TaskPriority.MEDIUM: 1.0,
    TaskPriority.HIGH: 1.5,
    TaskPriority.URGENT: 2.0,
}

# Achievements Definition
ACHIEVEMENTS = {
    "first_steps": {
        "name": "First Steps",
        "description": "Complete your first task",
        "icon": "🎯",
        "requirement": {"type": "total_tasks", "value": 1},
        "xp_reward": 100,
    },
    "task_master": {
        "name": "Task Master",
        "description": "Complete 50 tasks",
        "icon": "👑",
        "requirement": {"type": "total_tasks", "value": 50},
        "xp_reward": 300,
    },
    "productivity_ninja": {
        "name": "Productivity Ninja",
        "description": "Achieve 95% completion rate",
        "icon": "🥷",
        "requirement": {"type": "completion_rate", "value": 95},
        "xp_reward": 250,
    },
    "week_warrior": {
        "name": "Week Warrior",
        "description": "Maintain a 7-day streak",
        "icon": "⚔️",
        "requirement": {"type": "streak_days", "value": 7},
        "xp_reward": 200,
    },
    "habit_master": {
        "name": "Habit Master",
        "description": "Achieve a 30-day streak",
        "icon": "🏆",
        "requirement": {"type": "streak_days", "value": 30},
        "xp_reward": 500,
    },
    "streak_king": {
        "name": "Streak King",
        "description": "Achieve a 100-day streak",
        "icon": "👑",
        "requirement": {"type": "streak_days", "value": 100},
        "xp_reward": 1000,
    },
}

# Level System Configuration
BASE_XP_PER_LEVEL = 1000
XP_SCALING_FACTOR = 1.1  # Each level requires 10% more XP

# Default Categories
DEFAULT_CATEGORIES = [
    "Work",
    "Health",
    "Learning",
    "Personal",
    "Finance",
    "Social",
    "Entertainment",
]

# Color Palette for Habits
HABIT_COLORS = [
    "#FF6B6B",  # Red
    "#4ECDC4",  # Teal
    "#45B7D1",  # Blue
    "#FFA07A",  # Light Salmon
    "#98D8C8",  # Mint
    "#F7DC6F",  # Yellow
    "#BB8FCE",  # Purple
    "#85C1E2",  # Light Blue
]
