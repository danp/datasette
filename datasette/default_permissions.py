from datasette import hookimpl
from datasette.utils import actor_matches_allow


@hookimpl(tryfirst=True)
def permission_allowed(datasette, actor, action, resource):
    if action == "permissions-debug":
        if actor and actor.get("id") == "root":
            return True
    elif action == "view-instance":
        allow = datasette.metadata("allow")
        if allow is not None:
            return actor_matches_allow(actor, allow)
    elif action == "view-database":
        database_allow = datasette.metadata("allow", database=resource)
        if database_allow is None:
            return True
        return actor_matches_allow(actor, database_allow)
    elif action == "view-table":
        database, table = resource
        tables = datasette.metadata("tables", database=database) or {}
        table_allow = (tables.get(table) or {}).get("allow")
        if table_allow is None:
            return True
        return actor_matches_allow(actor, table_allow)
    elif action == "view-query":
        # Check if this query has a "allow" block in metadata
        database, query_name = resource
        queries_metadata = datasette.metadata("queries", database=database)
        assert query_name in queries_metadata
        if isinstance(queries_metadata[query_name], str):
            return True
        allow = queries_metadata[query_name].get("allow")
        if allow is None:
            return True
        return actor_matches_allow(actor, allow)
    elif action == "execute-sql":
        # Use allow_sql block from database block, or from top-level
        database_allow_sql = datasette.metadata("allow_sql", database=resource)
        if database_allow_sql is None:
            database_allow_sql = datasette.metadata("allow_sql")
        if database_allow_sql is None:
            return True
        return actor_matches_allow(actor, database_allow_sql)