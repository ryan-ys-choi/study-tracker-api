# connect to the database

import pymysql # imports the library which allows Python to connect to a MySQL database
import os # built-in module for accessing en variables (interacting with the operating system)
from flask import g # g is Flask object used to store data during a request

def get_db(): # function that the app can call to get a MySQL connection
    if 'db' not in g: # to check if a database connection already exists in g for this request
        # On the object g, assign custom attribute called g
        g.db = pymysql.connect(
            host=os.getenv("DB_HOST"), # grabs values from .env file
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME"),
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db