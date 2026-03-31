from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import date, timedelta


@dataclass
class Task:
	"""Represents a pet care task."""
	id: int
	name: str
	starting_time: str
	category: str = "general"
	duration_minutes: int = 0
	priority: int = 0
	recurrence: Optional[str] = None
	last_done: Optional[date] = None
	notes: Optional[str] = None
	completed: bool = False

	def is_due(self) -> bool:
		"""Return True when the task should be considered due."""
		if self.last_done is None:
			return True
		if self.recurrence == "daily":
			return self.last_done < date.today()
		if self.recurrence == "weekly":
			return (date.today() - self.last_done) >= timedelta(days=7)
		return False

	def to_dict(self) -> Dict[str, Any]:
		"""Serialize the task to a dictionary."""
		return {
			"id": self.id,
			"name": self.name,
			"starting_time": self.starting_time,
			"category": self.category,
			"duration_minutes": self.duration_minutes,
			"priority": self.priority,
			"recurrence": self.recurrence,
			"last_done": self.last_done,
			"notes": self.notes,
		}

	def mark_complete(self, done_date: Optional[date] = None) -> None:
		"""Mark the task completed and set its last_done date."""
		self.completed = True
		self.last_done = done_date or date.today()


@dataclass
class ScheduledItem:
	task: Task
	start_minute: Optional[int] = None
	end_minute: Optional[int] = None


@dataclass
class Pet:
	def __init__(self, id, name, species, age_years, preferences=None, tasks=None):
		self.id = id
		self.name = name
		self.species = species
		self.age_years = age_years
		
		self.preferences = preferences if preferences is not None else []
		self.tasks = tasks if tasks is not None else []
		
	def get_task(self, task_id: int) -> Optional[Task]:
		for t in self.tasks:
			"""Return the task with the given id, or None if missing."""
			if t.id == task_id:
				return t
		return None
	def add_task(self, task):
		"""Add a task to the pet's task list (raises on duplicate)."""
		if task is None:
			print("DEBUG: Warning! You are trying to add None to the task list.")
			return
		if self.get_task(task.id) is not None:
			raise ValueError(f"Task with id {task.id} already exists...")
		self.tasks.append(task)
		ids = [t.id for t in self.tasks if t is not None]
		print(f"Successfully added. Current list IDs: {ids}")

	def edit_task(self, task_id: int, updates: Dict[str, Any]) -> None:
		"""Apply updates to a task's attributes by id."""
		t = self.get_task(task_id)
		if t is None:
			raise KeyError(f"Task {task_id} not found")
		for k, v in updates.items():
			if hasattr(t, k):
				setattr(t, k, v)

	def remove_task(self, task_id: int) -> None:
		"""Remove a task by id (raises if not found)."""
		t = self.get_task(task_id)
		if t is None:
			raise KeyError(f"Task {task_id} not found")
		self.tasks.remove(t)

	def list_tasks(self) -> List[Task]:
		"""Return a shallow copy list of this pet's tasks."""
		return list(self.tasks)


class Scheduler:
	"""Generates schedules based on tasks, constraints and owner preferences.

	Implements a deterministic greedy scheduler that:
	- filters due tasks
	- scores tasks once and caches the score
	- sorts by score (desc) then id
	- assigns start/end minutes cumulatively from 0
	"""

	def __init__(self, pet: Optional[Pet] = None, user_prefs: Optional[Dict] = None, constraints: Optional[Dict] = None):
		self.pet = pet
		self.user_prefs = user_prefs or {}
		self.constraints = constraints or {}
		self.algorithm_params: Dict[str, Any] = {}
		self._score_cache: Dict[int, float] = {}

	def score_task(self, task: Task) -> float:
		"""Compute a deterministic score for a task (higher is better)."""
		if task.id in self._score_cache:
			return self._score_cache[task.id]
		score = float(task.priority) * 10.0 - (task.duration_minutes / 10.0)
		self._score_cache[task.id] = score
		return score

	def prioritize_tasks(self) -> List[Task]:
		"""Return due tasks sorted by score (descending) and id for determinism."""
		if not self.pet:
			return []
		scored = [(self.score_task(t), t) for t in self.pet.tasks if t.is_due()]
		# sort by score desc, then by id to be deterministic
		scored.sort(key=lambda si: (-si[0], si[1].id))
		return [t for _, t in scored]

	def generate_schedule(self, time_available_minutes: int) -> List[ScheduledItem]:
		"""Greedy scheduler: pick highest-scoring due tasks until time is exhausted."""
		schedule: List[ScheduledItem] = []
		remaining = time_available_minutes
		cursor = 0
		for task in self.prioritize_tasks():
			if task.duration_minutes <= 0:
				continue
			if task.duration_minutes <= remaining:
				si = ScheduledItem(task=task, start_minute=cursor, end_minute=cursor + task.duration_minutes)
				schedule.append(si)
				cursor += task.duration_minutes
				remaining -= task.duration_minutes
			if remaining <= 0:
				break
		return schedule

	def explain_reasoning(self, schedule: List[ScheduledItem]) -> str:
		"""Return a short explanation describing why tasks were selected."""
		lines = [f"Selected {si.task.name} (priority={si.task.priority}, duration={si.task.duration_minutes}min)" for si in schedule]
		if not lines:
			return "No tasks could be scheduled with the available time."
		return "; ".join(lines)


class User:
	"""Represents the owner of one or more pets."""

	def __init__(self, name: str, owner_preferences: Optional[Dict] = None, time_available_minutes: int = 0):
		self.name = name
		self.owner_preferences = owner_preferences or {}
		self.time_available_minutes = time_available_minutes
		self.pets: List[Pet] = []

	def get_pet(self, pet_id: int) -> Optional[Pet]:
		"""Return the pet with the given id, or None if missing."""
		return next((p for p in self.pets if p.id == pet_id), None)

	def enter_info(self, **info) -> None:
		"""Update user attributes from provided keyword arguments."""
		for k, v in info.items():
			setattr(self, k, v)

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to the user's collection (raises on duplicate)."""
		if self.get_pet(pet.id) is not None:
			raise ValueError(f"Pet with id {pet.id} already exists")
		self.pets.append(pet)

	def edit_pet(self, pet_id: int, updates: Dict[str, Any]) -> None:
		"""Apply attribute updates to a pet identified by id."""
		p = self.get_pet(pet_id)
		if p is None:
			raise KeyError(f"Pet {pet_id} not found")
		for k, v in updates.items():
			if hasattr(p, k):
				setattr(p, k, v)

	def remove_pet(self, pet_id: int) -> None:
		"""Remove a pet by id (raises if not found)."""
		p = self.get_pet(pet_id)
		if p is None:
			raise KeyError(f"Pet {pet_id} not found")
		self.pets.remove(p)

	def generate_schedule_for_pet(self, pet_id: int) -> List[ScheduledItem]:
		"""Generate a schedule for a specific pet using this user's time constraint."""
		p = self.get_pet(pet_id)
		if p is None:
			raise KeyError(f"Pet {pet_id} not found")
		gen = Scheduler(pet=p, user_prefs=self.owner_preferences)
		return gen.generate_schedule(self.time_available_minutes)


