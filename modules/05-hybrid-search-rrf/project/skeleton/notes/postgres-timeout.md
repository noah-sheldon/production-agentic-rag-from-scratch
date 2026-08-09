# Postgres timeout

Postgres timeout happens when the connection pool is full and a timeout
queues every session. Raise the pool size or the timeout to clear the
backlog. Watch `pg_stat_activity` for sessions stuck in `idle in
transaction`.
