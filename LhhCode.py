from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app and configure PostgreSQL database
# put your postgres password wher <PASSWORD> is
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:<PASSWORD>@localhost:5432/homework_hub'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define database models
class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Assignment(db.Model):
    __tablename__ = 'assignment'
    assignment_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    priority_level = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)

class Reminder(db.Model):
    __tablename__ = 'reminder'
    reminder_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.assignment_id'), nullable=False)

class StudySession(db.Model):
    __tablename__ = 'study_session'
    session_id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    subject = db.Column(db.String(100), nullable=False)

# Command-line menu
def menu(student_id):
    while True:
        print("\n=== Local Homework Hub Menu ===")
        print("1. Add Assignment")
        print("2. Add Reminder")
        print("3. Log Study Session")
        print("4. View Assignments")
        print("5. View Reminders")
        print("6. View Study Sessions")
        print("7. Delete Item")
        print("8. Edit Assignment")
        print("9. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_assignment(student_id)
        elif choice == '2':
            add_reminder()
        elif choice == '3':
            log_study_session()
        elif choice == '4':
            view_assignments(student_id)
        elif choice == '5':
            view_reminders(student_id)
        elif choice == '6':
            view_study_sessions()
        elif choice == '7':
            delete_item(student_id)
        elif choice == '8':
            edit_assignment(student_id)
        elif choice == '9':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


def initialize_student():
    print("Welcome to the Local Homework Hub!")
    email = input("Enter your email: ")
    
    # Check if the student exists
    existing_student = Student.query.filter_by(email=email).first()
    if existing_student:
        print(f"Welcome back, {existing_student.full_name}! Your student ID is {existing_student.student_id}.")
        return existing_student.student_id
    else:
        # Create a new student
        name = input("Enter your full name: ")
        try:
            student = Student(full_name=name, email=email)
            db.session.add(student)
            db.session.commit()
            print(f"Welcome, {name}! Your student ID is {student.student_id}.")
            return student.student_id
        except Exception as e:
            print(f"Error initializing student: {e}")
            return None

def add_assignment(student_id):
    task_name = input("Enter task name: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    subject = input("Enter subject: ")
    priority = int(input("Enter priority level (1-5): "))
    try:
        assignment = Assignment(
            task_name=task_name,
            due_date=datetime.strptime(due_date, '%Y-%m-%d'),
            subject=subject,
            priority_level=priority,
            student_id=student_id
        )
        db.session.add(assignment)
        db.session.commit()
        print(f"Assignment '{task_name}' added successfully!")
    except Exception as e:
        print(f"Error adding assignment: {e}")

def add_reminder():
    assignment_id = int(input("Enter assignment ID: "))
    reminder_date = input("Enter reminder date (YYYY-MM-DD): ")
    try:
        reminder = Reminder(
            date=datetime.strptime(reminder_date, '%Y-%m-%d'),
            assignment_id=assignment_id
        )
        db.session.add(reminder)
        db.session.commit()
        print("Reminder added successfully!")
    except Exception as e:
        print(f"Error adding reminder: {e}")

def log_study_session():
    subject = input("Enter subject: ")
    start_time = input("Enter start time (YYYY-MM-DD HH:MM:SS): ")
    end_time = input("Enter end time (YYYY-MM-DD HH:MM:SS): ")
    notes = input("Enter notes (optional): ")
    try:
        study_session = StudySession(
            start_time=datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S'),
            end_time=datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S'),
            notes=notes,
            subject=subject
        )
        db.session.add(study_session)
        db.session.commit()
        print("Study session logged successfully!")
    except Exception as e:
        print(f"Error logging study session: {e}")

def view_assignments(student_id):
    try:
        assignments = Assignment.query.filter_by(student_id=student_id).order_by(Assignment.due_date).all()
        if assignments:
            print("\nAssignments:")
            for a in assignments:
                print(f"- {a.task_name} | Due: {a.due_date} | Subject: {a.subject} | Priority: {a.priority_level}")
        else:
            print("No assignments found.")
    except Exception as e:
        print(f"Error viewing assignments: {e}")
        
def view_reminders(student_id):
    try:
        reminders = db.session.query(Reminder, Assignment).join(Assignment).filter(Assignment.student_id == student_id).all()
        if reminders:
            print("\nReminders:")
            for reminder, assignment in reminders:
                print(f"- Reminder for '{assignment.task_name}' | Date: {reminder.date}")
        else:
            print("No reminders found.")
    except Exception as e:
        print(f"Error viewing reminders: {e}")
        
def view_study_sessions():
    try:
        study_sessions = StudySession.query.all()
        if study_sessions:
            print("\nStudy Sessions:")
            for session in study_sessions:
                print(f"- Subject: {session.subject} | Start: {session.start_time} | End: {session.end_time} | Notes: {session.notes}")
        else:
            print("No study sessions found.")
    except Exception as e:
        print(f"Error viewing study sessions: {e}")
        
def delete_item(student_id):
    print("\nWhat would you like to delete?")
    print("1. Assignment")
    print("2. Reminder")
    print("3. Study Session")
    print("4. Return to Main Menu")
    item_choice = input("Enter your choice: ")

    if item_choice == '1':
        list_assignments(student_id)
        print("Or enter 0 to exit")
        assignment_id = int(input("Enter the Assignment ID to delete: "))
        delete_assignment(assignment_id, student_id)
    elif item_choice == '2':
        list_reminders()
        print("Or enter 0 to exit")
        reminder_id = int(input("Enter the Reminder ID to delete: "))
        delete_reminder(reminder_id)
    elif item_choice == '3':
        list_study_sessions()
        print("Or enter 0 to exit")
        session_id = int(input("Enter the Study Session ID to delete: "))
        delete_study_session(session_id)
    else:
        print("Invalid choice. Returning to the main menu.")


def list_assignments(student_id):
    print("\nYour Assignments:")
    assignments = Assignment.query.filter_by(student_id=student_id).all()
    if assignments:
        for assignment in assignments:
            print(f"ID: {assignment.assignment_id} | Task: {assignment.task_name} | Due Date: {assignment.due_date} | Subject: {assignment.subject} | Priority: {assignment.priority_level}")
    else:
        print("No assignments found.")


def list_reminders():
    print("\nReminders:")
    reminders = db.session.query(Reminder, Assignment).join(Assignment).all()
    if reminders:
        for reminder, assignment in reminders:
            print(f"Reminder ID: {reminder.reminder_id} | Assignment: {assignment.task_name} | Date: {reminder.date}")
    else:
        print("No reminders found.")

def list_study_sessions():
    print("\nStudy Sessions:")
    study_sessions = StudySession.query.all()
    if study_sessions:
        for session in study_sessions:
            print(f"Session ID: {session.session_id} | Subject: {session.subject} | Start: {session.start_time} | End: {session.end_time} | Notes: {session.notes}")
    else:
        print("No study sessions found.")

def delete_assignment(assignment_id, student_id):
    try:
        # Check if the assignment exists and belongs to the logged-in user
        assignment = Assignment.query.filter_by(assignment_id=assignment_id, student_id=student_id).first()
        if assignment:
            # Delete all reminders linked to the assignment
            reminders = Reminder.query.filter_by(assignment_id=assignment_id).all()
            for reminder in reminders:
                db.session.delete(reminder)
            db.session.commit()  # Commit after deleting reminders

            # Delete the assignment
            db.session.delete(assignment)
            db.session.commit()
            print(f"Assignment ID {assignment_id} and its associated reminders deleted successfully.")
        else:
            print(f"No assignment found with ID {assignment_id} for the current user.")
    except Exception as e:
        print(f"Error deleting assignment: {e}")



def delete_reminder(reminder_id):
    try:
        reminder = Reminder.query.get(reminder_id)
        if reminder:
            db.session.delete(reminder)
            db.session.commit()
            print(f"Reminder ID {reminder_id} deleted successfully.")
        else:
            print(f"No reminder found with ID {reminder_id}.")
    except Exception as e:
        print(f"Error deleting reminder: {e}")

def delete_study_session(session_id):
    try:
        session = StudySession.query.get(session_id)
        if session:
            db.session.delete(session)
            db.session.commit()
            print(f"Study Session ID {session_id} deleted successfully.")
        else:
            print(f"No study session found with ID {session_id}.")
    except Exception as e:
        print(f"Error deleting study session: {e}")
        
def edit_assignment(student_id):
    while True:
        print("\nYour Assignments:")
        list_assignments(student_id)
        print("Enter the Assignment ID to edit or '0' to return to the main menu.")
        assignment_id = input("Assignment ID: ")

        if assignment_id == '0':
            print("Returning to main menu.")
            break

        try:
            assignment = Assignment.query.filter_by(assignment_id=assignment_id, student_id=student_id).first()
            if assignment:
                print(f"\nEditing Assignment: {assignment.task_name} (ID: {assignment_id})")
                new_task_name = input(f"Enter new task name (leave blank to keep: '{assignment.task_name}'): ")
                new_due_date = input(f"Enter new due date (YYYY-MM-DD, leave blank to keep: '{assignment.due_date}'): ")
                new_subject = input(f"Enter new subject (leave blank to keep: '{assignment.subject}'): ")
                new_priority = input(f"Enter new priority level (1-5, leave blank to keep: '{assignment.priority_level}'): ")

                # Update fields if new values are provided
                if new_task_name.strip():
                    assignment.task_name = new_task_name
                if new_due_date.strip():
                    assignment.due_date = datetime.strptime(new_due_date, '%Y-%m-%d')
                if new_subject.strip():
                    assignment.subject = new_subject
                if new_priority.strip():
                    assignment.priority_level = int(new_priority)

                db.session.commit()
                print(f"Assignment ID {assignment_id} updated successfully.")
            else:
                print(f"No assignment found with ID {assignment_id} for the current user.")
        except Exception as e:
            print(f"Error editing assignment: {e}")



# Main entry point
if __name__ == '__main__':
    # Create all tables
    with app.app_context():
        db.create_all()
    
    # Initialize student and launch menu
    with app.app_context():
        student_id = initialize_student()
        if student_id:
            menu(student_id)
