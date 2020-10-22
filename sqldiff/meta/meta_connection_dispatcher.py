# Todo metadata provider decorator (checks if sql, register meta etc)







import importlib.util

import pkg_resources
import psycopg2

import sys, inspect

def check_obj(obj):
    # inspec.get()
    mod = importlib.util.module_from_spec(obj)
    base, _sep, _stem = mod.__name__.partition('.')
    return sys.modules[base]

# https://stackoverflow.com/questions/2020014/get-fully-qualified-class-name-of-an-object-in-python
def fullname(o):
    # o.__module__ + "." + o.__class__.__qualname__ is an example in
    # this context of H.L. Mencken's "neat, plausible, and wrong."
    # Python makes no guarantees as to whether the __module__ special
    # attribute is defined, so we take a more circumspect approach.
    # Alas, the module name is explicitly excluded from __qualname__
    # in Python 3.
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__  # Avoid reporting __builtin__
    else:
        return module + '.' + o.__class__.__name__



connection_params = {
            'host': 'localhost',
            'port': '5432',
            'user': 'admin',
            'password': 'admin',
            'database': 'test_db'
        }

connection = psycopg2.connect(**connection_params)
a = dir(connection)
# chk_ob = check_obj(connection)
# print(chk_ob)
version = pkg_resources.get_distribution('psycopg2')

fn = fullname(connection)
m = inspect.getmodule(psycopg2)


for name, data in inspect.getmembers(connection):
    if name == '__builtins__':
        continue
    print('%s :' % name, repr(data))



b=1



