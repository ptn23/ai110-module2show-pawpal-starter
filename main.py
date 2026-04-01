import pawpal_system

# Create a user and two pets
user = pawpal_system.User("Phuong")
pet1 = pawpal_system.Pet(1, "Waffle", "Guinea Pig", 10)
pet2 = pawpal_system.Pet(2, "Ginger", "Cat", 10)
user.add_pet(pet1)
user.add_pet(pet2)

# Add tasks OUT OF ORDER for pet1 (times are intentionally scrambled)
pet1.add_task(pawpal_system.Task(1, "Midday Check", "12:00", "general", 15, 1))
pet1.add_task(pawpal_system.Task(2, "Morning Snack", "07:15", "feeding", 10, 1, "daily"))
pet1.add_task(pawpal_system.Task(3, "Evening Play", "19:30", "play", 30, 1))

# Add tasks for pet2 also out of order
pet2.add_task(pawpal_system.Task(1, "Nap Time", "14:00", "rest", 60, 1))
pet2.add_task(pawpal_system.Task(2, "Breakfast", "08:00", "feeding", 20, 1))
pet2.add_task(pawpal_system.Task(3, "Grooming", "09:30", "care", 25, 1))

# Add a conflicting task at the same time as pet1's Morning Snack (07:15)
pet2.add_task(pawpal_system.Task(4, "Visitor Breakfast", "07:15", "feeding", 5, 1))

# Use Scheduler.sort_by_time to get ordered lists
sched1 = pawpal_system.Scheduler(pet=pet1)
sorted_pet1 = sched1.sort_by_time()
print("Sorted tasks for pet1 by time:")
for t in sorted_pet1:
    print(f"- {t.name} at {t.starting_time}")

sched2 = pawpal_system.Scheduler(pet=pet2)
sorted_pet2 = sched2.sort_by_time()
print("\nSorted tasks for pet2 by time:")
for t in sorted_pet2:
    print(f"- {t.name} at {t.starting_time}")

# Mark one task complete and demonstrate filtering
# Use Scheduler.mark_task_complete so recurring tasks create the next instance
new_task = sched1.mark_task_complete(2)
if new_task is not None:
    print(f"\nCreated next recurring task: {new_task.name} (id={new_task.id}) with last_done={new_task.last_done}")

print("\nAll completed tasks across user:")
for t in user.filter_tasks(completed=True):
    print(f"- {t.name} (pet task id={t.id}) at {t.starting_time}")

print("\nAll tasks for pet named 'Waffle':")
for t in user.filter_tasks(pet_name="Waffle"):
    print(f"- {t.name} at {t.starting_time} (completed={t.completed})")

# Detect conflicts across pets and print warnings (lightweight)
warnings = sched1.detect_time_conflicts(pets=[pet1, pet2])
if warnings:
    print("\nWarnings:")
    for w in warnings:
        print("- ", w)
else:
    print("\nNo time conflicts detected.")