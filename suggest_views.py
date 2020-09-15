
import query_mapping
import query_binary_mapping
import sqlparse
import re
import sys
import TPCH_DDL

#
# input_file = sys.argv[1]
# use_predicate = sys.argv[2] == 'yes'

input_file = 'batch_queries.sql'
use_predicate = True

fd = open ( input_file, 'r' )
sqlFile = fd.read ()

commands = sqlparse.split ( sqlFile )
commands = [x for x in commands if x] #remove empty files


views_code, views_queries , queries = query_mapping.suggest_materialized_views(commands,use_predicate) #With predicate is True by default

for view_name,view_code in views_code.items():
     print(view_name)
     print(view_code)
     print("queries of "+view_name)
     for q in views_queries[view_name]: #Query_rewrtiting_module

          select, join, where  =  query_mapping.sql_to_la(queries[q],True)

          print('= ORIGINAL QUERY = ')
          print(queries[q])
          groupby_orderby =''
          select = ','.join(select)
          select = select.replace('.','_')
          where = ','.join(where)
          if 'group by' in queries[q]:
               groupby_orderby = queries[q].split('group by')
               # print('1=', groupby_orderby)
               groupby_orderby=groupby_orderby[-1]
               # print ( '2=', groupby_orderby )
               groupby_orderby = groupby_orderby.replace('.','_')
               # print ( '3=', groupby_orderby )
               groupby_orderby = ' group by ' + groupby_orderby
               # print('4=',groupby_orderby)
          where = where.replace('.','_')

          select = re.sub(r"sum.*as",'sum(',select)

          print('select '+select+' from '+view_name + ' ' + where + groupby_orderby)
     print ('====')

fd.close()

