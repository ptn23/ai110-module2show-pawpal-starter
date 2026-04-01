import pytest
from datetime import date

from pawpal_system import Task, Pet, Scheduler, ScheduledItem


def test_task_mark_complete_sets_last_done_and_completed():
    t = Task(id=1, name="Feed", starting_time="08:00", duration_minutes=10)
    assert not t.completed
    assert t.last_done is None

    today = date.today()
    t.mark_complete(done_date=today)

    assert t.completed is True
    assert t.last_done == today


def test_adding_task_increases_pet_task_count():
    pet = Pet(id=1, name="Fido", species="dog", age_years=3)
    assert len(pet.list_tasks()) == 0

    t = Task(id=2, name="Walk", starting_time="09:00", duration_minutes=30)
    pet.add_task(t)

    assert len(pet.list_tasks()) == 1
    assert pet.list_tasks()[0].id == 2


def test_sorting_tasks_by_time():
    pet = Pet(id=10, name="Spot", species="cat", age_years=2)
    t1 = Task(id=1, name="Medicate", starting_time="09:00", duration_minutes=10)
    t2 = Task(id=2, name="Walk", starting_time="08:30", duration_minutes=20)
    t3 = Task(id=3, name="Groom", starting_time="11:15", duration_minutes=15)

    pet.add_task(t1)
    pet.add_task(t2)
    pet.add_task(t3)

    sched = Scheduler(pet=pet)
    sorted_tasks = sched.sort_by_time()
    assert [t.id for t in sorted_tasks] == [2, 1, 3]


def test_marking_daily_task_creates_next_occurrence():
    pet = Pet(id=11, name="Luna", species="dog", age_years=4)
    t = Task(id=1, name="Feed", starting_time="08:00", duration_minutes=10, recurrence="daily")
    pet.add_task(t)

    sched = Scheduler(pet=pet)
    new_task = sched.mark_task_complete(1, done_date=date.today())

    # Should have created a new recurring task and returned it
    assert new_task is not None
    assert new_task.recurrence == "daily"
    # The scheduler sets last_done on the new task to today so it's not due again until tomorrow
    assert new_task.last_done == date.today()
    # Original task should be marked completed
    orig = pet.get_task(1)
    assert orig.completed is True
    assert orig.last_done == date.today()
    # New task should be present in the pet's task list
    assert any(t.id == new_task.id for t in pet.tasks)
    # And the newly-created task should not be due today
    assert new_task.is_due() is False


def test_scheduler_conflict_detection():
    # Overlapping scheduled items should be flagged as conflict (same_schedule -> False)
    s_task1 = Task(id=100, name="A", starting_time="07:00", duration_minutes=60)
    s_task2 = Task(id=101, name="B", starting_time="07:30", duration_minutes=60)

    si1 = ScheduledItem(task=s_task1, start_minute=60, end_minute=120)
    si2 = ScheduledItem(task=s_task2, start_minute=90, end_minute=150)

    sched = Scheduler()
    assert sched.same_schedule(si1, si2) is False

    # Non-overlapping should return True
    si3 = ScheduledItem(task=s_task2, start_minute=120, end_minute=180)
    assert sched.same_schedule(si1, si3) is True
