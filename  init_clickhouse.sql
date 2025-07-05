clickhouse-client --query "CREATE DATABASE IF NOT EXISTS test"
clickhouse-client --query """
CREATE TABLE IF NOT EXISTS test.user_events (
    id UInt64,
    user String,
    event String,
    event_time DateTime
) ENGINE = MergeTree()
ORDER BY (id)
"""