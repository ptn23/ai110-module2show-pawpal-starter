import streamlit as st
from pawpal_system import User
from pawpal_system import Task
from pawpal_system import Pet
from pawpal_system import Scheduler
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
time_available = st.number_input("Owner time available (minutes)", min_value=0, max_value=1440, value=60)

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# initialize or update owner in session state
if "owner" not in st.session_state:
    st.session_state.owner = User(name=owner_name, owner_preferences={}, time_available_minutes=time_available)
else:
    # keep owner object but update editable fields
    st.session_state.owner.name = owner_name
    st.session_state.owner.time_available_minutes = time_available

owner = st.session_state.owner

# id counters
if "next_pet_id" not in st.session_state:
    st.session_state.next_pet_id = 1
if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = 1

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

# Add pet button
col_pet1, col_pet2 = st.columns(2)
with col_pet1:
    if st.button("Add pet"):
        pet = Pet(id=st.session_state.next_pet_id, name=pet_name, species=species, age_years=0)
        owner.add_pet(pet)
        st.session_state.next_pet_id += 1
        st.success(f"Added pet: {pet.name}")

with col_pet2:
    if st.button("Add task"):
        # ensure there's at least one pet to attach to
        if not owner.pets:
            pet = Pet(id=st.session_state.next_pet_id, name=pet_name, species=species, age_years=0)
            owner.add_pet(pet)
            st.session_state.next_pet_id += 1
        else:
            pet = owner.pets[0]

        priority_map = {"low": 1, "medium": 5, "high": 10}
        pval = priority_map.get(priority, 5)
        t = Task(id=st.session_state.next_task_id, name=task_title, starting_time="", duration_minutes=int(duration), priority=pval)
        pet.add_task(t)
        st.session_state.next_task_id += 1
        st.success(f"Added task '{t.name}' to pet {pet.name}")

if owner.pets:
    for pet in owner.pets:
        st.write(f"Tasks for {pet.name}:")
        rows = [task.to_dict() for task in pet.list_tasks()]
        if rows:
            st.table(rows)
        else:
            st.info("No tasks for this pet yet.")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if not owner.pets:
        st.warning("No pets to schedule for. Add a pet first.")
    else:
        pet = owner.pets[0]
        schedule = owner.generate_schedule_for_pet(pet.id)
        if not schedule:
            st.info("No tasks could be scheduled with the available time.")
        else:
            rows = []
            for si in schedule:
                rows.append({
                    "task": si.task.name,
                    "start_minute": si.start_minute,
                    "end_minute": si.end_minute,
                    "priority": si.task.priority,
                })
            st.write("Schedule:")
            st.table(rows)
            gen = Scheduler(pet=pet, user_prefs=owner.owner_preferences)
            st.markdown(gen.explain_reasoning(schedule))
