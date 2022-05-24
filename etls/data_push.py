import faust
from record import ParsedRecord
from datetime import datetime
import psycopg2
import sys


def create_table(conn):
    command = """
    CREATE TABLE IF NOT EXISTS measurements (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    date DATE NOT NULL,
    time TIME NOT NULL,
    name STRING NULL,
    value FLOAT NULL,
    CONSTRAINT "primary" PRIMARY KEY (id ASC),
    FAMILY "primary" (id, date, time, name, value)
    );  """
    try:
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_measurement(conn, record: ParsedRecord):
    command = """
    INSERT INTO measurements (date, time, name, value)
    VALUES (%s, %s, %s, %s);"""
    try:
        cur = conn.cursor()
        cur.execute(
            command,
            (
                record.timestamp.strftime("%m-%d-%y"),
                record.timestamp.strftime("%H:%M:%S"),
                record.name,
                record.value,
            ),
        )
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        sys.stderr.write(f"DB ERROR {str(error)}")
