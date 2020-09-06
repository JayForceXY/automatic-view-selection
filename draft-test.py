
import query_mapping
import sqlparse
import query_binary_mapping
import TPCH_DDL
import numpy as np
fd = open ( 'batch_queries2.sql', 'r' )
sqlFile = fd.read ()

commands = sqlparse.split ( sqlFile )
query_set = []
for command in commands:
    query_set.append(query_mapping.sql_to_la(command))

# print(query_binary_mapping.binary_mapping_table(table_attributes=TPCH_DDL.LINEORDER_ATTRIBUTES, r_attributes = ['shipmode','quantity']))


similar_queries = query_mapping.find_similar_queries(query_set)
print(similar_queries)
queries = similar_queries.values()
views = []
for query in queries :

    view_jnq = []
    view_prq = []
    view_rgq = []
    for q in query :
        tmp_view_prq, tmp_view_jnq,tmp_view_rgq = query_set[q]
        print(tmp_view_rgq)

        if tmp_view_prq:
            items = tmp_view_prq[0].split(',')
        for item in items:
            # print('item ==', item)
            if item not in view_prq : view_prq.append(item)

        if tmp_view_jnq :
            items = tmp_view_jnq
        for item in items :
            if item not in view_jnq : view_jnq.append ( item )

        if tmp_view_rgq:


            items = tmp_view_rgq
            print('where items',items)

        for item in items :
            if item not in view_rgq : view_rgq.append ( item )

    views.append([view_prq,view_jnq,view_rgq])
    print('===')
#
for view in views:
    select = list(dict.fromkeys(view[0]))
    join = list(dict.fromkeys(view[1]))
    where = list (dict.fromkeys(view[2]))
    print('select',select,'join',join,'where',where)
fd.close()
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
