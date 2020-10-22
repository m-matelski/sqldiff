import psycopg2

# API example


"""
diff result should have option to filter only to problematic fields (generator?)

diff list result should have option to filter only to diff results where problem occurded (generator?)

statuses as booleans?

switching source with target result display should work without rerunning db call
"""

# calling compare
# source_connection = psycopg2.connect(...)
"""(1 objet comparison)
calling for single object
specified connection and query for source and target"""
diff_result = sqldiff.compare(source_connection, source_query, target_connection, target_query)

"""specify 2 dicts with connection and query for source and targets (1 objects comparison)
source, target = dict{'connection': x, 'query': y}"""
sqldiff.compare(source, target)

"""2 lists of dicts {connection: x, query: y}
source, target = List[dict[connection, query]]"""
sqldiff.compare(source, target)

"""2 dicts of {connection: x, query: [...]}
source, target = Dict[connection, List[query]]"""
sqldiff.compare(source, target)

"""dict of {source: dicts/lists, target: dict/lists}
source_target = dict[source: List of dicts / dict of lists, target: ...]"""
sqldiff.compare(source_target) -> List of diff_results

"""tuple (lists/dicts, lists/dicts)
source_target = Tuple[source List of dicts / dict of lists, target ...]"""
sqldiff.compare(source_target) -> list of diff results

# result
diff_result = [{source: x, target: y{DbApiField, database_type, compare_status, position, pos_diff, source.target pos in this list}}]



# Checkign status
# whole diff status
diff_result.match() # true false, true if all fields exact match name, type attribute

# iterate and indexing fields in resul set
(SqlDiffStatus.Field.Name.Match, SqlDiffStatus.Field.Attribute.Match) in diff_result[0].status # any, all
# statuses wildcards
(SqlDiffStatus._.NoMatch) diff_result[0].status
SqDiffStatus.Position.Match




diff_result = sqldiff.compare(source_connection, source_query, target_connection, target_query)
"""
* single object check
* check if its query or table name, generate query from tablename, parse and validate query
* check source target connection types (databases) pick right get metadata function
* pass query and connection to right function
"""





Field = List[ColumnDescription]

compare_field



filed_diff_result = List[Tuple[src column, tgt_column]]











