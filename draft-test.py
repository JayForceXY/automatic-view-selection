
import query_mapping
import sqlparse
import query_binary_mapping
import TPCH_DDL
import numpy as np


fd = open ( 'batch_queries3.sql', 'r' )
sqlFile = fd.read ()

commands = sqlparse.split ( sqlFile )
commands = [x for x in commands if x] #remove empty files
query_set = [query_mapping.sql_to_la(command) for command in commands]

views,x = query_mapping.queries_view_mapping( commands )

SQL = query_mapping.view_statements_definition_creation( views )


for view_name, view_code in query_mapping.view_sql_code(SQL).items():
     print(view_name)
     print(view_code)
     print('====')
     for query in x[view_name] :
          print(commands[query])
fd.close()

