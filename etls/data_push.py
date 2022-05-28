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
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        sys.stderr.write(f"{str(error)}")


def insert_measurement(
    conn, record: Dict[str, Any], existing_columns: faust.types.tables.TableT
):
    command = f"""
    INSERT INTO measurements (timestamp, name, value)
    VALUES (%s, %s, %s);"""
    new_columns = set(
        filter(lambda x: x not in existing_columns["labels"], record.keys())
    )
    print(type(existing_columns["labels"]))
    existing_columns["labels"] |= new_columns
    print(existing_columns)
    insert_column(conn, new_columns)

    try:
        cur = conn.cursor()
        cur.execute(
            command,
            (
                record["timestamp"],
                record["name"],
                record["value"],
            ),
        )
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        sys.stderr.write(f"DB ERROR (insert record) {str(error)}")


def insert_column(conn, colnames: Iterable[str]) -> None:
    try:
        sys.stderr.write(f"Creating cursor")
        cur = conn.cursor()
        args = ", ".join(cur.mogrify("ADD COLUMN %s IF NOT EXISTS", list(colnames)))
        command = f"""ALTER TABLE IF EXISTS measurements {args};"""
        cur.execute(command)
        sys.stderr.write(f"Closing cursor")
        cur.close()
        sys.stderr.write("Commit")
        conn.commit()
    except (Exception, psycopg2.DataError) as error:
        sys.stderr.write(f"DB ERROR (insert_column) {str(error)}")
