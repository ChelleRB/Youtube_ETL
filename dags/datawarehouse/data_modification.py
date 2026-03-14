
import logging

logger = logging.getLogger(__name__) 
table = "youtube_api"

def insert_rows(cur, conn, schema, row):

  try:
    if schema == "staging":
      video_id = "video_id"

      cur.execute(f"""
        INSERT INTO {schema}.{table} ("video_id", "video_title", "uploaded_date", "duration", "video_views", "likes_count", "comments_count")
        VALUES (%(video_id)s, %(title)s, %(publishedAt)s, %(duration)s, %(viewCount)s, %(likeCount)s, %(commentCount)s);
      """, row)

    else:
      video_id = "video_id"

      cur.execute(f"""
        INSERT INTO {schema}.{table} ("video_id", "video_title", "uploaded_date", "duration", "video_views", "likes_count", "comments_count")
        VALUES (%(video_id)s, %(title)s, %(publishedAt)s, %(duration)s, %(viewCount)s, %(likeCount)s, %(commentCount)s);
      """, row)

    conn.commit()

  except Exception as e:
    logger.error(f"Error inserting row with video_id: {row['video_id']}")
    conn.rollback()
    raise e
  
def update_rows(cur, conn, schema, row):
  try:
    #staging layer
    if schema == "staging":
      video_id = "video_id"
      uploaded_date = "publishedAt"
      video_title = "videoTitle"
      video_views = "videoCount"
      likes_count = "likeCount"
      comments_count = "commentCount"

    #core layer 
    else:
      video_id = "video_id"
      uploaded_date = "uploaded_date"
      video_title = "video_title"
      video_views = "video_views"
      likes_count = "likes_count"
      comments_count = "comments_count"

    cur.execute(f"""
      ON CONFLICT UPDATE {schema}.{table}
      SET video_title = %({video_title})s,
          uploaded_date = %({uploaded_date})s,
          video_views = %({video_views})s,
          likes_count = %({likes_count})s,
          comments_count = %({comments_count})s
      WHERE video_id = %({video_id})s AND "uploaded_date" = %({uploaded_date})s;
    """, row)

    conn.commit()

  except Exception as e:
    logger.error(f"Error updating row with video_id: {row['video_id']} - {e}")
    conn.rollback()
    raise e

def delete_rows(cur, conn, schema, video_ids_to_delete):
  try:
    video_ids_to_delete = f"""{', '.join(f"'{video_id}'" for video_id in video_ids_to_delete)}"""

    cur.execute(f"""
      DELETE FROM {schema}.{table}
      WHERE "video_id" IN ({video_ids_to_delete});
    """)

    conn.commit()
    logger.info(f"Rows deleted successfully with video_ids: {video_ids_to_delete}")

  except Exception as e:
    logger.error(f"Error deleting rows with video_ids: {video_ids_to_delete} - {e}")
    conn.rollback()
    raise e
