def test_api_key(api_key):
    assert api_key == "MOCK_KEY1234"

def test_channel_handle(channel_handle):
    assert channel_handle == "COMEDY_BITES"

def test_postgres_conn(mock_postgres_conn_vars):
    conn = mock_postgres_conn_vars
    assert conn.login == "mock_username"
    assert conn.password == "mock_password"
    assert conn.host == "mock_host"
    assert conn.port == 1234
    assert conn.schema == "mock_db_name"

def test_dags_integrity(dagbag):
    assert len(dagbag.import_errors) == {}, f"DAG import errors: {dagbag.import_errors}"
    print(f"Found {len(dagbag.dags)} DAGs in the DAG bag.")

    expected_dags_ids = ["produce_json", "update_db", "data_quality_checks"]
    loaded_dags_ids = list(dagbag.dags.keys())

    for expected_dag_id in expected_dags_ids:
        assert expected_dag_id in loaded_dags_ids, f"DAG '{expected_dag_id}' not found in DAG bag. Loaded DAGs: {loaded_dags_ids}"

assert dagbag.size == 3
print(dagbag.size())

expected_task_counts = {
    "produce_json": 4,
    "update_db": 2,
    "data_quality_checks": 2
}
print("=================")
for dag_id, dag in dagbag.dags.items():
    task_count = len(dag.tasks)
    expected_count = expected_task_counts.get(dag_id)
    
    assert task_count == expected_count, f"DAG '{dag_id}' has {task_count} tasks, expected {expected_count}"
    print(f"DAG '{dag_id}' has {task_count} tasks (Expected: {expected_count})")

