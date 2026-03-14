
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pyscopg2.extras import RealDictCursor

table = "youtube_api"

def get_conn_cursor():
  hook = PostgresHook(postgres_conn_id = "postgres_db_yt_elt", database = "elt_db")
  #in docker compose yaml line 80 we get the hook from AIRFLOW_CONN_POSTGRES_DB_YT_ELT
  conn = hook.get_conn()
  cur = conn.cursor(cursor_factory=RealDictCursor)
  return conn, cur

def close_conn_cursor(conn, cur):
  cur.close()
  conn.close()

def create_schema(schema):
  conn, cur = get_conn_cursor()
  create_schema_query = f"""
    CREATE SCHEMA IF NOT EXISTS {schema};
  """
  cur.execute(create_schema_query)
  conn.commit()
  close_conn_cursor(conn, cur)

def create_table(schema):
  conn, cur = get_conn_cursor()

  if schema == "staging":
    create_table_query = f"""
      CREATE TABLE IF NOT EXISTS {schema}.{table}.video_stats (
        "video_id" VARCHAR(100) PRIMARY KEY NOT NULL,
        "video_title" TEXT NOT NULL,
        "uploaded_date" TIMESTAMP NOT NULL,
        "duration" VARCHAR(20) NOT NULL,
        "video_views" INTEGER,
        "likes_count" INTEGER,
        "comments_count" INTEGER
      );
    """
  else:
    create_table_query = f"""
      CREATE TABLE IF NOT EXISTS {schema}.{table}.video_stats (
        "video_id" VARCHAR(100) PRIMARY KEY NOT NULL,
        "video_title" TEXT NOT NULL,
        "uploaded_date" TIMESTAMP NOT NULL,
        "duration" VARCHAR(20) NOT NULL,
        "video_views" INTEGER,
        "likes_count" INTEGER,
        "comments_count" INTEGER
      );
    """

  cur.execute(create_table_query)
  conn.commit()
  close_conn_cursor(conn, cur)

def get_video_ids(cur, schema):
  get_video_ids_query = f"""
    SELECT "video_id" FROM {schema}.{table};"""
  cur.execute(get_video_ids_query)
  extracting_ids = cur.fetchall()
  video_ids = [row["video_id"] for row in extracting_ids]
  return video_ids