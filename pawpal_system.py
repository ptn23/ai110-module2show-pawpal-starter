from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import date


@dataclass
class DailyShow:
	"""Represents a pet care task (previously called DailyShow / Task)."""
	id: int
	name: str
	category: str = "general"
	duration_minutes: int = 0
	priority: int = 0
	recurrence: Optional[str] = None
	last_done: Optional[date] = None
	notes: Optional[str] = None

	def is_due(self) -> bool:
		"""Determine whether the task is due. Stubbed for now."""
		raise NotImplementedError()

	def to_dict(self) -> Dict:
		return {
			"id": self.id,
			"name": self.name,
			"category": self.category,
			"duration_minutes": self.duration_minutes,
			"priority": self.priority,
			"recurrence": self.recurrence,
			"last_done": self.last_done,
			"notes": self.notes,
		}


@dataclass
class Pet:
	id: int
	name: str
	species: str = "dog"
	age_years: int = 0
	preferences: Optional[str] = None
	tasks: List[DailyShow] = field(default_factory=list)

	def add_task(self, task: DailyShow) -> None:
		raise NotImplementedError()

	def edit_task(self, task_id: int, updates: Dict) -> None:
		raise NotImplementedError()

	def remove_task(self, task_id: int) -> None:
		raise NotImplementedError()

	def list_tasks(self) -> List[DailyShow]:
		return list(self.tasks)


class Generator:
	"""Generates schedules based on tasks, constraints and owner preferences."""

	def __init__(self, tasks: Optional[List[DailyShow]] = None, constraints: Optional[Dict] = None):
		self.tasks = tasks or []
		self.constraints = constraints or {}
		self.algorithm_params: Dict = {}

	def score_task(self, task: DailyShow) -> float:
		"""Return a score for a task; higher means more important."""
		raise NotImplementedError()

	def prioritize_tasks(self) -> List[DailyShow]:
		raise NotImplementedError()

	def generate_schedule(self, time_available_minutes: int) -> List[DailyShow]:
		raise NotImplementedError()

	def explain_reasoning(self, schedule: List[DailyShow]) -> str:
		raise NotImplementedError()


class User:
	"""Represents the owner of one or more pets."""

	def __init__(self, name: str, owner_preferences: Optional[Dict] = None, time_available_minutes: int = 0):
		self.name = name
		self.owner_preferences = owner_preferences or {}
		self.time_available_minutes = time_available_minutes
		self.pets: List[Pet] = []

	def enter_info(self, **info) -> None:
		raise NotImplementedError()

	def add_pet(self, pet: Pet) -> None:
		raise NotImplementedError()

	def edit_pet(self, pet_id: int, updates: Dict) -> None:
		raise NotImplementedError()

	def remove_pet(self, pet_id: int) -> None:
		raise NotImplementedError()

	def generate_schedule_for_pet(self, pet_id: int) -> List[DailyShow]:
		raise NotImplementedError()

