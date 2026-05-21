# Inspection Query Recipes

Ready-to-use psycopg2 query patterns for PostgreSQL schema inspection with restricted permissions.

## Connection boilerplate

```python
import psycopg2

conn = psycopg2.connect(
    host="<host>",
    user="<user>",
    password="<password>",
    dbname="<dbname>",
    connect_timeout=10
)
conn.autocommit = True  # CRITICAL: prevents InFailedSqlTransaction on permission errors
cur = conn.cursor()
```

## List all tables with row estimates

```python
cur.execute("""
    SELECT n.nspname, c.relname, c.reltuples::bigint
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
      AND c.relkind = 'r'
    ORDER BY n.nspname, c.relname
""")
for schema, table, est_rows in cur.fetchall():
    print(f"{schema}.{table} (~{est_rows:,} rows)")
```

## Get columns for all tables in a schema

```python
cur.execute("""
    SELECT c.relname, c.reltuples::bigint,
           a.attname, pg_catalog.format_type(a.atttypid, a.atttypmod),
           CASE WHEN a.attnotnull THEN 'NOT NULL' ELSE 'NULL' END,
           COALESCE(pg_get_expr(d.adbin, d.adrelid), '')
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    JOIN pg_attribute a ON a.attrelid = c.oid
    LEFT JOIN pg_attrdef d ON d.adrelid = c.oid AND d.adnum = a.attnum
    WHERE n.nspname = %s
      AND c.relkind = 'r'
      AND a.attnum > 0
      AND NOT a.attisdropped
    ORDER BY c.relname, a.attnum
""", (schema_name,))
```

## Accurate row counts via pg_stat_user_tables

```python
cur.execute("""
    SELECT schemaname, relname, n_live_tup, n_dead_tup,
           last_autoanalyze, last_analyze
    FROM pg_stat_user_tables
    ORDER BY schemaname, relname
""")
```

`n_live_tup` is more accurate than `reltuples` from `pg_class`.

## Get indexes for a table

```python
cur.execute("""
    SELECT indexname, indexdef
    FROM pg_indexes
    WHERE schemaname = %s AND tablename = %s
    ORDER BY indexname
""", (schema, table))
```

## Get foreign key relationships

```python
cur.execute("""
    SELECT conname, conrelid::regclass AS table,
           a.attname AS column,
           confrelid::regclass AS foreign_table,
           af.attname AS foreign_column
    FROM pg_constraint c
    JOIN pg_attribute a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
    JOIN pg_attribute af ON af.attnum = ANY(c.confkey) AND af.attrelid = c.confrelid
    WHERE c.contype = 'f'
      AND c.conrelid::regclass::text LIKE %s
""", (f'{schema}.%',))
```

Note: `::regclass` cast may fail with restricted permissions — use JOIN on `pg_namespace` as a fallback.
