
import query_mapping
import sqlparse
import query_binary_mapping
import TPCH_DDL
import numpy as np


fd = open ( 'batch_queries3.sql', 'r' )
sqlFile = fd.read ()

commands = sqlparse.split ( sqlFile )
commands = [x for x in commands if x] #remove empty files

views,x,y = query_mapping.queries_view_mapping( commands )

SQL = query_mapping.view_statements_definition_creation( views )

view_with_predicat = False
for view_name, view_code in query_mapping.view_sql_code(SQL,x,y,view_with_predicat).items():
     print(view_name)
     print(view_code)
     print('====')
     where = ''



fd.close()

