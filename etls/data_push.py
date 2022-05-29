from typing import Any, Dict, Iterable
import faust
import psycopg2
import sys
import faust.types.tables


def create_table(conn):
    command = """
    CREATE TABLE IF NOT EXISTS measurements (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP NOT NULL,
    name STRING NULL,
    value FLOAT NULL,
    CONSTRAINT "primary" PRIMARY KEY (id),
    FAMILY "primary" (id, timestamp, name, value)
    );
    """
    try:
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        sys.stderr.write(f"{str(error)}")


def insert_measurement(
    conn, record: Dict[str, Any], existing_columns: faust.types.tables.TableT
) -> None:
    command = f"""
    INSERT INTO measurements ({', '.join(record.keys())})
    VALUES ({'%s, ' * (len(record.keys()) - 1) + '%s'});"""
    new_columns = list(
        filter(lambda x: x not in existing_columns["labels"], record.keys())
    )
    existing_columns["labels"] += new_columns
    if len(new_columns) > 0:
        insert_column(conn, new_columns)

    try:
        cur = conn.cursor()
        cur.execute(
            command,
            list(record.values()),
        )
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        sys.stderr.write(f"DB ERROR (insert record) {str(error)}")


def insert_column(conn, colnames: Iterable[str]) -> None:
    try:
        conn.commit()
        cur = conn.cursor()
        for i in colnames:
            cur.execute(
                f"ALTER TABLE IF EXISTS measurements ADD COLUMN IF NOT EXISTS {i} STRING;"
            )
        cur.close()
    except (Exception, psycopg2.DataError) as error:
        sys.stderr.write(f"DB ERROR (insert_column) {str(error)}")
    conn.commit()
