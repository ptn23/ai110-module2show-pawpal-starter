# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

Initial: User -> Pet -> DailyShow, Generator on the side (same tier as User)

- What classes did you include, and what responsibilities did you assign to each?
    - User: enter information, add/edit tasks, button that makes the "machine" generate schedule
    - Generator: helps considering what tasks is more relevant, generate schedule
    - Pet: general information of pet, their preferences, the tasks they do
    - DailyShow: the details of the tasks the pets do

**b. Design changes**

- Did your design change during implementation?
Yes
- If yes, describe at least one change and why you made it.
Added CRUD: Retrieve and establish connection between User, Pet, and Generator classes
Added is_due to check when is the task is considered due.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
Time, priority, preferences
- How did you decide which constraints mattered most?
Time, because it's often the main reason why people need these apps to begin with
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
More Pythonic code
- Why is that tradeoff reasonable for this scenario?
Better, more detailed code

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
Debugging and factoring, mostly what the tasks ask. Most helpful: streamlit

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
In section 4 when there's the extend your Scheduler to detect if two tasks for the same pet (or different pets) are scheduled at the same time. AI suggest a significantly longer and unnecessarily hard code, while all we need to do is compare animals and their begin/end time in tasks.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

add user/pets, sort by time, mark complete with recurrence, filter tasks, detect conflicts because they are the main functions

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Mostly. I would want to add edge cases if different animals can have something similar to a break time in which no actions/tasks can be added

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
Getting everything correctly installed and done

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
Improve: I found bugs in my streamlit app

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
You have to have a solid grip of code and what they do, as AI is prone to hallucination.

 <a href="/ai110-week5/ai110-module2show-pawpal-starter/rand.png" target="_blank"><img src='/ai110-week5/ai110-module2show-pawpal-starter/rand.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.
