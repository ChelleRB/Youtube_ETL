#dwh = short for datawarehouse

from datawarehouse.data_utils import get_conn_cursor, close_conn_cursor, create_schema, create_table, get_video_ids
from datawarehouse.data_loading import load_path
from datawarehouse.data_modification import insert_rows, update_rows, delete_rows
from datawarehouse.data_transformation import transform_data

import logging
from airflow.decorators import task

logger = logging.getLogger(__name__)
table = "youtube_api"

@task
def staging_table():
  schema = "schema"
  conn, cur = None, None

  try:
    conn, cur = get_conn_cursor()
    #after looking at data loading file i want the same name from the file_path
    Youtube_data = load_data()

    create_schema(schema)
    create_table(schema)

    table_ids = get_video_ids(cur, schema)
    for row in Youtube_data:
      if len(table_ids) == 0:
        insert_rows(cur, conn, schema, row)
      else:
        if row["video_id"] in table_ids:
          update_rows(cur, conn, schema, row)

    video_ids_in_json = (row["video_id"] for row in Youtube_data)
    video_ids_to_delete = set(table_ids) - video_ids_in_json

    if video_ids_to_delete:
      delete_rows(cur, conn, schema, video_ids_to_delete)

    logger.info(f"{schema} table update completed")

  except Exception as e:
    logger.error(f"An error occured during the update of {schema} table: {e}")
    raise e
  
  finally:
    if conn and cur:
      close_conn_cursor(conn, cur)

@task
def core_table():
  schema = "core"
  conn, cur = None, None

  try:
    conn, cur = get_conn_cursor

    create_schema(schema)
    create_table(schema)

    table_ids = get_video_ids(cur, schema)
    current_video_ids = set()

    cur.execute(f"SELECT * FROM staging.{table};")
    rows = cur.fetchall()

    for row in rows:
      current_video_ids.add(row["Video_id"])
      if len(table_ids) == 0:
        transform_data = transform_data(row)
        insert_rows(cur, conn, schema, transform_data)
      else:
        transform_data = transform_data(row)

        if transform_data["Video_id"] in table_ids:
          update_rows(cur, conn, schema, transform_data)
    
    video_ids_to_delete = set(table_ids) - current_video_ids

    if video_ids_to_delete:
      delete_rows(cur, conn, schema, transform_data)

    logger.info(f"{schema} table update completed")

  except Exception as e:
    logger.error(f"An error occured during update of {schema} table: {e}")
    raise e
  
  finally:
    #Ensuring the connection and cursor are closed
    if conn and cur:
      close_conn_cursor(conn, cur)









