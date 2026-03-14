
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pyscopg2.extras import RealDictCursor

def get_conn_cursor():
  hook = PostgresHook(postgres_conn_id = "postgres_db_yt_elt", database = "elt_db")
  #in docker compose yaml line 80 we get the hook from AIRFLOW_CONN_POSTGRES_DB_YT_ELT
  conn = hook.get_conn()