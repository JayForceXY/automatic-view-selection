View0
create materialized view View0 as select c.nation as c_nation , c.region as c_region , d.year as d_year , p.brand1 as p_brand1 , p.category as p_category , p.mfgr as p_mfgr , s.city as s_city , s.nation as s_nation , s.region as s_region , sum(lo.revenue - lo.supplycost) as profit   from lineorder lo  join customer c on lo.custkey = c.custkey join date_dim d on lo.orderdate = d.datekey join part p on lo.partkey = p.partkey join supplier s on lo.suppkey = s.suppkey( c.region = 'AMERICA' and s.nation = 'UNITED STATES' and ( d.year = 1997 or d.year = 1998 ) and p.category = 'MFGR#14' ) or ( c.region = 'AMERICA' and s.region = 'AMERICA' and ( p.mfgr = 'MFGR#1' or p.mfgr = 'MFGR#2' ) ) or ( c.region = 'AMERICA' and s.region = 'AMERICA' and ( d.year = 1997 or d.year = 1998 ) and ( p.mfgr = 'MFGR#1' or p.mfgr = 'MFGR#2' ) )  group by c.nation,c.region,d.year,p.brand1,p.category,p.mfgr,s.city,s.nation,s.region
====
View1
create materialized view View1 as select d.weeknuminyear as d_weeknuminyear , d.year as d_year , d.yearmonthnum as d_yearmonthnum , lo.discount as lo_discount , lo.quantity as lo_quantity , sum(lo.extendedprice * lo.discount) as revenue   from lineorder lo  join date_dim d on lo.orderdate = d.datekey( d.year = 1993 and lo.discount between 1 and 3 and lo.quantity < 25 ) or ( d.weeknuminyear = 6 and d.year = 1994 and lo.discount between 5 and 7 and lo.quantity between 26 and 35 ) or ( d.yearmonthnum = 199401 and lo.discount between 4 and 6 and lo.quantity between 26 and 35 )  group by d.weeknuminyear,d.year,d.yearmonthnum,lo.discount,lo.quantity
====
View2
create materialized view View2 as select d.year as d_year , p.brand1 as p_brand1 , p.category as p_category , s.nation as s_nation , s.region as s_region , sum(lo.revenue)   from lineorder lo  join date_dim d on lo.orderdate = d.datekey join part p on lo.partkey = p.partkey join supplier s on lo.suppkey = s.suppkey( p.category = 'MFGR#12' and s.region = 'AMERICA' ) or ( p.brand1 = 'MFGR#2221' and s.region = 'EUROPE' and s.nation = 'SWEDEN' ) or ( p.brand1  =  'MFGR#2221' and s.region = 'EUROPE' ) or ( p.brand1 between 'MFGR#2221' and 'MFGR#2228' and s.region = 'ASIA' )  group by d.year,p.brand1,p.category,s.nation,s.region
====
View3
create materialized view View3 as select c.city as c_city , c.name as c_name , c.nation as c_nation , c.region as c_region , d.year as d_year , d.yearmonth as d_yearmonth , s.city as s_city , s.nation as s_nation , s.region as s_region , sum(lo.revenue) as revenue   from lineorder lo  join customer c on lo.custkey = c.custkey join date_dim d on lo.orderdate = d.datekey join supplier s on lo.suppkey = s.suppkey( c.region = 'ASIA' and s.region = 'ASIA' and d.year >= 1992 and d.year <= 1997 ) or ( c.nation = 'UNITED STATES' and s.nation = 'UNITED STATES' and d.year >= 1992 and d.year <= 1997 ) or ( ( c.city = 'UNITED KI1' or c.city = 'UNITED KI5' ) and ( s.city = 'UNITED KI1' or s.city = 'UNITED KI5' ) and d.yearmonth = 'Dec1997' ) or ( ( c.city = 'UNITED KI1' or c.city = 'UNITED KI5' ) and ( s.city = 'UNITED KI1' or s.city = 'UNITED KI5' ) and d.year >= 1992 and d.year <= 1997 )  group by c.city,c.name,c.nation,c.region,d.year,d.yearmonth,s.city,s.nation,s.region
====
View0
create materialized view View0 as select c.nation as c_nation , c.region as c_region , d.year as d_year , p.brand1 as p_brand1 , p.category as p_category , p.mfgr as p_mfgr , s.city as s_city , s.nation as s_nation , s.region as s_region , sum(lo.revenue - lo.supplycost) as profit   from lineorder lo  join customer c on lo.custkey = c.custkey join date_dim d on lo.orderdate = d.datekey join part p on lo.partkey = p.partkey join supplier s on lo.suppkey = s.suppkey where ( c.region = 'AMERICA' and s.nation = 'UNITED STATES' and ( d.year = 1997 or d.year = 1998 ) and p.category = 'MFGR#14' ) or ( c.region = 'AMERICA' and s.region = 'AMERICA' and ( p.mfgr = 'MFGR#1' or p.mfgr = 'MFGR#2' ) ) or ( c.region = 'AMERICA' and s.region = 'AMERICA' and ( d.year = 1997 or d.year = 1998 ) and ( p.mfgr = 'MFGR#1' or p.mfgr = 'MFGR#2' ) )  group by c.nation,c.region,d.year,p.brand1,p.category,p.mfgr,s.city,s.nation,s.region
====
View1
create materialized view View1 as select d.weeknuminyear as d_weeknuminyear , d.year as d_year , d.yearmonthnum as d_yearmonthnum , lo.discount as lo_discount , lo.quantity as lo_quantity , sum(lo.extendedprice * lo.discount) as revenue   from lineorder lo  join date_dim d on lo.orderdate = d.datekey where ( d.year = 1993 and lo.discount between 1 and 3 and lo.quantity < 25 ) or ( d.weeknuminyear = 6 and d.year = 1994 and lo.discount between 5 and 7 and lo.quantity between 26 and 35 ) or ( d.yearmonthnum = 199401 and lo.discount between 4 and 6 and lo.quantity between 26 and 35 )  group by d.weeknuminyear,d.year,d.yearmonthnum,lo.discount,lo.quantity
====
View2
create materialized view View2 as select d.year as d_year , p.brand1 as p_brand1 , p.category as p_category , s.nation as s_nation , s.region as s_region , sum(lo.revenue)   from lineorder lo  join date_dim d on lo.orderdate = d.datekey join part p on lo.partkey = p.partkey join supplier s on lo.suppkey = s.suppkey where ( p.category = 'MFGR#12' and s.region = 'AMERICA' ) or ( p.brand1 = 'MFGR#2221' and s.region = 'EUROPE' and s.nation = 'SWEDEN' ) or ( p.brand1  =  'MFGR#2221' and s.region = 'EUROPE' ) or ( p.brand1 between 'MFGR#2221' and 'MFGR#2228' and s.region = 'ASIA' )  group by d.year,p.brand1,p.category,s.nation,s.region
====
View3
create materialized view View3 as select c.city as c_city , c.name as c_name , c.nation as c_nation , c.region as c_region , d.year as d_year , d.yearmonth as d_yearmonth , s.city as s_city , s.nation as s_nation , s.region as s_region , sum(lo.revenue) as revenue   from lineorder lo  join customer c on lo.custkey = c.custkey join date_dim d on lo.orderdate = d.datekey join supplier s on lo.suppkey = s.suppkey where ( c.region = 'ASIA' and s.region = 'ASIA' and d.year >= 1992 and d.year <= 1997 ) or ( c.nation = 'UNITED STATES' and s.nation = 'UNITED STATES' and d.year >= 1992 and d.year <= 1997 ) or ( ( c.city = 'UNITED KI1' or c.city = 'UNITED KI5' ) and ( s.city = 'UNITED KI1' or s.city = 'UNITED KI5' ) and d.yearmonth = 'Dec1997' ) or ( ( c.city = 'UNITED KI1' or c.city = 'UNITED KI5' ) and ( s.city = 'UNITED KI1' or s.city = 'UNITED KI5' ) and d.year >= 1992 and d.year <= 1997 )  group by c.city,c.name,c.nation,c.region,d.year,d.yearmonth,s.city,s.nation,s.region
====
