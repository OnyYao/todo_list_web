# CMU Todo – Multiuser TODO List Web App

A multiuser TODO list web app built with Django and JavaScript for CMU students to track class tasks and due dates.

## User Stories

1. **As an student at CMU**, I want to write down a list of tasks I have to do for my classes with due dates for each so that I don't forget what my teachers have assigned me to do.

2. **As a busy college student**, I want to be reminded every morning about the things I need to finish that day so that I can plan how to get my tasks done throughout the day.

## Features

- **User accounts**: Sign up, log in, and log out. Each user has their own tasks.
- **Tasks with due dates**: Add tasks with title, description, due date, and course (e.g., 15-213).
- **Today's tasks**: A prominent "Good morning" section shows tasks due today when you log in.
- **Morning email reminders**: A management command sends daily email reminders for tasks due today (run via cron).

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:

   ```bash
   python manage.py migrate
   ```

4. Create a superuser (optional, for admin):

   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

   If you get `ModuleNotFoundError: No module named 'django'` after activating the venv, use the venv's Python explicitly:

   ```bash
   ./venv/bin/python manage.py runserver
   ```

6. Open http://127.0.0.1:8000/ in your browser.

## Morning Reminders

To send daily email reminders for tasks due today:

1. Configure email in `todo_project/settings.py` (e.g., SMTP for production).
2. Run the command every morning (e.g., via cron at 7:00 AM):

   ```bash
   python manage.py send_morning_reminders
   ```

   To test without sending emails:

   ```bash
   python manage.py send_morning_reminders --dry-run
   ```

   In development, emails are printed to the console by default.

## Tech Stack

- **Backend**: Django 5
- **Frontend**: Vanilla JavaScript, CSS
- **Database**: SQLite (default)

## Approved PRs

The list below is updated automatically when a pull request is merged into the default branch.

- AvalonMei 2026-03-24 Add task editing functionality and improve form styling
- OnyYao 2026-03-24 Update: update the readme.md
