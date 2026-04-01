# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

Main goals: enter information, add/edit tasks, generate daily schedule, display plan + reasoning, include tests for scheduling reason

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).

# Smarter Scheduling

This project now includes advanced scheduling features:

- **Recurring Task Automation:** When a daily or weekly task is marked complete, a new instance is automatically created for the next occurrence, using Python's `timedelta` for accurate due dates.
- **Time Conflict Detection:** The scheduler can detect if two tasks (for the same or different pets) are scheduled at the same time, returning a warning message instead of crashing.
- **Flexible Filtering:** Tasks can be filtered by completion status or pet name, making it easy to view and manage schedules.
- **Robust Sorting:** Tasks are sorted by their `starting_time` using a lambda function for correct chronological order.

These features make PawPal+ more robust and user-friendly for busy pet owners managing complex schedules.

# Testing PawPal+
python -m pytest: collected 5 items, assess add user/pets, sort by time, mark complete with recurrence, filter tasks, detect conflicts
Confidence level: 3-4 stars