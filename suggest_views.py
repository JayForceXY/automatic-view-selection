
import query_mapping
import query_binary_mapping
import sqlparse
import json
import re
import sys
import TPCH_DDL

#
input_file = sys.argv[1]
use_predicate = sys.argv[2] == 'yes'

# input_file = 'batch_queries2.sql'
# use_predicate = True



fd = open ( input_file, 'r' )
sqlFile = fd.read ()

commands = sqlparse.split ( sqlFile )
commands = [x for x in commands if x] #remove empty files


views_code, views_queries , queries = query_mapping.suggest_materialized_views(commands, use_predicate) #With predicate is True by default
views_code,translated_queries,queries_set = query_mapping.query_rewriting(views_code=views_code,views_queries=views_queries,queries=queries)

for view in views_code:
    print(view)
    print(views_code[view])
    print(' == Original Queries  == ')
    for q in views_queries[view]:
        print(queries_set[q])
    print(' == Translated Quereis == ')
    print( translated_queries[view].replace(';','\n'))

fd.close()

