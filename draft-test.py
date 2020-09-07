
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

x,y,views = query_mapping.view_definition(commands)
print(commands[2] ,'\n',commands[3], '\n',commands[9] ,'\n',commands[13])
SQL = query_mapping.view_creation(views)

for stmt in SQL :

     print(query_mapping.view_sql_code(stmt))



fd.close()

