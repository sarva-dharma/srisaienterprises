# TaskFlow Studio 2.0 - Enterprise Project & Workflow Suite

A complete, refreshed full-stack project management platform with **Kanban Drag-and-Drop**, **Data Table & Bulk Batch Operations**, **Executive Analytics Dashboard**, **Subtask Checklist Systems**, **Team Assignee Ownership**, and a **Flask REST API & SQLite Backend**.

---

## 🚀 Key Features in TaskFlow Studio 2.0

### 1. Multi-View Management
- 📋 **Kanban Board**: 4 workflow stages (`Backlog / Pending`, `In Progress`, `In Review / QA`, `Completed`). Native HTML5 drag-and-drop card movement across stages, quick navigation arrow buttons (`◀` / `▶`), and column task counters.
- 📑 **Data Table View**: High-density table with column sorting, inline status badges, assignee avatars, subtask progress, and batch selection.
- 📊 **Analytics Dashboard**: Real-time completion velocity meter, stage distribution graphs, priority classification bars, team workload charts, and overdue deadline alerts.

### 2. Task & Workflow Management
- **Subtask / Checklist System**: Add subtasks to any task with live progress percentage indicators on cards (`3/5 done • 60%`).
- **Team Assignee & Ownership**: Assign tasks to team members with color-coded avatar initials (e.g. Alex Chen [AC], Sarah Lin [SL]).
- **Smart Deadline Tracking**: Real-time tags for Overdue, Due Today, Due Tomorrow, and Upcoming.
- **Frictionless Quick-Add Bar**: Rapid single-line task creation by typing and pressing `Enter`.

### 3. Data Portability & Bulk Operations
- **Bulk Actions**: Select multiple tasks in Table View to batch update status or bulk delete.
- **Data Export**: Export tasks to **JSON** or **CSV** in 1 click.
- **Data Import**: Upload and import tasks directly from JSON.
- **Demo Reset**: Re-seed rich realistic demo management data anytime.

### 4. UI Polish & Usability
- **Dark & Light Theme**: Toggle between dark-slate theme and light mode, persisted in `localStorage`.
- **Keyboard Shortcuts**: `/` to focus search, `n` to create a task, `Esc` to close modals and clear selections.

---

## 📁 Project Architecture

```text
website 2.01/
├── app.py                 # Flask server, SQLite schema, 4-stage REST API, export/import
├── requirements.txt       # Dependencies (Flask, Flask-SQLAlchemy)
├── run.bat                # 1-click Windows launcher
├── README.md              # Project documentation
├── test_api.py            # Automated test suite (10/10 tests)
├── templates/
│   └── index.html         # Modern SPA (Kanban Board, Data Table, Analytics, Modals)
└── static/
    ├── css/
    │   └── style.css      # Design system with Dark/Light theme CSS variables, grid, drag styles
    └── js/
        └── app.js         # Client controller (views, drag-and-drop, checklists, bulk actions)
```

---

## 💻 Getting Started

### Quickest Launch (Windows)
Double-click `run.bat` in the project root folder.

### Command Line Launch
```powershell
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

---

## 🧪 Automated Testing
Run the test suite:
```powershell
python test_api.py
```
All 10 tests verify end-to-end API functionality across CRUD, bulk operations, checklists, and analytics.
