from airflow import DAG
import pendulum 
from datetime import datetime, timedelta

from api.video_stats import (get_playlist_id, get_video_ids, extract_video_data, save_to_json)
from api.db_tasks import staging_table, core_table

#Define the local timezone
local_tz = pendulum.timezone("Europe/London")

#Default Args
default_args = {
    "owner": "dataengineers",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "data@engineers.com",
    # "retries": 1,
    # "retry_delay": timedelta(minutes=5),
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2026, 3, 13, tzinfo=local_tz),
    # "end_date": datetime(2030, 6, 30, tzinfo=local_tz),
}

with DAG(
     dag_id="produce_json",
     default_args=default_args,
     description="DAG to extract raw video data from YouTube API and save it as JSON",
     schedule='0 14 * * *', #runs every day at 2pm
     catchup=False,
 ) as produce_json_dag:
     
     #Define tasks
     playlist_id = get_playlist_id()
     video_ids = get_video_ids(playlist_id)
     extract_data = extract_video_data(video_ids)
     save_to_json_task = save_to_json(extract_data)

     #Define task dependencies
     playlist_id >> video_ids >> extract_data >> save_to_json_task

with DAG(
     dag_id="update_db",
     default_args=default_args,
     description="DAG to process JSON file and insert data into both staging and core schema",
     schedule='0 15 * * *', #runs every day at 3pm
     catchup=False,
 ) as update_db_dag:
     
     #Define tasks
     update_staging = staging_table()
     update_core = core_table()

     #Define task dependencies
     update_staging >> update_core 

     
