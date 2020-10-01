import prestodb
import csv
conn=prestodb.dbapi.connect(
    host='localhost',
    port=8080,
    user='the-user',
    catalog='hive',
    schema='tpch',
)
cur = conn.cursor()
cur.execute('SELECT distinct(date) FROM date_dim')
dates = ['dates']
dates += sorted([element[0] for element in cur.fetchall()] )

cur.execute('SELECT distinct(nation) FROM customer')
c_nation = ['c.nation']
c_nation += [element[0] for element in cur.fetchall()]

cur.execute('SELECT distinct(nation) FROM supplier')
s_nation = ['s.nation']
s_nation += [element[0] for element in cur.fetchall()]

cur.execute('SELECT distinct(brand1) FROM part')
p_brand = ['p.brand']
p_brand += [element[0] for element in cur.fetchall()]


cur.execute('SELECT distinct(name) FROM customer')
c_name = ['c.name']
c_name = [element[0] for element in cur.fetchall()]


a = [dates,c_nation,s_nation,p_brand,c_name]
with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(a)
