# Timely — School Timetable System

A multi-tenant web application that lets a school register, set up its grades, streams,
teachers, subjects, and constraints, then automatically generates a conflict-free weekly
timetable using a constraint solver — no manual scheduling required.

Each school's data is fully isolated from every other school using the system. A school
signs up, sets up its own structure, and generates its own timetable independently.

---

## How it works, end to end

1. A school **signs up** with a generated school ID, email, and password.
2. The school defines its **grades and streams** (e.g. Form 1 → 1A, 1B, 1C).
3. The school adds its **teachers**.
4. The school adds **subjects**, tags any that need a shared resource (e.g. Chemistry
   needs the Chemistry Lab), and sets **lesson requirements** per subject per grade
   (lessons/week, doubles/week, max lessons/day) — then assigns which teacher covers
   each subject for which specific stream.
5. If a grade splits into parallel elective groups (e.g. some students take Biology
   while others take Physics, at the same time), the school sets that up as an
   **elective split**.
6. The school adds any **teacher availability rules** (e.g. "Mr. Maina is unavailable
   Tuesday afternoons") and defines the **weekly period structure** (what time each
   lesson/break starts and ends).
7. The school clicks **Generate**, and the solver produces a complete, conflict-free
   timetable for the whole school in one pass — viewable by class, by teacher, or as
   a whole-school schedule.

---

## Tech stack

- **Backend:** Python, Flask
- **Database:** MySQL, accessed via SQLAlchemy
- **Solver:** [Google OR-Tools](https://developers.google.com/optimization) (CP-SAT) —
  a constraint programming solver, not AI/ML. Scheduling is a classic constraint
  satisfaction problem; CP-SAT finds a timetable that satisfies every rule
  simultaneously, far faster than hand-rolled search.
- **Frontend:** Plain HTML, CSS, and JavaScript — no framework. Pages call the backend
  directly via `fetch`.
- **Auth:** Email/password with hashed passwords (`werkzeug.security`) and
  cookie-based sessions (`flask.session`).

---

## Architecture

The backend follows a strict layered structure — each layer only talks to the layer
directly below it:

```
routes/        → thin controllers: parse the request, call a service, return JSON
services/      → business rules and validation
repositories/  → all direct database access lives here, nowhere else
models/        → SQLAlchemy table definitions only, no logic
solver/        → fully isolated constraint-solving engine (no Flask, no database)
  ├─ structs.py       → plain data containers the solver works with
  ├─ engine.py         → the CP-SAT model and solve logic
  └─ adapters/
      ├─ input_builder.py   → database models → solver structs
      └─ output_writer.py   → solver result → database rows
```

The solver never imports anything from `models/`, `repositories/`, or `services/` —
only the two adapter files know how to translate between the solver's world and the
database's world. This keeps the solver testable on its own, with plain data, no
database required.

---

## Database schema (high level)

- `schools`, `term` — one school, one or more terms
- `grade`, `streams` — grades (e.g. Form 1) and their streams (e.g. 1A, 1B)
- `teachers`, `teacherconstraint` — teachers and their availability rules
- `subjects`, `subjectrequirement` — subjects and how often each must appear, per grade
- `resources` — shared spaces with limited capacity (e.g. one Chemistry Lab)
- `optionblock`, `optiongroup` — elective splits within a grade
- `teacherassignment` — who teaches what, to which stream or elective group
- `period` — the daily time structure (repeats Monday–Friday)
- `timetableentry` — the generated output

---

## Hard constraints the solver enforces

These are non-negotiable — the generated timetable can never violate any of them:

1. A teacher is never double-booked at the same time.
2. A shared resource (e.g. a lab) never serves more classes than its capacity at once.
3. All subjects in the same elective split land in the exact same time slot.
4. Every subject gets exactly its required number of lessons per week — no more, no less.
5. A double lesson occupies two consecutive periods, same day, same class.
6. A subject never exceeds its max lessons per day.
7. A teacher is never scheduled during a time they've marked unavailable.

> **Known gap:** a teacher's *max consecutive lessons* rule (e.g. "never more than 4
> periods in a row") is stored and validated at data-entry time, but is **not yet
> enforced by the solver itself** — the CP-SAT rewrite deferred this constraint. It
> needs sliding-window overlap constraints added to `engine.py`.

Soft/preference constraints (e.g. "this teacher prefers mornings") are intentionally
not implemented yet — the system currently only supports hard constraints.

---

## Setup

### Backend

```bash
cd Backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
pip install ortools --no-cache-dir
```

Create a `.env` file in `Backend/` (see `.env.example` for the full list):

```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=masterscheduler
SECRET_KEY=generate-your-own-random-string
FRONTEND_ORIGINS=http://127.0.0.1:5500,http://localhost:5500
```

Then set up the database:

```bash
flask db init        # once
flask db migrate -m "initial models"
flask db upgrade
python main.py
```

The API runs at `http://127.0.0.1:5000`.

### Frontend

The frontend is a set of static HTML files — no build step. Serve the `Frontend/`
folder with any static file server (e.g. VS Code's Live Server extension) and open
`signup.html` to get started. Update `API_BASE` in `common.js` if your backend runs
somewhere other than `http://localhost:5000`.

---

## Project structure

```
Backend/
├── main.py
├── config.py
├── .env
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── routes/
│   └── solver/
│       ├── structs.py
│       ├── engine.py
│       └── adapters/

Frontend/
├── login.html / signup.html / style.css
├── dashboard.html / dashboard.css
├── forms-classes.html / forms-classes.css
├── teachers.html / teachers.css
├── subjects.html / subjects.css
├── option-blocks.html / option-blocks.css
├── constraints.html / constraints.css
├── periods.html / periods.css
├── generate.html / generate.css
├── layout.css       (shared sidebar/card shell used by every setup page)
└── common.js         (shared API base, error helpers, auth check)
```

---

## Known limitations

- **No soft/preference constraints** — only hard rules are enforced (deferred by design).
- **Teacher max-consecutive-lessons** is not yet enforced by the solver (see above).
- **No confirmation prompts** on some destructive actions — deleting a teacher,
  subject, or option block cascades and removes everything tied to it immediately.
- **Generic failure messages in places** — a few solver failure cases don't yet point
  to the exact subject/teacher/constraint responsible.
- **No cascading warning UI** — the backend cleans up dependent data correctly, but
  the frontend doesn't always warn the user what's about to be deleted first.
