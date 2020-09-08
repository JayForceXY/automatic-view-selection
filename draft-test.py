
import query_mapping
import sqlparse
import re
import query_binary_mapping
import TPCH_DDL
import numpy as np


fd = open ( 'batch_queries3.sql', 'r' )
sqlFile = fd.read ()

commands = sqlparse.split ( sqlFile )
commands = [x for x in commands if x] #remove empty files



views_code, views_queries , queries = query_mapping.suggest_materialized_views(commands)

for view_name,view_code in views_code.items():
     print(view_name)
     print(view_code)
     for q in views_queries[view_name]: #Query_rewrtiting_module

          select, join, where  =  query_mapping.sql_to_la(queries[q],True)

          select = ','.join(select)
          where = ','.join(where)
          where = where.replace('.','_')
          select = re.sub(r"sum.*as",' ',select)
          print('select '+select+' from '+view_name +' ' +where)

     print ('====')

fd.close()

