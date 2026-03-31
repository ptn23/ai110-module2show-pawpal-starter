import pawpal_system
user = pawpal_system.User("Phuong")
pet1 = pawpal_system.Pet(1,"Waffle","Guinea Pig", 10)
pet2 = pawpal_system.Pet(2, "Ginger","Cat", 10)
user.add_pet(pet1)
user.add_pet(pet2)
task1_pet1 = pawpal_system.Task(1, "Eating", "07:30", "general", 30, 1)
task2_pet1 = pawpal_system.Task(2, "Showering", "08:30", "general", 30, 1)
task3_pet1 = pawpal_system.Task(3, "Walking", "11:30", "general", 60, 1)

task1_pet2 = pawpal_system.Task(1, "Sunbathing", "07:30", "general", 160, 1)
task2_pet2 = pawpal_system.Task(2, "Eating", "11:30", "general", 30, 1)
task3_pet2 = pawpal_system.Task(3, "Playing", "14:30", "general", 30, 1)

pet1.add_task(task1_pet1)
pet1.add_task(task2_pet1)
pet1.add_task(task3_pet1)

pet2.add_task(task1_pet2)
pet2.add_task(task2_pet2)
pet2.add_task(task3_pet2)

for i in range(1,4):
    n = pet1.get_task(i)
    print(f"Today's schedule for pet1: {n.name, n.starting_time, n.category, n.duration_minutes, n.priority, n.recurrence, n.last_done, n.notes}")
for i in range(1,4):
    n = pet2.get_task(i)
    print(f"Today's schedule for pet2: {n.name, n.starting_time, n.category, n.duration_minutes, n.priority, n.recurrence, n.last_done, n.notes}")