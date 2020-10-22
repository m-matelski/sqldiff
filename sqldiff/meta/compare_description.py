import functools


class ColumnDescription:
    """
    PEP 249 - https://www.python.org/dev/peps/pep-0249/
    DB API Cursor description provides sequence of 7 items describing one result column:
    name, type_code, display_size, internal_size, precision, scale, null_ok
    The first two items (name and type_code) are mandatory,
    the other five are optional and are set to None if no meaningful values can be provided.

    Thi class contains additional fields such as:
    source database type (dbsystem),
    type_name (not provided in cursor desciption),
    position
    """

    def __init__(self, name, type_code, display_size, internal_size,
                 precision, scale, null_ok, type_name, position, dbsystem):
        self.name = name
        self.type_code = type_code
        self.display_size = display_size
        self.internal_size = internal_size
        self.precision = precision
        self.scale = scale
        self.null_ok = null_ok
        self.type_name = type_name
        self.position = position
        self.dbsystem = dbsystem

    def __repr__(self):
        column_desc = f"ColumnDescription({self.position=}, {self.dbsystem=}, {self.name=}, {self.type_name=}, " \
                      f"{self.precision=}, {self.scale=}, {self.internal_size=}, " \
                      f"{self.null_ok=}, {self.display_size=}, {self.type_code=})"
        column_desc = column_desc.replace('self.', '')
        return column_desc

    def __str__(self):
        s_prec = str(self.precision) if self.precision is not None else ''
        s_scale = str(self.scale) if self.scale is not None else ''
        s = f'{self.name} {self.type_name}({", ".join(filter(None, (s_prec, s_scale)))})'.replace('()', '')
        return s

    @functools.cached_property
    def dict(self):
        return {
            self.name: self
        }


class ColumnsComparisonResult:
    """
    This class stores compare_column_lists result [Dict] and provides some methods for analyzing comparison result.
    """

    def __init__(self, comparison_result):
        self.comparison_result = comparison_result

    def __iter__(self):
        return iter(self.comparison_result)

    def __len__(self):
        return len(self.comparison_result)

    def __str__(self):
        max_src = self.get_column_str_max_len('source')
        max_tgt = self.get_column_str_max_len('target')

        header = 'SOURCE TARGET MATCH ORDER_MATCH TYPE_MATCH ATTR_MATCH'.split()
        row_format = '{:>' + str(max_src+3) + '} | {:' + str(max_tgt+3) + '} - {:^20}|{:^20}|{:^20}|{:^20}|'
        rows = []
        for c in self.comparison_result:
            try:
                attr = c['attributes_comparison_results'][0]['attr_comp_result']
            except TypeError:
                attr = dict()
                attr['type_name_match'] = 'N/A'
                attr['precision_match'] = 'N/A'
                attr['scale_match'] = 'N/A'

            r = map(str, [c['source'], c['target'], c['match'], c['order_match'],
                    attr['type_name_match'], attr['precision_match'] and attr['scale_match']])

            rows.append(r)
        output_rows = [row_format.format(*header)] + [row_format.format(*r) for r in rows]
        output_string = '\n'.join(output_rows)
        # [row_format.format(header)]# +
        return output_string





    def get_column(self, col_name, col_source='target'):
        """
        Search and return specified column from comparison_result.

        :param col_name: Column name to look for.
        :param col_source: Specify if column will be looked for in 'source' or 'target' columns.
        :return: comparison_result row with specified column.
        """

        try:
            for c in self.comparison_result:
                if c[col_source].name==col_name:
                    return c
        except KeyError:
            raise KeyError("col_source must have value of 'source' or 'target'.")

    def match(self, order=True):
        """
        Checks if target columns match source columns in terms of names, orders and columns attributes.
        :param order: Default True. Set to False if want to ommit order checking.
        :return:
        """
        # Catching KeyError when 'attributes_comparison_results' doesn't exist (no matching field on source/target)
        try:
            for c in self:
                if not (c['match'] and (c['order_match'] or not order) and
                        c['attributes_comparison_results'][0]['comparison_score']==0):
                    return False
        except KeyError:
            return False
        return True

    def get_column_str_max_len(self, col_source='target'):
        """
        Gets longest column string representation on 'source' or 'target'
        :param col_source: 'source' or 'target'
        :return: length of longest column string representation
        """
        try:
            return max([len(str(c[col_source])) for c in self.comparison_result])
        except KeyError:
            raise KeyError("col_source must have value of 'source' or 'target'.")




# TODO change compare source / target functions to "order" funcns
# zip will be the basic for sorting
# for sorting keygetter will be used to get zip string, and string with field name will be mapped to position on source/target


# def _compare_keys_source(source_keys, target_keys):
#     l1 = [(src_key, src_key if src_key in target_keys else None) for src_key in source_keys.keys()]
#     l2 = [(None, tgt_key) for tgt_key in target_keys if tgt_key not in source_keys]
#     l3 = l1 + l2
#     a = 1
