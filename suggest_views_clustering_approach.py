
import query_mapping
import query_binary_mapping
import sqlparse
from scipy.cluster.hierarchy import weighted, fcluster
from scipy.spatial.distance import pdist
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import re
import sys
import TPCH_DDL

#
input_file = sys.argv[1]
use_predicate = sys.argv[2] == 'yes'



fd = open ( input_file, 'r' )
sqlFile = fd.read ()

commands = sqlparse.split ( sqlFile )
commands = [x for x in commands if x]
clustering = []

views_code, views_queries , queries = query_mapping.suggest_materialized_views_clustering_approach(commands, use_predicate)
views_code,translated_queries,queries_set = query_mapping.query_rewriting(views_code=views_code,views_queries=views_queries,queries=queries)

for view in views_code:
    print(view)
    print(views_code[view])
    print(' == Original Queries  == ')
    for q in views_queries[view]:
        print(queries_set[q])
    print(' == Translated Quereis == ')
    print( translated_queries[view].replace(';','\n'))



