# Homework Hub Database Setup

This project provides a PostgreSQL database setup script for the **Homework Hub** application. The database is named `homework_hub` and supports managing student assignments, reminders, and study sessions.

## Features

- Creates the `homework_hub` database.
- Defines the schema with tables for:
  - Students
  - Assignments
  - Reminders
  - Study Sessions
- Includes default configurations to streamline setup.

---

## Prerequisites

Before running the script, ensure the following:

- **Python 3** is installed.
- **PostgreSQL** is installed and running.
- You have administrative access to PostgreSQL.

---

## Usage

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/homework-hub-db.git
cd homework-hub-db
```

### Step 2: Install Dependencies

Install the Python dependencies using `pip`:

```bash
pip install psycopg2
```

### Step 3: Run the Database Creation Script

Execute the `create_homework_hub_db.py` script to create the `homework_hub` database:

```bash
python create_homework_hub_db.py
```

### Step 4: Follow Prompts

The script will prompt for the PostgreSQL password for the default `postgres` user:

```
Enter the PostgreSQL password for user 'postgres': your_password
```

### Step 5: Run the Homework Hub Script

Execute the `LhhCode.py` to use the program to track your homework, study sessions and reminders:

```bash
python LhhCode.py
```
---

## Database Schema

The `homework_hub` database includes the following tables:

### `student`
| Column        | Type        | Description                      |
|---------------|-------------|----------------------------------|
| `student_id`  | `SERIAL`    | Primary key                      |
| `full_name`   | `VARCHAR(100)` | Full name of the student          |
| `email`       | `VARCHAR(100)` | Email address (unique identifier) |

### `assignment`
| Column          | Type        | Description                          |
|------------------|-------------|--------------------------------------|
| `assignment_id`  | `SERIAL`    | Primary key                          |
| `task_name`      | `VARCHAR(255)` | Name of the assignment               |
| `due_date`       | `DATE`      | Due date of the assignment           |
| `subject`        | `VARCHAR(100)` | Subject associated with the assignment |
| `priority_level` | `INT`       | Priority level (1-5)                 |
| `student_id`     | `INT`       | Foreign key referencing `student_id` |

### `reminder`
| Column        | Type        | Description                            |
|---------------|-------------|----------------------------------------|
| `reminder_id` | `SERIAL`    | Primary key                            |
| `date`        | `DATE`      | Date of the reminder                   |
| `assignment_id` | `INT`     | Foreign key referencing `assignment_id`|

### `study_session`
| Column        | Type          | Description                          |
|---------------|---------------|--------------------------------------|
| `session_id`  | `SERIAL`      | Primary key                          |
| `start_time`  | `TIMESTAMP`   | Start time of the study session      |
| `end_time`    | `TIMESTAMP`   | End time of the study session        |
| `notes`       | `TEXT`        | Notes about the study session        |
| `subject`     | `VARCHAR(100)` | Subject associated with the session |

---

## Example Output

### When the Database is Created:
```bash
Database 'homework_hub' created successfully.
```

### If the Database Already Exists:
```bash
Database 'homework_hub' already exists.
```

---

## Troubleshooting

- **Error: `could not connect to server`**
  - Ensure PostgreSQL is running and accessible at `localhost:5432`.

- **Error: `FATAL: password authentication failed for user "postgres"`**
  - Check the entered password. Ensure it matches the PostgreSQL configuration.

- **Error: `psycopg2.errors.DuplicateDatabase`**
  - The database already exists. You can connect to it directly.
