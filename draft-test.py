
import query_mapping
import sqlparse
fd = open ( 'batch_queries2.sql', 'r' )
sqlFile = fd.read ()

commands = sqlparse.split ( sqlFile )
for command in commands:
    print(query_mapping.sql_to_la(command))



# sql = 'select * from "someschema"."mytable" where id = 1'
# parsed = sqlparse.parse(sql)
# stmt = parsed[0]
# print (str(stmt))
# #only parts of sql statements
# print (str(stmt.tokens[-1]))
# #so the result of last str() method is 'where id = 1'
# print(str(stmt.tokens[-3]))
# #result "someschema"."mytable"


# cursor = presto.connect ( host='localhost',
#                         catalog='hive',
#                         schema='tpch').cursor ( )
#
# # Open and read the file as a single buffer
# fd = open('batch_queries.sql', 'r')
# sqlFile = fd.read()
# fd.close()
#
# # all SQL commands (split on ';')
# commands = sqlFile.split(';')
# query_set = []
# for command in commands:
#     query_set.append(command)
#
#
#
# print(query_set[0])
# cursor.execute("EXPLAIN select customer.nation, supplier.nation, date_dim.year, sum(revenue) as revenue from lineorder left join date_dim on lineorder.orderdate = date_dim.datekey left join customer on lineorder.custkey = customer.custkey left join supplier on lineorder.suppkey = supplier.suppkey where customer.region = 'ASIA' and supplier.region = 'ASIA' and date_dim.year >= 1992 and date_dim.year <= 1997 group by customer.nation, supplier.nation,date_dim.year order by date_dim.year asc,revenue desc")
# print(cursor.fetchall())
