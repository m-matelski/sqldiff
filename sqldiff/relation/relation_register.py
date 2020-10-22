# TODO DEFINE RELATIONS

@dbmapping('LONG VARCHAR', dbsystem.TERADATA)
def teradata_long_varchar_mapping(src_col: ColumnDescription):
    tgt_col = deepcopy(src_col)
    tgt_col.type_name = 'VARCHAR'
    tgt_col.precision = 64000
    return tgt_col