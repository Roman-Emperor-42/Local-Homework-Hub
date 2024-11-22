import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configuration for database creation
POSTGRES_USER = "postgres"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
DB_NAME = "homework_hub"

def create_database():
    """
    Create the PostgreSQL database 'homework_hub' with user-provided credentials.
    """
    try:
        # Prompt for the password
        postgres_password = input("Enter the PostgreSQL password for user 'postgres': ")

        # Connect to the default 'postgres' database
        connection = psycopg2.connect(
            dbname="postgres",
            user=POSTGRES_USER,
            password=postgres_password,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        # Create the database
        cursor.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"Database '{DB_NAME}' created successfully.")

        # Close connection
        cursor.close()
        connection.close()

    except psycopg2.errors.DuplicateDatabase:
        print(f"Database '{DB_NAME}' already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == "__main__":
    create_database()
