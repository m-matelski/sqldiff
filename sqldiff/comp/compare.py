from operator import itemgetter, attrgetter
from typing import List

from sqldiff.comp.syntax_analysis import is_schema_dot_table_string, schema_table_name_to_query, is_select_statement
from sqldiff.meta.compare_description import ColumnDescription, ColumnsComparisonResult
from sqldiff.relation.relation_manager import get_relations


KEYS_ORDER_TARGET = 'target'
KEYS_ORDER_SOURCE = 'source'
KEYS_ORDER_ZIP = 'zip'
KEY_ORDER_OPTIONS = (KEYS_ORDER_TARGET, KEYS_ORDER_SOURCE, KEYS_ORDER_ZIP)


def get_item_or_none(iterable, i):
    try:
        return iterable[i]
    except IndexError:
        return None


def _compare_keys_zip(source_keys, target_keys):
    pos_factor = 0
    src_idx = 0
    tgt_idx = 0
    key_comp_list = []

    # set of common keys
    common_keys = source_keys.keys() & target_keys.keys()

    while src_idx < len(source_keys) or tgt_idx < len(target_keys):

        src_key = get_item_or_none(list(source_keys.keys()), src_idx)
        tgt_key = get_item_or_none(list(target_keys.keys()), tgt_idx)

        if src_key in common_keys and tgt_key in common_keys:
            comparison_dict = {
                'source': source_keys[src_key],
                'target': target_keys[tgt_key],
                'exists_on_source': True,
                'exists_on_target': True,
                'match': True,
                'inserted_on_source': False,
                'inserted_on_target': False,
                'order_match': bool(src_idx + pos_factor == tgt_idx and src_key == tgt_key)
            }
            key_comp_list.append(comparison_dict)
            src_idx += 1
            tgt_idx += 1

        else:

            if tgt_key not in common_keys and tgt_key is not None:
                comparison_dict = {
                    'source': None,
                    'target': target_keys[tgt_key],
                    'exists_on_source': False,
                    'exists_on_target': True,
                    'match': False,
                    'inserted_on_source': False,
                    'inserted_on_target': bool(src_idx + pos_factor == tgt_idx),
                    'order_match': bool(src_idx + pos_factor == tgt_idx)
                }
                key_comp_list.append(comparison_dict)
                tgt_idx += 1
                pos_factor += 1

            if src_key not in common_keys and src_key is not None:
                comparison_dict = {
                    'source': source_keys[src_key],
                    'target': None,
                    'exists_on_source': True,
                    'exists_on_target': False,
                    'match': False,
                    'inserted_on_source': bool(src_idx + pos_factor == tgt_idx),
                    'inserted_on_target': False,
                    'order_match': bool(src_idx + pos_factor == tgt_idx)
                }
                key_comp_list.append(comparison_dict)
                src_idx += 1
                pos_factor -= 1

    return key_comp_list


def compare_keys(source, target, key=None):
    getter = key if key is not None else lambda a: a
    # dict key insertion order
    source_keys = {getter(i): i for i in source}
    target_keys = {getter(i): i for i in target}

    keys_comparison = _compare_keys_zip(source_keys, target_keys)

    # Add

    return keys_comparison


def _compare_columns_attributes(src_col: ColumnDescription, tgt_col: ColumnDescription):
    precision_is_comparable = src_col.precision is not None and tgt_col.precision is not None
    scale_is_comparable = src_col.scale is not None and tgt_col.scale is not None
    comparison_result = {
        'precision_match': src_col.precision == tgt_col.precision if precision_is_comparable else True,
        'precision_higher_on_target': src_col.precision < tgt_col.precision if precision_is_comparable else False,
        'precision_higher_on_source': src_col.precision > tgt_col.precision if precision_is_comparable else False,
        'scale_match': src_col.scale == tgt_col.scale if scale_is_comparable else True,
        'scale_higher_on_target': src_col.scale < tgt_col.scale if scale_is_comparable else False,
        'scale_higher_on_source': src_col.scale > tgt_col.scale if scale_is_comparable else False,
        'type_name_match': src_col.type_name == tgt_col.type_name
    }
    return comparison_result


COMPARISON_RESULT_SCORECARD = {
    'precision_match': lambda x: (not x) * 5,
    'precision_higher_on_target': lambda x: x * 1,
    'precision_higher_on_source': lambda x: x * 2,
    'scale_match': lambda x: (not x) * 5,
    'scale_higher_on_target': lambda x: x * 1,
    'scale_higher_on_source': lambda x: x * 2,
    'type_name_match': lambda x: (not x) * 50
}


def _calculate_attributes_comparison_result_score(attributes_comparison_result, scorecard=None):
    if scorecard is None:
        scorecard = COMPARISON_RESULT_SCORECARD
    score = sum([scorecard[k](v) for k, v in attributes_comparison_result.items()])
    return score


def compare_columns(src_col: ColumnDescription, tgt_col: ColumnDescription):
    # Get all mapping functions for source column to target database system
    relations = get_relations(src_col=src_col, tgt_col=tgt_col)
    # Map source column using every returned relation
    mapped_source_columns = [rel(src_col) for rel in relations]
    # Compare mapped fields with target field
    attr_comp_results = [_compare_columns_attributes(src_mapped_column, tgt_col) for src_mapped_column in
                         mapped_source_columns]
    # Calculate comparison results scores
    comparison_scores = [_calculate_attributes_comparison_result_score(res) for res in attr_comp_results]
    # Pack data into dictionary entry
    comparison_result = {
        'source_column': src_col,
        'target_column': tgt_col,
        'attributes_comparison_results': [
            {
                'relation': relation,
                'mapped_source_column': mapped_source_column,
                'attr_comp_result': attr_comp_result,
                'comparison_score': comparison_score
            }
            for relation, mapped_source_column, attr_comp_result, comparison_score
            in zip(relations, mapped_source_columns, attr_comp_results, comparison_scores)
        ]
    }
    # Order attributes_comparison_results by score asc
    comparison_result['attributes_comparison_results'].sort(key=itemgetter('comparison_score'))
    return comparison_result


def compare_column_lists(src_cols: List[ColumnDescription], tgt_cols: List[ColumnDescription]):

    # Convert List[ColumnDescription] to Dict[name, ColumnDescription]
    src_cols_dict = {col_desc.name: col_desc for col_desc in src_cols}
    tgt_cols_dict = {col_desc.name: col_desc for col_desc in tgt_cols}

    # Compare Keys
    keys_comparison = compare_keys(src_cols, tgt_cols, key=attrgetter('name'))
    # Add columns key comparison - using target column for comparing attributes for matching columns
    columns_comparison = [
        compare_columns(src_cols_dict[kc['target'].name], tgt_cols_dict[kc['target'].name]) if kc['match'] else None
        for kc in keys_comparison
    ]

    for kc, cc in zip(keys_comparison, columns_comparison):
        kc['attributes_comparison_results'] = cc['attributes_comparison_results'] if cc is not None else None

    result = ColumnsComparisonResult(keys_comparison)
    return result

def validate_compare_query(query):
    if is_schema_dot_table_string(query):
        return schema_table_name_to_query(query)
    if is_select_statement(query):
        return query
    else:
        raise ValueError('Invalid statement. Must be schema.table or SELECT statement.')



def compare(source_connection, source_query, target_connection, target_query,
            source_get_meta=None, target_get_meta=None):
    # TODO - metadata provider dispatching based on connection object
    # validsate query - check if it is quyery or schema.table, check if theres only one query, chec if it is select query.
    src_sql = validate_compare_query(source_query)
    tgt_sql = validate_compare_query(target_query)

    src_cols = source_get_meta(source_connection, src_sql)
    tgt_cols = target_get_meta(target_connection, tgt_sql)

    result = compare_column_lists(src_cols, tgt_cols)
    return result



