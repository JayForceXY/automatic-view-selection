
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
# input_file = sys.argv[1]
# use_predicate = sys.argv[2] == 'yes'

input_file = 'batch_queries2.sql'
use_predicate = True

fd = open ( input_file, 'r' )
sqlFile = fd.read ()

commands = sqlparse.split ( sqlFile )
commands = [x for x in commands if x]
clustering = []
for command in commands:
    prj,jnq,rgq = query_mapping.sql_to_la(command)
    prj,agg = query_binary_mapping.detect_aggregation(prj)

    clustering.append(query_binary_mapping.binary_mapping_query(command))


y = pdist(clustering)
Z = weighted(y)
print(fcluster(Z,  2.6 , criterion='distance'))



