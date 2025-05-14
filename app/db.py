# connect to the database

import pymysql # imports the library which allows Python to connect to a MySQL database
import os # built-in module for accessing en variables (interacting with the operating system)
from flask import g # g is Flask object used to store data during a request
from contextlib import contextmanager
from typing import Generator

def get_db(): # function that the app can call to get a MySQL connection
    if 'db' not in g: # to check if a database connection already exists in g for this request
        try:
            g.db = pymysql.connect(
                host=os.getenv("DB_HOST"), # grabs values from .env file
                user=os.getenv("DB_USER"),
                passwd=os.getenv("DB_PASSWORD"),
                db=os.getenv("DB_NAME"),
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.Error as e:
            raise Exception(f"Database connection failed: {str(e)}")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@contextmanager
def get_db_connection() -> Generator[pymysql.Connection, None, None]:
    """Context manager for database connections."""
    conn = None
    try:
        conn = get_db()
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.commit()