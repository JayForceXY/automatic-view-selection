import prestodb

conn=prestodb.dbapi.connect(
    host='localhost',
    port=8080,
    user='the-user',
    catalog='hive',
    schema='tpch',
)
cur = conn.cursor()
cur.execute('SELECT distinct(date) FROM date_dim')
dates = sorted([element[0] for element in cur.fetchall()] )

cur.execute('SELECT distinct(nation) FROM customer')

c_nation = [element[0] for element in cur.fetchall()]

cur.execute('SELECT distinct(nation) FROM supplier')

s_nation = [element[0] for element in cur.fetchall()]

cur.execute('SELECT distinct(brand1) FROM part')

p_brand = [element[0] for element in cur.fetchall()]


cur.execute('SELECT distinct(name) FROM customer')

c_name = [element[0] for element in cur.fetchall()]

# print(dates)
print(c_name)
print(p_brand)
