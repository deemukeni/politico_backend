import os

import psycopg2
import sys

def connect_db():
    db_url=os.getenv("DATABASE_URL")
    conn= None
    cursor=None

    try:

        conn = psycopg2.connect(db_url)
        print ("connected")

        cursor = con.cursor()
    except(Exception,psycopg2.DatabaseError,psycopg2.ProgrammingError) as error:
        print (error)
    
    return conn , cursor

