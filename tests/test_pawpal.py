import pytest
from datetime import date

from pawpal_system import Task, Pet


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
