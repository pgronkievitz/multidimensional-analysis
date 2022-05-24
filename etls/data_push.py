import faust
from record import ParsedRecord
from datetime import datetime
import psycopg2


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
    VALUES ('{date}', '{time}', {name}, {value});""".format(date=
                                                                        record.timestamp.strftime("%m-%d-%y"),
                                                            time=record.timestamp.strftime("%H:%M:%S"),
                                                            name=record.name,
                                                            value=record.value
                                                            )
    try:
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
