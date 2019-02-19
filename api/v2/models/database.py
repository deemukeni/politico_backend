# import os
import os

import psycopg2
import sys

# connects to the database as indicated in the .env file
def connect_db():
    """
    A function make connection to database
    :return: conn, cursor
    """
    db_url=os.getenv("DATABASE_URL")
    conn= None
    cursor=None

    try:

        conn = psycopg2.connect(db_url)
        print ("\n Database connected\n")

        cursor = conn.cursor()
    except(Exception,psycopg2.DatabaseError,psycopg2.ProgrammingError) as error:
        print (error)
    
    return conn, cursor


def create_tables():
    """
    A function to create tables on the database
    """
    parties_table_query="""
    CREATE TABLE IF NOT EXISTS parties (
        party_id SERIAL PRIMARY KEY,
        party_name VARCHAR (24) NOT NULL,
        hqAddress VARCHAR NOT NULL,
        logo_url VARCHAR NOT NULL
    )
    """

    users_table_query="""
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        firstname VARCHAR (24) NOT NULL,
        lastname VARCHAR (24) NOT NULL,
        username VARCHAR (24) NOT NULL,
        email VARCHAR (24) NOT NULL,
        password VARCHAR (24) NOT NULL,
        phoneNumber INTEGER NOT NULL,
        passport_url VARCHAR NOT NULL
    )
    """

    offices_table_query="""
    CREATE TABLE IF NOT EXISTS offices (
        office_id SERIAL PRIMARY KEY,
        office_type VARCHAR (24) NOT NULL,
        office_name VARCHAR (24) NOT NULL
    )
    """

    candidates_table_query="""
    CREATE TABLE IF NOT EXISTS candidates (
        candidate_id SERIAL PRIMARY KEY,
        candidate_name VARCHAR (24) NOT NULL,
        office_id INTEGER NOT NULL,
        party_id INTEGER NOT NULL
    )
    """

    votes_table_query="""
    CREATE TABLE IF NOT EXISTS votes (
        vote_id SERIAL PRIMARY KEY,
        createdOn TIMESTAMP NOT NULL,
        createBy VARCHAR NOT NULL,
        candidateVoteFor VARCHAR  NOT NULL,
        officeVotedFor VARCHAR NOT NULL
    )
    """

    return [parties_table_query,users_table_query,offices_table_query,candidates_table_query, votes_table_query]


def drop_tables():
    """
    Drops the existing tables everytime the app is run to avoid any errors, i.e 
    "the table requested already exists"
    It returns an empty database every time the programme is run
    """
    drop_users_query="""
    DROP TABLE IF EXISTS users
    """

    drop_parties_query="""
    DROP TABLE IF EXISTS parties
    """

    drop_offices_query="""
    DROP TABLE IF EXISTS offices
    """

    drop_candidates_query="""
    DROP TABLE IF EXISTS candidates
    """

    drop_votes_query="""
    DROP TABLE IF EXISTS votes
    """

    return [drop_users_query, drop_parties_query, drop_offices_query, drop_candidates_query, drop_votes_query]

def initiate_database(db_url):
    """
    A function to initiate the database
    :param db_url: os.getenv("DATABASE_URL")(receives environment configurations from the .env file)
    :it first checks to see if the database is empty, if so it drops the tables leaving the databas empty
    :It will only add data into the database while its  still empty.
    """
    try:
        conn, cursor = connect_db()
        i = 0
        # drop_tables is for clearing all the data from the data base.
        queries = drop_tables() + create_tables()
        # queries = create_tables()

        while i != len(queries):
            query = queries[i]
            cursor.execute(query)
            conn.commit()
            i+=1

        conn.close()
    except Exception as error:
        print("\n Something went wrong: {}".format(error))

def select_from_database(query):
    """
    A function is for getting data from the database
    :param query: an sql query
    :return: rows from the querried table   
    """
    conn, cursor = connect_db()
    cursor.execute(query)
    rows = cursor.fetchall()

    conn.commit()
    conn.close()
    return rows

def insert_to_db(query):
    """
    A function for inserting data into the database
    :param query: an sql query
    """
    try:
        conn, cursor = connect_db()
        cursor.execute(query)
        conn.commit() # save
        conn.close()
    except psycopg2.Error as error:
        print (error)
